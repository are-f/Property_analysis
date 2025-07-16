# Phase 2: Data Extraction System

This module is part of a multi-phase intelligent agent system designed for real estate data analysis. Phase 2 focuses on **extracting**, **validating**, and **indexing** property records — especially those with **industrial zoning classifications** (e.g., M1, M2, I-1, I-2).

---

## Capabilities

- Fetches property records from a public API.
- Filters records based on industrial zoning codes.
- Validates that required fields (e.g., zoning, square footage) are present.
- Detects outliers and invalid data entries.
- Logs all validation failures with full context.
- Stores cleaned data to disk.
- Chunks and indexes the cleaned data using a RAG-ready vector store for future querying (e.g., Phase 3: Comparable Analysis).

# Input
- Api of the dataset user discovers from phase1

# Output
- Cleaned data: data/filtered_industrial_data.json

- Validation errors: data/logs/validation_errors.log

- Vector index: rag/vector_index/

# Sample Queries
- 
