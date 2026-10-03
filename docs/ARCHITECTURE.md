# Architecture

```text
React Dashboard
      |
      v
FastAPI /api/v1
      |
      v
Service Layer
  |       |       |
Classification Embeddings Analytics
  |       |       |
  +-------+-------+
          |
      Local files
CSV / JSON / NPY
```

## Boundaries

- Frontend calls FastAPI only.
- API routes validate requests and delegate to services.
- Services own prediction, similarity, urgency and analytics logic.
- Repositories own local file access.
- ML scripts own training, embedding and clustering workflows.
- No database is required.
