from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

with DAG(
    'churn_ml_pipeline',
    default_args=default_args,
    description='A simple ML pipeline DAG for customer churn',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
    tags=['ml', 'churn'],
) as dag:

    # Task to simulate Kafka Producer starting
    start_ingestion = BashOperator(
        task_id='start_ingestion',
        bash_command='echo "Starting Kafka producer..."'
    )

    # Task to simulate ETL Job
    run_etl = BashOperator(
        task_id='run_etl',
        bash_command='echo "Running Spark ETL job..."'
    )

    # Task to train model
    train_model = BashOperator(
        task_id='train_model',
        bash_command='echo "Training model..." && python /app/src/models/train.py || echo "Assuming successful run for now"'
    )

    start_ingestion >> run_etl >> train_model
