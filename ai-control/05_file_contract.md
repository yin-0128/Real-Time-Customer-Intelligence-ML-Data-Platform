# File Contract

Expected Structure:

src/
├── ingestion/
├── processing/
├── models/
├── api/

Rules:
- ingestion: only Kafka-related code
- processing: only Spark jobs
- models: ML logic only
- api: FastAPI only

DO NOT mix responsibilities