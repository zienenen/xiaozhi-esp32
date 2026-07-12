# datasets

Owns real scenic dataset status and knowledge search.

Phase 1 scope:
- Use real scenic data
- Keep the final source format flexible
- Provide minimal frontend schema:
  - `dataset_id`
  - `name`
  - `status`
  - `chunk_count`
  - `summary_items`
  - `updated_at`
- Provide `/api/v1/knowledge/search` for xiaozhi-side tool/MCP calls

`pgvector` can be added later if real vector search enters the implementation path.
