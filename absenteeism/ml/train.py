from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from absenteeism.dataprep.preproc import AbsenteeismPreprocessor
from absenteeism.ml.constants import COLUMNS_TO_OMIT
from absenteeism.ml.scalers import CustomScaler


class AbsenteeismModelTrainer:
    """
    Class that trains a logistic regression model using the
    "Absenteeism at Work" dataset.
    """

    @classmethod
    def train_model(cls, file_path: str):
        """
        Train a logistic regression model using the specified training
        data file. Applies the absenteeism preprocessor to the data,
        then trains a logistic regression model using the custom scaler.
        """
        preprocessor = AbsenteeismPreprocessor.from_csv(file_path)
        df = preprocessor.preprocess()

        # Remove the target column from the input data, and extract
        # columns to scale by omitting extra columns from what
        # remains
        unscaled_inputs = df.iloc[:, :-1]
        columns_to_scale = [
            x for x in unscaled_inputs.columns.values if x not in COLUMNS_TO_OMIT
        ]

        # Scale the input data using custom scaler
        scaler = CustomScaler(columns_to_scale)
        scaled_inputs = scaler.fit_transform(unscaled_inputs)

        # Split the data into training and testing sets
        x_train, x_test, y_train, y_test = train_test_split(
            scaled_inputs,
            df["excessive_absence"],
            train_size=0.8,
            random_state=20,
        )

        # Train the logistic regression model
        model = LogisticRegression()
        model.fit(x_train, y_train)

        # Return model and scaler
        return model, scaler
