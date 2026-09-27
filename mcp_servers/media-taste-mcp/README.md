# Media Taste MCP

A small, local **Model Context Protocol (MCP)** server built as my first hands-on exploration of MCP and AI tool integration.

The project intentionally keeps the scope simple. Instead of jumping directly into databases, RAG, embeddings, external APIs, or complex recommendation systems, I wanted to understand the fundamentals first — how an MCP server exposes tools, how an AI client interacts with them, and how persistent data can be made available to an LLM.

The result is a personal movie-history server that lets Claude manage and reason over my movie preferences.

> **Simple by design, built as a foundation for more ambitious MCP projects.**

---

## Overview

Media Taste MCP gives an MCP-compatible AI client access to a local movie history stored in a JSON file.

The AI can use the exposed tools to:

* Add movies to the history
* Update ratings, likes/dislikes, and notes
* Search and filter the history
* Retrieve the complete history for taste analysis

The MCP server is responsible for **data access and persistence**, while the AI client is responsible for **reasoning and interpretation**.

```text
┌─────────────────────┐
│    Claude Desktop   │
│                     │
│  AI reasoning       │
└──────────┬──────────┘
           │
           │ MCP / stdio
           ▼
┌─────────────────────┐
│  Media Taste MCP    │
│                     │
│  add_media          │
│  rate_media         │
│  search_media       │
│  get_taste_profile  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│     movies.json     │
│                     │
│  Local persistence  │
└─────────────────────┘
```

---

## Features

### `add_media`

Adds a movie to the personal movie history.

Example request:

```text
Add Inception (2010), genres Sci-Fi and Thriller.
```

The tool creates a unique movie ID based on the title and year and stores the movie in `movies.json`.

---

### `rate_media`

Updates an existing movie.

Supported fields:

* `rating`
* `liked`
* `notes`

The tool supports **partial updates**, meaning only the fields provided by the user are modified.

For example, changing only a rating does not overwrite the existing notes or like/dislike status.

---

### `search_media`

Searches the movie history using optional filters.

Supported filters:

| Filter       | Description                     |
| ------------ | ------------------------------- |
| `query`      | Case-insensitive title search   |
| `genre`      | Genre filter                    |
| `min_rating` | Minimum rating                  |
| `max_rating` | Maximum rating                  |
| `liked`      | Filter by liked/disliked status |

Multiple filters are combined using **AND** logic.

For example:

```text
genre = "Sci-Fi"
min_rating = 8
```

means:

> Find movies that are Sci-Fi **AND** have a rating of at least 8.

Unrated movies are not treated as having a rating of `0`; they remain unrated.

---

### `get_taste_profile`

Returns the user's movie history so that the AI can analyze it.

The MCP server does **not** hard-code conclusions such as:

```text
favorite_genre = "Sci-Fi"
```

Instead, it provides the underlying data and allows the LLM to reason over:

* Ratings
* Genres
* Likes/dislikes
* Personal notes
* Movie history

This allows Claude to identify patterns dynamically as more movies are added.

---

## Example AI Interactions

Once connected to Claude Desktop, natural-language requests can trigger the appropriate MCP tools.

### Retrieve history

```text
What movies do I have in my personal movie history?
```

Claude can call:

```text
get_taste_profile
```

and present the stored movies.

### Search

```text
What Sci-Fi movies have I rated highly?
```

Claude can use:

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

### Update a movie

```text
I watched The Edge of Tomorrow and I'd give it a 9.5.
I really enjoyed the action and the time-loop concept.
```

Claude can call:

```text
rate_media
```

and update the existing movie.

### Taste analysis

```text
What patterns do you notice in my movie taste?
```

Claude can retrieve the movie history and reason over the data rather than relying on hard-coded recommendation logic.

---

## Tech Stack

* **Python** — MCP server implementation
* **MCP Python SDK** — Model Context Protocol server
* **uv** — Python project and dependency management
* **JSON** — Local persistent storage
* **Claude Desktop** — MCP client
* **MCP Inspector** — MCP server development and testing

---

## Project Structure

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

contains the actual local movie history and should **not** be committed to GitHub.

It is included in `.gitignore`.

### Example data

```text
data/movies.example.json
```

is a safe sample dataset committed to the repository.

It demonstrates the expected structure without exposing personal movie history.

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
    "notes": "Loved the concept and the layered storytelling."
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
    "notes": "Great rewatch value and an excellent ending."
  },
  {
    "id": "edge-of-tomorrow-2014",
    "title": "Edge of Tomorrow",
    "year": 2014,
    "genres": [
      "Sci-Fi",
      "Action"
    ]
  },
  {
    "id": "the-terminal-2004",
    "title": "The Terminal",
    "year": 2004,
    "genres": [
      "Comedy",
      "Drama"
    ],
    "rating": 8,
    "liked": true,
    "notes": "A wholesome and surprisingly emotional movie."
  }
]
```

The example deliberately contains both **rated and unrated movies** so the behavior of the search filters is clear.

---

## Getting Started

### Prerequisites

Install:

* Python 3.13+
* `uv`

The project was developed and tested with Python 3.13+.

---

### 1. Clone the repository

```bash
git clone https://github.com/yuvraj-9999/AIML-Assignments
cd mcp_servers/media-taste-mcp
```

---

### 2. Install dependencies

```bash
uv sync
```

---

### 3. Create your local data file

Copy the example dataset:

```powershell
Copy-Item data/movies.example.json data/movies.json
```

Then modify `movies.json` with your own movie history.

The application reads:

```text
data/movies.json
```

and does not modify `movies.example.json`.

---

## Testing with MCP Inspector

MCP Inspector was used during development to test tool discovery, arguments, results, and server behavior before connecting the server to Claude Desktop.

Run:

```bash
uv run mcp dev src/media_taste_mcp/server.py
```

This launches the MCP development workflow and allows the available tools to be tested individually.

The server exposes:

```text
add_media
rate_media
search_media
get_taste_profile
```

---

## Claude Desktop Setup

The server can be connected to Claude Desktop as a local MCP server.

Example configuration:

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

The exact configuration location depends on the Claude Desktop installation and operating system.

After restarting Claude Desktop, the `media-taste` MCP server should expose the four tools to the client.

---

## MCP Architecture

The project follows a simple client/server architecture.

### MCP Client

Claude Desktop acts as the MCP client.

It:

* Discovers available tools
* Determines when a tool is useful
* Supplies tool arguments
* Receives tool results
* Reasons over the returned information

### MCP Server

Media Taste MCP acts as the server.

It:

* Defines the available tools
* Validates tool arguments through the MCP schema
* Reads and writes local data
* Returns structured results

### Storage

A local JSON file provides persistence.

This keeps the project intentionally lightweight and removes the need for:

* MongoDB
* PostgreSQL
* Redis
* Cloud storage

---

## Design Decisions

### Why JSON?

The goal of V1 is to understand MCP rather than database engineering.

JSON provides enough persistence for a small personal dataset while keeping the implementation easy to inspect and understand.

### Why no recommendation algorithm?

The MCP server provides **data**, not conclusions.

Instead of implementing a custom recommendation engine, the project lets the connected LLM reason over the user's actual history.

This keeps the responsibilities separated:

```text
MCP Server → Data access
LLM        → Reasoning
```

### Why no external movie API?

The project focuses on personal movie data rather than movie metadata retrieval.

External APIs can be introduced later without changing the fundamental MCP architecture.

---

## What I Learned

This project was built as a hands-on introduction to MCP.

Key concepts explored:

* MCP client/server architecture
* MCP tools
* Tool schemas
* Tool arguments
* Structured tool results
* stdio transport
* MCP Inspector
* Persistent local state
* Partial updates
* Optional arguments
* Handling missing data
* LLM tool calling
* Separating data access from AI reasoning
* Connecting a custom MCP server to Claude Desktop
* Managing a Python project with `uv`

One particularly useful lesson was handling partial updates correctly.

For example:

```python
if "liked" in updates:
    movie["liked"] = updates["liked"]
```

checks whether the caller actually supplied the field, allowing:

```text
liked = false
```

to remain distinguishable from:

```text
liked was not provided
```

---

## Scope

This is intentionally a **V1 learning project**.

It currently does not include:

* External movie APIs
* Web scraping
* Databases
* Vector databases
* RAG
* Embeddings
* Recommendation algorithms
* Authentication
* Cloud deployment
* Frontend UI
* Multi-user support
* TV shows, books, music, or other media types

The goal was to understand the MCP fundamentals first and establish a working foundation for more ambitious projects.

---

## Possible Future Improvements

Potential extensions include:

* Better movie identifiers
* Director and actor information
* Movie metadata from external APIs
* Statistics and analytics
* Importing existing movie history
* More advanced taste analysis
* Support for additional media types
* Database-backed persistence
* Additional MCP tools

These are intentionally outside the current V1 scope.

---

## License

MIT
