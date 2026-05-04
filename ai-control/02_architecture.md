# Architecture

Components:

1. Data Ingestion
   - Kafka producer (simulate events)
   - Kafka consumer

2. Data Processing
   - Spark jobs for ETL

3. Storage
   - PostgreSQL (structured data)

4. ML Pipeline
   - Train churn model
   - Save model

5. API
   - FastAPI service

6. Dashboard
   - Streamlit app

7. Orchestration
   - Airflow DAGs

8. Infrastructure
   - Docker Compose

Data Flow:
Kafka → Spark → PostgreSQL → ML → API → Dashboard