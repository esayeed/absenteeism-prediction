from pathlib import Path


def get_project_root() -> Path:
    """
    Get the root directory of the project.
    """
    return Path(__file__).parent.parent


def snake_case_columns(columns):
    """
    Convert a list of column names to snake case.

    :param columns: A list of column names to convert
    :return: A list of column names in snake case
    """
    return [col.lower().replace(" ", "_") for col in columns]
