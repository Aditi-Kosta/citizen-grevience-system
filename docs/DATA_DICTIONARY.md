# Canonical data dictionary

| Field | Purpose |
|---|---|
| complaint_id | Stable local complaint identifier |
| source_id | Source-specific identifier |
| source_name | Dataset/source name |
| complaint_text | Original narrative complaint |
| language | Input language |
| category | Predicted/validated civic category |
| department | Department mapped to category |
| severity | Source severity if available |
| urgency_score | Transparent assistance score 0–1 |
| location_text | Human-readable location |
| latitude/longitude | Coordinates when legally/appropriately available |
| submitted_at | Original submission time |
| status | Local workflow state |
| is_duplicate | Duplicate assistance flag |
| duplicate_of | Candidate parent complaint |
| cluster_id | Semantic cluster assignment |
| classifier_confidence | Model confidence |
| classifier_model_version | Classifier version |
| embedding_model_version | Embedding version |
| created_at | Local record creation time |
| updated_at | Local record update time |
