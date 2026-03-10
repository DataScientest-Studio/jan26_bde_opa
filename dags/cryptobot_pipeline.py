from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="cryptobot_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False
) as dag:

    build_features = BashOperator(
        task_id="build_features",
        bash_command="python /opt/airflow/src/features/build_features.py"
    )

    train_model = BashOperator(
        task_id="train_model",
        bash_command="python /opt/airflow/src/models/train_model.py"
    )

    build_features >> train_model