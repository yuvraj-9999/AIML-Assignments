# Media Taste MCP

A small, local **Model Context Protocol (MCP)** server built as a hands-on exploration of MCP, AI tool integration, resources, prompts, and persistent personal data.

The project solves a simple but real problem which i actually face as a guy who absolutely love movies:

> **I want an AI assistant that can maintain my personal movie history and use that history to understand how my movie taste evolves over time.**

Instead of building a generic movie recommendation system, Media Taste MCP gives an AI client structured access to my own movie history. The MCP server handles data access and persistence, while the connected LLM handles reasoning and interpretation.

> **Simple by design, built to understand MCP fundamentals before moving to more complex AI systems.**

---

## Overview

Media Taste MCP provides an MCP-compatible AI client with access to a local movie history stored in a JSON file.

The server exposes three types of MCP primitives:

- **Tools** — perform operations on the movie history
- **Resources** — expose addressable movie data
- **Prompts** — provide reusable instructions for analyzing movie taste

The AI can:

- Add movies to the history
- Update ratings, likes/dislikes, and notes
- Search and filter movies
- Access the complete movie history
- Access favorite movies
- Access highly-rated movies
- Analyze overall movie taste
- Analyze how movie preferences evolve over time

The responsibilities are intentionally separated:

```text
┌──────────────────────────┐
│      Claude Desktop      │
│                          │
│     AI reasoning         │
│     Tool calling         │
│     Interpretation       │
└────────────┬─────────────┘
             │
             │ MCP / stdio
             ▼
┌──────────────────────────┐
│     Media Taste MCP      │
│                          │
│ Tools                    │
│ Resources                │
│ Prompts                  │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│       movies.json        │
│                          │
│   Local persistence      │
└──────────────────────────┘
```

---

# MCP Primitives

## Tools

Tools are callable operations that allow the AI client to interact with the user's movie history.

### `add_media`

Adds a movie to the personal movie history.

The tool accepts:

- `title`
- `year`
- `genres`
- `watched_at`

Example request:

```text
Add Inception (2010), genres Sci-Fi and Thriller.
I watched it on September 29, 2026.
```

The movie is stored with a generated ID and its watch date.

Example structure:

```json
{
  "id": "inception-2010",
  "title": "Inception",
  "year": 2010,
  "genres": ["Sci-Fi", "Thriller"],
  "watchedAt": "2026-09-29"
}
```

The `watchedAt` field provides a temporal dimension to the movie history and allows the user's taste to be analyzed chronologically.

---

### `rate_media`

Updates an existing movie.

Supported fields:

- `rating`
- `liked`
- `notes`

The tool uses a partial-update approach.

For example:

```json
{
  "rating": 9.5
}
```

updates only the rating without overwriting the movie's existing notes or like/dislike status.

This also keeps the distinction between:

```text
field was not provided
```

and:

```text
field was explicitly set to false
```

---

### `search_media`

Searches the personal movie history using optional filters.

Supported filters:

| Filter | Description |
|---|---|
| `query` | Case-insensitive title search |
| `genre` | Genre filter |
| `min_rating` | Minimum rating |
| `max_rating` | Maximum rating |
| `liked` | Filter by liked/disliked status |

Multiple filters are combined using **AND** logic.

For example:

```text
genre = "Sci-Fi"
min_rating = 8
```

means:

> Find movies that are Sci-Fi **AND** have a rating of at least 8.

Unrated movies are not treated as having a rating of `0`. They remain unrated and are excluded when a rating boundary is applied.

---

### `get_taste_profile`

Returns the user's movie history so that an AI client can reason over it.

The server does not hard-code conclusions such as:

```text
favorite_genre = "Sci-Fi"
```

Instead, it exposes the underlying data:

- Ratings
- Genres
- Likes/dislikes
- Personal notes
- Watch dates
- Movie history

The LLM can then identify patterns dynamically.

---

# Resources

Resources provide addressable data that an MCP client can read.

Media Taste MCP currently exposes three resources.

## `movie-history://all`

Returns the complete movie history as JSON.

Example:

```text
movie-history://all
```

This provides the full dataset for operations such as general movie-history inspection and taste analysis.

---

## `movie-history://favorites`

Returns movies where the user has explicitly marked:

```json
"liked": true
```

Example:

```text
movie-history://favorites
```

The resource only considers an explicitly `true` value as a favorite.

---

## `movie-history://highly-rated/{rating}`

Returns movies whose rating is greater than or equal to the requested value.

Example:

```text
movie-history://highly-rated/9
```

returns movies rated:

```text
9 or higher
```

Another example:

```text
movie-history://highly-rated/9.8
```

returns only movies rated at least `9.8`.

Movies without a rating are excluded from this resource.

---

# Prompts

Prompts are reusable instruction templates that guide an AI client through a particular task.

Media Taste MCP currently provides two prompts.

## `analyze_movie_taste`

Provides instructions for analyzing the user's overall movie preferences.

The prompt asks the AI to examine:

- Frequently enjoyed genres
- Highly-rated movies
- Recurring themes and characteristics
- Personal notes
- Relationships between ratings and genres
- Possible preference patterns

The prompt also instructs the AI to distinguish between:

1. Observations directly supported by the data
2. Reasonable interpretations

It explicitly discourages inventing preferences that are not supported by the movie history.

---

## `analyze_taste_evolution`

Analyzes how the user's movie taste may have changed over time.

It uses the `watchedAt` field to examine the movie history chronologically.

The prompt asks the AI to look for:

- Changes in genres watched
- Changes in ratings
- Recurring themes over time
- Whether preferences appear broader or more focused
- Changes in the types of movies the user enjoys
- Differences between earlier and more recent movies

It also asks the AI to distinguish genuine trends from patterns that may simply result from a small dataset.

---

# Example AI Interactions

Once connected to an MCP-compatible client such as Claude Desktop, natural-language requests can trigger the appropriate MCP capabilities.

### Retrieve movie history

```text
What movies do I have in my personal movie history?
```

The AI can use the movie-history data exposed by the server.

---

### Search the history

```text
What Sci-Fi movies have I rated highly?
```

The AI can use:

```text
search_media
```

with filters such as:

```json
{
  "genre": "Sci-Fi",
  "min_rating": 8
}
```

---

### Add a movie

```text
I watched Inception today. Add it to my movie history.
```

The AI can call:

```text
add_media
```

with the movie information and watch date.

---

### Update a movie

```text
I watched The Edge of Tomorrow and I'd give it a 9.5.
I really enjoyed the action and the time-loop concept.
```

The AI can use:

```text
rate_media
```

to update the existing movie.

---

### Analyze movie taste

```text
What patterns do you notice in my movie taste?
```

The AI can use the available movie history and the corresponding analysis prompt to reason over the data.

---

### Analyze taste evolution

```text
How has my movie taste changed over time?
```

The `watchedAt` information allows the AI to examine the movie history chronologically.

---

# Tech Stack

- **Python** — MCP server implementation
- **MCP Python SDK** — Model Context Protocol server
- **uv** — Python project and dependency management
- **JSON** — Local persistent storage
- **Claude Desktop** — MCP client
- **MCP Inspector** — MCP server development and testing

---

# Project Structure

```text
media-taste-mcp/
│
├── data/
│   ├── movies.example.json
│   └── movies.json
│
├── src/
│   └── media_taste_mcp/
│       └── server.py
│
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

### Personal data

```text
data/movies.json
```

contains the actual local movie history.

It should **not** be committed to GitHub and is included in `.gitignore`.

### Example data

```text
data/movies.example.json
```

contains a safe sample dataset that demonstrates the expected structure without exposing personal movie history.

Example:

```json
[
  {
    "id": "inception-2010",
    "title": "Inception",
    "year": 2010,
    "genres": [
      "Sci-Fi",
      "Thriller"
    ],
    "rating": 9,
    "liked": true,
    "notes": "Loved the concept and the layered storytelling.",
    "watchedAt": "2026-01-15"
  },
  {
    "id": "the-prestige-2006",
    "title": "The Prestige",
    "year": 2006,
    "genres": [
      "Drama",
      "Mystery",
      "Thriller"
    ],
    "rating": 9.5,
    "liked": true,
    "notes": "Great rewatch value and an excellent ending.",
    "watchedAt": "2026-03-20"
  }
]
```

The example dataset can contain both rated and unrated movies so that search and filtering behavior is easy to understand.

---

# Getting Started

## Prerequisites

Install:

- Python 3.13+
- `uv`

The project was developed and tested with Python 3.13+.

---

## 1. Clone the repository

If this project is inside the `AIML-Assignments` repository:

```bash
git clone https://github.com/yuvraj-9999/AIML-Assignments

cd AIML-Assignments/mcp_servers/media-taste-mcp
```
---

## 2. Install dependencies

```bash
uv sync
```

---

## 3. Create your local data file

Copy the example dataset.

### Windows PowerShell

```powershell
Copy-Item data/movies.example.json data/movies.json
```

Then modify:

```text
data/movies.json
```

with your own movie history.

The application reads:

```text
data/movies.json
```

and does not modify:

```text
data/movies.example.json
```

---

# Testing with MCP Inspector

MCP Inspector was used throughout development to test:

- Tool discovery
- Tool arguments
- Tool results
- Resource discovery
- Resource contents
- Parameterized resources
- Prompt discovery
- Prompt execution
- Server behavior

Run:

```bash
uv run mcp dev src/media_taste_mcp/server.py
```

The server should expose:

### Tools

```text
add_media
rate_media
search_media
get_taste_profile
```

### Resources

```text
movie-history://all
movie-history://favorites
movie-history://highly-rated/{rating}
```

### Prompts

```text
analyze_movie_taste
analyze_taste_evolution
```

The Inspector provides a convenient way to validate each MCP primitive independently before connecting the server to an AI client.

---

# Claude Desktop Setup

Media Taste MCP can be connected to Claude Desktop as a local MCP server.

A typical configuration looks like:

```json
{
  "mcpServers": {
    "media-taste": {
      "command": "uv",
      "args": [
        "--directory",
        "D:\\path\\to\\media-taste-mcp",
        "run",
        "python",
        "src\\media_taste_mcp\\server.py"
      ]
    }
  }
}
```

The important part is that `--directory` points to the **project root**, the directory containing:

```text
pyproject.toml
```

For example:

```text
D:\aiml\mcp_servers\media-taste-mcp
```

The Python server itself is located at:

```text
src\media_taste_mcp\server.py
```

After changing the configuration or moving the project, restart Claude Desktop so that it launches the server using the updated configuration.

The exact Claude Desktop configuration location depends on the operating system and installation method.

---

# MCP Architecture

The project follows a simple MCP client/server architecture.

## MCP Client

Claude Desktop acts as an MCP client.

The client:

- Connects to the MCP server
- Discovers available capabilities
- Determines when tools are useful
- Supplies tool arguments
- Reads available resources
- Uses prompt templates when supported by the client
- Receives structured results
- Reasons over the returned information

---

## MCP Server

Media Taste MCP acts as the MCP server.

The server:

- Defines tools
- Defines resources
- Defines prompts
- Exposes tool schemas
- Reads and writes local movie data
- Returns structured results
- Maintains persistent local state

---

## Storage

A local JSON file provides persistence:

```text
data/movies.json
```

This keeps the project intentionally lightweight and removes the need for:

- MongoDB
- PostgreSQL
- Redis
- Cloud storage

---

# Why This Is an MCP Project

The project intentionally demonstrates the three major MCP primitives required for the assignment:

```text
Tools
  ↓
Perform operations

Resources
  ↓
Expose addressable data

Prompts
  ↓
Provide reusable instructions
```

For example:

```text
add_media
```

is a **tool** because it performs an operation.

```text
movie-history://favorites
```

is a **resource** because it provides addressable movie data.

```text
analyze_movie_taste
```

is a **prompt** because it provides a reusable instruction template for an AI client.

This separation makes the project useful for understanding how MCP servers expose different types of capabilities to AI applications.

---

# Design Decisions

## Why JSON?

The primary goal of V1 is to understand MCP rather than database engineering.

JSON provides enough persistence for a small personal dataset while keeping the implementation:

- Lightweight
- Local
- Easy to inspect
- Easy to modify
- Easy to debug

A database can be introduced later if the project grows.

---

## Why no recommendation algorithm?

The MCP server provides **data and capabilities**, not hard-coded conclusions.

Instead of implementing something like:

```text
favorite_genre = "Sci-Fi"
```

the server exposes the underlying movie history.

The LLM can then reason over:

```text
MCP Server → Data access
LLM        → Reasoning
```

This keeps the responsibilities separated.

---

## Why include `watchedAt`?

A movie history without dates can describe what the user likes, but it cannot meaningfully describe how those preferences change.

Adding:

```json
"watchedAt": "2026-09-29"
```

introduces a temporal dimension.

This makes questions such as:

```text
How has my movie taste changed over time?
```

possible without requiring a separate analytics system.

---

## Why no external movie API?

The project focuses on **personal movie data**, not movie metadata retrieval.

External APIs such as TMDB or OMDb could be integrated later, but they are intentionally outside the current scope.

This keeps the project focused on learning MCP rather than API integration.

---

## Why both tools and resources?

Tools and resources serve different purposes.

A tool is an operation that the AI can invoke:

```text
search_media(...)
```

A resource is an addressable piece of data:

```text
movie-history://favorites
```

Having both in the project makes the distinction between MCP capabilities clearer and provides practical experience with both primitives.

---

## Why prompts?

Prompts provide reusable instructions for recurring AI workflows.

Instead of repeatedly explaining how movie taste should be analyzed, the server provides:

```text
analyze_movie_taste
```

Similarly, the temporal analysis workflow is represented by:

```text
analyze_taste_evolution
```

The prompt defines the analytical task while the underlying movie data remains external to the prompt itself.

---

# What I Learned

This project was built as a hands-on introduction to MCP.

Key concepts explored:

- MCP client/server architecture
- MCP tools
- Tool schemas
- Tool arguments
- Structured tool results
- MCP resources
- Parameterized resources
- MCP prompts
- Prompt registration
- stdio transport
- MCP Inspector
- Persistent local state
- Partial updates
- Optional arguments
- Handling missing data
- LLM tool calling
- Separating data access from AI reasoning
- Connecting a custom MCP server to Claude Desktop
- Managing a Python project with `uv`

One particularly useful lesson was handling partial updates correctly.

For example:

```python
if "liked" in updates:
    movie["liked"] = updates["liked"]
```

checks whether the caller actually supplied the field.

This allows:

```text
liked = false
```

to remain distinguishable from:

```text
liked was not provided
```

Another important lesson was understanding the difference between:

```text
Tool
Resource
Prompt
```

rather than treating all MCP capabilities as simply "functions the AI can call."

---

# Scope

This is intentionally a **V1 learning project**.

It currently does not include:

- External movie APIs
- Web scraping
- Database-backed persistence
- Vector databases
- RAG
- Embeddings
- Recommendation algorithms
- Authentication
- Cloud deployment
- Frontend UI
- Multi-user support
- TV shows, books, music, or other media types

The goal is to understand MCP fundamentals first and establish a clean foundation for more ambitious MCP projects.

---

# Possible Future Improvements

Potential extensions include:

- Better movie identifiers
- Director and actor information
- External movie metadata
- Movie statistics and analytics
- Importing existing movie history
- More advanced taste analysis
- More temporal analysis
- Additional MCP resources
- Additional MCP tools
- Database-backed persistence
- Support for additional media types
- Richer MCP prompt workflows

These are intentionally outside the current V1 scope.

---

# License

MIT