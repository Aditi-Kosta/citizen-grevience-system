# Dataset setup

## Primary NLP source

**Civic Complaint Prioritization — NLP approach**
https://github.com/rohanrepo123/Civic-Complaint-Prioritization-a-NLP-approach

The project specification describes this source as approximately 25,000 Indian civic complaint narratives across 32 categories and 4 urgency levels. These claims must be verified against the downloaded files before training.

Expected local placement:

```text
data/raw/civic_complaints.csv
```

Before use, inspect exact columns, license/provenance, language distribution, duplicates, missing values and class distribution.

## Secondary source

Mumbai Nagar Seva BMC Civic Complaint Resolution 2018–2024:
https://www.kaggle.com/competitions/mumbai-nagar-seva-bmc-civic-complaint-resolution-2018-2024/data

Use this for dashboard testing, analytics and trend visualisation unless inspection confirms its text is suitable for NLP training. Treat it as synthetic as described by the source.

## Government context

CPGRAMS public aggregate reference:
https://www.data.gov.in/keywords/CPGRAM

Do not connect this prototype to production government systems.

## Canonical schema

`complaint_id, source_id, source_name, complaint_text, language, category, department, severity, urgency_score, location_text, latitude, longitude, submitted_at, status, is_duplicate, duplicate_of, cluster_id, classifier_confidence, classifier_model_version, embedding_model_version, created_at, updated_at`

Unavailable source fields may be null.

## Large/restricted datasets

Do not commit restricted or oversized datasets. Download them locally, then run `scripts/prepare_dataset.py` to validate and convert them into the canonical schema.
