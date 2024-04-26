from typing import Final

# Data columns for training and input data. The last column in the
# training data is the target and is not included in the input data.
#
# The columns from the original data file will be converted to snake
# case during processing to make them easier to work with.
COLUMNS_TRAINING = [
    "ID",
    "Reason for Absence",
    "Date",
    "Transportation Expense",
    "Distance to Work",
    "Age",
    "Daily Work Load Average",
    "Body Mass Index",
    "Education",
    "Children",
    "Pets",
    "Absenteeism Time in Hours",
]
COLUMNS_INPUT = COLUMNS_TRAINING[:-1]

# File types
FILE_INPUT: Final[int] = 1
FILE_TRAINING: Final[int] = 2

# Education level codes
EDUCATION_HIGH_SCHOOL: Final[int] = 1
EDUCATION_BACHELORS: Final[int] = 2
EDUCATION_POST_GRAD: Final[int] = 3
EDUCATION_MASTERS_PLUS: Final[int] = 4

# Map of education levels for categorization into
# high school only or greater than high school
# where:
#   0 = high school only
#   1 = greater than high school
MAP_EDUCATION_HIGH_SCHOOL_OR_GT: Final[dict] = {
    EDUCATION_HIGH_SCHOOL: 0,
    EDUCATION_BACHELORS: 1,
    EDUCATION_POST_GRAD: 1,
    EDUCATION_MASTERS_PLUS: 1,
}
