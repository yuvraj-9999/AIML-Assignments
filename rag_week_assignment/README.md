# RAG, Vector Databases & Retrieval

This assignment explores the core concepts behind Retrieval-Augmented Generation (RAG), from vector databases and similarity search to practical retrieval techniques and multimodal RAG.

## Sections

### Section A — Vector Databases
Covers the fundamentals of vector databases and how they differ from traditional databases.

- What a vector database is and how it differs from MySQL/PostgreSQL
- Converting raw text into embeddings and storing them
- Exact lookup vs. similarity search and why B-trees are not suitable for embeddings
- Cosine similarity calculation and interpretation
- The role of vector databases in a RAG pipeline

### Section B — Chunking & Retrieval
Implements and compares different techniques used to retrieve relevant information from a text corpus.

- Fixed-size text chunking with overlap
- Dense retrieval using sentence embeddings and cosine similarity
- Sparse retrieval using BM25
- Comparison of dense and sparse retrieval for different queries

The experiments use a movie-related corpus containing information about Ryan Gosling and his movies.

### Section C — Advanced RAG
Explores how RAG can handle information that is not limited to plain text.

- Multimodal RAG for product manuals containing text, diagrams, and images
- Limitations of text-only RAG when important information exists only in images
- Unified embedding space vs. separate indexes with fusion
- Choosing an appropriate multimodal retrieval approach for a product manual scenario.


## Objective

The main goal of this assignment is to understand how modern RAG systems represent, retrieve, and use information, and how retrieval techniques can be extended beyond text to handle multimodal data.