import numpy as np
import pandas as pd

from absenteeism.dataprep.constants import (
    COLUMNS_INPUT,
    COLUMNS_TRAINING,
    FILE_INPUT,
    FILE_TRAINING,
    MAP_EDUCATION_HIGH_SCHOOL_OR_GT,
)
from absenteeism.utils import snake_case_columns


class AbsenteeismPreprocessor:
    """
    Custom data preprocessor for the "Absenteeism at Work" dataset.

    Provides the following functionality:
        - Load training or input data from a CSV file
        - Automatically distinguish between a training dataset and
          an input data file
        - Apply different preprocessing operations depending on the
          loaded data file
        - Store preprocessed data into a CSV file
    """

    def __init__(self, df: pd.DataFrame):
        """
        Initialize the preprocessor with a pandas DataFrame.

        :param df: A pandas DataFrame containing the data to preprocess
        """

        # Check if dataframe contains valid data columns, and set type
        # to either FILE_INPUT or FILE_TRAINING based on columns that
        # match
        if list(df.columns) == COLUMNS_INPUT:
            self._type = FILE_INPUT
        elif list(df.columns) == COLUMNS_TRAINING:
            self._type = FILE_TRAINING
        else:
            raise ValueError("Dataframe contains invalid data columns")

        # Convert columns to snake case and store dataframe reference
        df.columns = snake_case_columns(df.columns)
        self._df: pd.DataFrame = df

    @classmethod
    def from_csv(cls, file_path):
        """
        Load data from a CSV file and return a new instance of the
        preprocessor. This is the preferred way to create a new
        preprocessor instance.

        :param file_path: Path to the CSV file to load
        :return: A new instance of the preprocessor
        """
        df = pd.read_csv(file_path)
        return cls(df=df)

    def preprocess(self):
        """
        Apply preprocessing operations to the dataframe based on the
        type of data that was loaded.

        :return: The preprocessed dataframe
        """
        if self.is_input():
            self._preprocess_input_data()
        elif self.is_training():
            self._preprocess_training_data()
        return self._df

    def dump_csv(self, file_path):
        """
        Write the contents of the current dataframe to a CSV file.

        :param file_path: Path to the file to write
        """
        self._df.to_csv(file_path, index=False)

    def is_input(self):
        """
        Helper method to check if the preprocessor is working on input
        data.

        :return: Returns True if working on input data, False otherwise
        """
        return self._type == FILE_INPUT

    def is_training(self):
        """
        Helper method to check if the preprocessor is working on training
        data.

        :return: Returns True if working on training data, False otherwise
        """
        return self._type == FILE_TRAINING

    def _preprocess_input_data(self):
        """
        Apply required preprocessing operations to input data columns.
        """
        self._categorize_absence_reasons()
        self._extract_month_and_day_of_the_week()
        self._recategorize_education_level()
        self._reorder_columns()

        # Replace any NaN values with 0
        self._df = self._df.fillna(value=0).astype("int64")

        # Drop unnecessary columns
        self._df = self._df.drop(
            [
                "id",
                "reason_for_absence",
                "date",
                "dotw",
                "daily_work_load_average",
                "distance_to_work",
            ],
            axis=1,
        )

    def _preprocess_training_data(self):
        """
        Apply required preprocessing operations to training data columns.
        """
        self._categorize_absence_reasons()
        self._extract_month_and_day_of_the_week()
        self._recategorize_education_level()
        self._reorder_columns()
        self._define_targets()

        # Drop unnecessary columns
        self._df = self._df.drop(
            [
                "id",
                "reason_for_absence",
                "date",
                "absenteeism_time_in_hours",
                "dotw",
                "daily_work_load_average",
                "distance_to_work",
            ],
            axis=1,
        )

    def _categorize_absence_reasons(self):
        """
        Categories the absence reasons into four distinct categories from
        the original reason for absence column. Updates the dataframe in
        place.
        """

        # Generate dummy category values table from reason for absence column
        reason_df = pd.get_dummies(self._df["reason_for_absence"], drop_first=True, dtype=int)

        # Group reason codes into four distinct categories
        reason_disease = reason_df.loc[:, 1:14].max(axis=1)
        reason_maternity = reason_df.loc[:, 15:17].max(axis=1)
        reason_external = reason_df.loc[:, 18:21].max(axis=1)
        reason_medical = reason_df.loc[:, 22:].max(axis=1)

        # Add reason category columns
        reason_labels = ["disease", "maternity", "external", "medical"]
        reason_values = [reason_disease, reason_maternity, reason_external, reason_medical]
        for label, values in zip(reason_labels, reason_values):
            self._df[f"reason_{label}"] = values

    def _extract_month_and_day_of_the_week(self):
        """
        Extracts the month and day of the week from the date column and
        adds them as new columns to the dataframe. Updates the dataframe
        in place.
        """
        # Parse date column (in format "dd/mm/YYYY") to Python 'date' objects, in place
        self._df["date"] = pd.to_datetime(self._df["date"], format="%d/%m/%Y")

        # Extract months and days of the week for each row
        self._df["month"] = [self._df["date"][x].month for x in range(len(self._df))]
        self._df["dotw"] = [self._df["date"][x].weekday() for x in range(len(self._df))]

    def _recategorize_education_level(self):
        """
        Recategorizes the 'education' column into high school or greater
        than high school. Updates the dataframe in place.
        """

        # Categorize 'education' as only high school or greater than high school, in place
        self._df["education"] = self._df["education"].map(MAP_EDUCATION_HIGH_SCHOOL_OR_GT)

    def _reorder_columns(self):
        """
        Drops unnecessary columns and reorders the columns in the
        dataframe to match the expected order. Updates the dataframe in
        place.
        """

        # Columns to move to the front
        new_columns = [
            "reason_disease",
            "reason_maternity",
            "reason_external",
            "reason_medical",
            "month",
            "dotw",
        ]

        if self.is_input():
            new_columns.extend(snake_case_columns(COLUMNS_INPUT))
        elif self.is_training():
            new_columns.extend(snake_case_columns(COLUMNS_TRAINING))

        # Reorder columns
        self._df = self._df[new_columns]

    def _define_targets(self):
        """
        Defines the target column for the training data. Updates the
        dataframe in place.
        """
        # Determine median values absence time in hours
        absence_median = self._df["absenteeism_time_in_hours"].median()

        # Calculate targets for excessive absence when absence time in hours > median
        self._df["excessive_absence"] = np.where(
            self._df["absenteeism_time_in_hours"] > absence_median, 1, 0
        )
