from src.etl.mongo_to_postgres import run_batch
from src.etl.ml_transform import run_ml_transform
from src.etl.dashboard_transform import run_dashboard_transform

def run_pipeline():
    print("[pipeline] Starting batch...")
    run_batch()

    print("[pipeline] Running ML transform...")
    run_ml_transform()

    print("[pipeline] Running dashboard transform...")
    run_dashboard_transform()

    print("[pipeline] Pipeline finished.")


if __name__ == "__main__":
    run_pipeline()