# Real-Time Customer Intelligence & ML Data Platform

An end-to-end data and artificial intelligence platform designed to predict customer churn in real-time. This project features a complete modular pipeline that ingests, processes, stores, and serves data using a modern tech stack.

## 🚀 Overview

The goal of this platform is to:
- **Ingest** simulated user events (login, logout, purchase, view) in real-time.
- **Process** raw events using scalable ETL jobs.
- **Store** transformed data into structured fact and dimension tables.
- **Train & Track** a machine learning model for churn prediction.
- **Serve** predictions through a REST API.
- **Visualize** customer insights and predictions on an interactive dashboard.

## 🏗️ Architecture & Tech Stack

- **Data Ingestion**: Apache Kafka & Zookeeper (Python Producer/Consumer)
- **Data Processing**: Apache Spark (PySpark)
- **Storage**: PostgreSQL (Fact & Dimension modeling)
- **Machine Learning**: Scikit-Learn, MLflow (Experiment tracking), Joblib
- **API Backend**: FastAPI, Uvicorn
- **Frontend Dashboard**: Streamlit
- **Orchestration**: Apache Airflow
- **Infrastructure**: Docker & Docker Compose
- **CI/CD**: GitHub Actions

## 📂 Project Structure

```text
├── ai-control/         # Project documentation and task tracking
├── dags/               # Airflow DAGs for pipeline orchestration
├── dashboard/          # Streamlit frontend app
├── src/
│   ├── api/            # FastAPI backend service
│   ├── ingestion/      # Kafka producers and consumers
│   ├── models/         # ML model training and evaluation
│   ├── processing/     # PySpark ETL jobs
│   └── storage/        # PostgreSQL schema setup scripts
├── Dockerfile          # App container definition
├── docker-compose.yml  # Multi-container infrastructure setup
└── requirements.txt    # Python dependencies
```

## 🛠️ Setup & Installation

### Prerequisites
- Docker and Docker Compose
- Python 3.10+ (for local development)

### 1. Start the Infrastructure
Use Docker Compose to spin up Zookeeper, Kafka, PostgreSQL, the FastAPI backend, and the Streamlit dashboard.

```bash
docker-compose up -d
```

### 2. Run the Schema Setup
Set up the PostgreSQL tables (you can run this locally or inside the API container):
```bash
docker-compose exec api python src/storage/setup_db.py
```

### 3. Generate the ML Model
Train the Random Forest model to generate the necessary artifacts for the API:
```bash
docker-compose exec api python src/models/train.py
```

### 4. Restart the API
Restart the API so it can load the newly generated machine learning model:
```bash
docker-compose restart api
```

## 🖥️ Usage

- **Streamlit Dashboard**: Open your browser and navigate to `http://localhost:8501`.
- **FastAPI Interactive Docs**: Navigate to `http://localhost:8000/docs` to test the `/predict` endpoint directly.
- **Simulate Data Stream**: You can run the Kafka producer to simulate real-time user events:
  ```bash
  docker-compose exec api python src/ingestion/producer.py
  ```

## 🔄 CI/CD
This repository is integrated with GitHub Actions. On every push to the `main` branch, the pipeline will install dependencies and run `flake8` to ensure code quality across the codebase.
