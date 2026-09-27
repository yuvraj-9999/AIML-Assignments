import json
from pathlib import Path
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("Media Taste MCP")

DATA_FILE = Path("data/movies.json")

@mcp.tool()
def add_media( title: str, year: int, genres: list[str] ) -> str:
    """Add a movie to the user's personal movie history"""

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        movies = json.load(file)

    
    movie_id = f"{title.lower().replace(' ', '-')}-{year}"

    movie = {
        "id": movie_id,
        "title": title,
        "year": year,
        "genres": genres,
        
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

if __name__ == "__main__":
    mcp.run()