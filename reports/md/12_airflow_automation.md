## Orchestration du pipeline avec Airflow

Le pipeline `cryptobot_pipeline` orchestre les différentes étapes du Machine Learning.

1. build_features : préparation du dataset
2. train_model : entraînement du modèle RandomForest

![Airflow DAG](../figures/12_airflow_dag_pipeline.png)
