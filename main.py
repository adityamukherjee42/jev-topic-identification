"""Test Jev's Noul topic-detection against a labeled transcript dataset.

Usage: .venv/bin/python main.py [dataset/life_insurance_transcripts.json]
"""
import sys
from pathlib import Path

from helpers import evaluate, load_dataset, load_env, log_to_mlflow, print_report

ROOT = Path(__file__).parent
DEFAULT_DATASET = ROOT / "dataset" / "life_insurance_transcripts.json"


def main():
    load_env(ROOT)
    dataset_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DATASET
    dataset = load_dataset(dataset_path)
    correct, rows = evaluate(dataset)
    total = len(dataset["transcripts"])
    print_report(correct, rows, total=total)
    log_to_mlflow(dataset_path, correct, rows, total=total)


if __name__ == "__main__":
    main()
