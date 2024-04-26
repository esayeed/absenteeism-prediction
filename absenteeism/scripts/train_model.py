#
# Command that loads and prepares training data, runs regressions, and outputs a
# reusable model and scaler.
#
import pickle

import click

from absenteeism.ml.train import AbsenteeismModelTrainer
from absenteeism.utils import get_project_root


@click.command()
@click.argument("filename")
def train_model(filename: str) -> None:
    """
    Train a model using the specified training data file.

    FILENAME is the path to the file to process.
    """
    root = get_project_root()
    model, scaler = AbsenteeismModelTrainer.train_model(filename)

    # Save the model and scaler to disk
    with open(f"{root}/output/model.pkl", "wb") as f:
        pickle.dump(model, f)

    with open(f"{root}/output/scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)


if __name__ == "__main__":
    train_model()
