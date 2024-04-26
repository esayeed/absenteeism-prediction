#
# Command that loads and prepares input data, runs predictions using a previously
# generated scaler and training model, and outputs the results to a CSV file.
#
import pickle

import click
import pandas as pd

from absenteeism.dataprep.preproc import AbsenteeismPreprocessor
from absenteeism.utils import get_project_root


@click.command()
@click.argument("filename")
def predict_outputs(filename: str) -> None:
    """
    Predict outputs using the specified input data file.

    FILENAME is the path to the file to process.
    """
    root = get_project_root()
    with open(f"{root}/output/model.pkl", "rb") as f:
        model = pickle.load(f)

    with open(f"{root}/output/scaler.pkl", "rb") as f:
        scaler = pickle.load(f)

    # Load and preprocess the data
    preprocessor = AbsenteeismPreprocessor.from_csv(filename)
    input_df = preprocessor.preprocess()

    # Scale the input data and store the predictions in a DataFrame
    scaled_inputs = scaler.transform(input_df)
    predictions_df = pd.DataFrame()
    if scaled_inputs is not None:
        predictions_df["probability"] = model.predict_proba(scaled_inputs)[:, 1]
        predictions_df["prediction"] = model.predict(scaled_inputs)

    # Output the final results including predictions to a CSV file
    output_df = pd.concat([input_df, predictions_df], axis=1)
    output_df.to_csv(f"{root}/output/absenteeism_predictions.csv", index=False)


if __name__ == "__main__":
    predict_outputs()
