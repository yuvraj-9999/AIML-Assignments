import json
from pathlib import Path
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("Media Taste MCP")

DATA_FILE = Path("data/movies.json")

@mcp.resource("movie-history://all", mime_type="application/json")
def get_movie_history() -> str:
    """Return the user's complete movie history as JSON."""

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        movies = json.load(file)

    return json.dumps(movies, indent=2)


@mcp.resource("movie-history://favorites", mime_type="application/json")
def get_favorite_movies() -> str:
    """Return movies that the user has marked as liked."""

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        movies = json.load(file)

    favorites = [
        movie
        for movie in movies
        if movie.get("liked") is True
    ]

    return json.dumps(favorites, indent=2)

@mcp.resource("movie-history://highly-rated/{rating}", mime_type="application/json")
def get_highly_rated_movies(rating: float) -> str:
    """Return the movies rated at or above the requested rating."""

    with open(DATA_FILE,"r", encoding="utf -8") as file:
        movies = json.load(file)

    highly_rated = [
        movie
        for movie in movies
        if movie.get("rating") is not None
        and movie.get("rating") >= rating
    ]

    return json.dumps(highly_rated, indent=2)


@mcp.tool()
def add_media( title: str, year: int, genres: list[str], watched_at: str, ) -> str:
    """Add a movie to the user's personal movie history"""

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        movies = json.load(file)

    
    movie_id = f"{title.lower().replace(' ', '-')}-{year}"

    movie = {
        "id": movie_id,
        "title": title,
        "year": year,
        "genres": genres,
        "watched_at": watched_at,
    }

    movies.append(movie)

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(movies, file, indent=2)

    return f"Added `{title}` to your movie history"

@mcp.tool()
def rate_media(movie_id: str, updates: dict) -> str:
    """Update the user's rating, like/dislike, or personal notes for a movie."""

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        movies = json.load(file)

    for movie in movies:
        if movie["id"] == movie_id:
            if "rating" in updates:
                movie["rating"] = updates["rating"]
            
            if "liked" in updates:
                movie["liked"] = updates["liked"]

            if "notes" in updates:
                movie["notes"] = updates["notes"]

            with open(DATA_FILE, "w", encoding="utf-8") as file:
                json.dump(movies, file, indent=2)

            return f"Updated '{movie["title"]}'."

    return f"No movie found with id as '{movie_id}'."


@mcp.tool()
def search_media(
    query: str | None = None,
    genre: str | None = None,
    min_rating: float | None = None,
    max_rating: float | None = None,
    liked: bool | None = None,
) -> list[dict]:
    """Search the user's personal movie history using optional filters."""

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        movies = json.load(file)

    results = []

    for movie in movies:

        # Title search
        if query is not None:
            if query.lower() not in movie["title"].lower():
                continue

        # Genre filter
        if genre is not None:
            movie_genres = [
                g.lower() for g in movie.get("genres", [])
            ]

            if genre.lower() not in movie_genres:
                continue

        # Minimum rating
        if min_rating is not None:
            rating = movie.get("rating")

            # Unrated movies do not match a rating filter
            if rating is None or rating < min_rating:
                continue

        # Maximum rating
        if max_rating is not None:
            rating = movie.get("rating")

            # Unrated movies do not match a rating filter
            if rating is None or rating > max_rating:
                continue

        # Like/dislike filter
        if liked is not None:
            if movie.get("liked") != liked:
                continue

        results.append(movie)

    return results


@mcp.tool()
def get_taste_profile() -> list[dict]:
    """Return the user's movie history for taste analysis."""

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        movies = json.load(file)

    return movies

@mcp.prompt()
def analyze_movie_taste() -> str:
    """Analyze the user's movie history and identify meaningful taste patterns."""

    return """
    Analyze my movie taste using my available movie history.

    Look for patterns in:
    - genres I frequently enjoy
    - movies I rate highly
    - recurring themes or characteristics
    - patterns in my personal notes
    - relationships between my ratings and genres
    - how my preferences may have changed over time

    Base your observations on the available movie data.
    Do not invent preferences that are not supported by the data.

    Clearly distinguish between:
    1. Observations directly supported by the data
    2. Reasonable interpretations of those observations
    """

@mcp.prompt()
def analyze_taste_evolution() -> str:
    """Analyze how the user's movie taste has changed over time."""

    return """
    Analyze how my movie taste has evolved over time using my movie history.

    Use the `watchedAt` dates to examine my movies chronologically.

    Look for:
    - changes in the genres I watch
    - changes in the ratings I give
    - recurring themes or characteristics over time
    - whether my preferences appear to be becoming broader or more focused
    - changes in the kinds of movies I seem to enjoy
    - notable shifts between earlier and more recent movies

    For your analysis:

    1. Start with observations directly supported by the movie data.
    2. Then provide reasonable interpretations of those observations.
    3. Distinguish actual trends from patterns that may simply be caused by having a small amount of data.
    4. Do not invent preferences or motivations that are not supported by the data.
    5. Mention missing or insufficient data when it affects the conclusion.

    Present the result as a chronological analysis of my movie taste.
    """

if __name__ == "__main__":
    mcp.run()