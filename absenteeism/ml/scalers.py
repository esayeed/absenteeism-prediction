import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler


class CustomScaler(BaseEstimator, TransformerMixin):
    """
    Custom scaler class that can be used as a drop-in replacement for
    the StandardScaler class from scikit-learn. This class allows
    for more flexibility in the scaling process, such as the ability
    to scale only specific columns in a dataframe.
    """

    def __init__(self, columns, copy=True, with_mean=True, with_std=True):
        """
        Initialize the custom scaler with the specified parameters.

        :param columns: The columns to scale
        :param copy: Whether to make a copy of the input data
        :param with_mean: Whether to center the data before scaling
        :param with_std: Whether to scale the data to unit variance
        """
        self.scaler = StandardScaler(copy=copy, with_mean=with_mean, with_std=with_std)
        self.columns = columns

        # Used to store the mean and variance of the columns during the fit
        self.mean_ = None
        self.var_ = None

    def fit(self, X, y=None):
        """
        Fit the scaler to the input data.

        :param X: The input data
        :param y: The target data
        :return: The fitted scaler
        """
        self.scaler.fit(X[self.columns], y)

        # Store the mean and variance of the columns
        self.mean_ = np.array(np.mean(X[self.columns]))
        self.var_ = np.array(np.var(X[self.columns]))

        # Return the scaler
        return self

    def transform(self, X, **transform_params):
        """
        Transform the input data using the fitted scaler.

        :param X: The input data
        :param transform_params: Additional parameters
        :return: The transformed dataframe
        """
        # Store the initial column order
        init_col_order = X.columns

        # Scale the specified columns
        X_scaled = pd.DataFrame(self.scaler.transform(X[self.columns]), columns=self.columns)

        # Remove the scaled columns from the dataframe
        X_not_scaled = X.loc[:, ~X.columns.isin(self.columns)]

        # Return the scaled and unscaled data concatenated together
        # and in the original column order
        return pd.concat([X_not_scaled, X_scaled], axis=1)[init_col_order]
