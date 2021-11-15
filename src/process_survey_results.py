import os

import pandas as pd
import yaml


def load_env_var(env_file_path):
    """Loads all of the environment variables from config/env.yml into
    the os environment.

    Args:
        env_file_path (str): The path to the env yml file

    """
    print("loading environment variables")
    with open(env_file_path, "r") as stream:
        try:
            env_config = yaml.safe_load(stream)
            for var in env_config["env_var"]:
                os.environ[var] = env_config["env_var"][var]
        except yaml.YAMLError as exc:
            print(exc)


def load_survey_data():
    """Reads the survey results from configured location"""
    columns = [
        "timestamp",
        "role",
        "years_experience",
        "programming_language",
        "programming_package",
        "data_tool",
        "cloud_provider",
    ]
    survey_df = pd.read_csv(os.environ["survey_results"], names=columns, skiprows=1)
    # do not care about the timestamp column
    survey_df = survey_df.drop(columns="timestamp")

    return survey_df


def standardize_survey_list(row):
    """This function takes in a list for a given row of a survey result and will
    lower-case it and strip it of all white space

    Args:
        row (list): A list of survey results

    Returns:
        list: standardized survey results
    """
    # lowers all strings and strips whitespace
    clean_row = [x.lower().strip() for x in row]
    return list(set(clean_row))


def map_values_for_column(df, target_column, mapped_df):
    """This method will loop through each entry in a mapping dataframe
    and replace the original values with the mapped values.  This is helpful
    for cleaning up the results for analysis.

    All mapped values can be found in the `mapping/` directory.

    Args:
        df (Dataframe): The dataframe where the values are being re-mapped
        target_column (str): The column that will have the values re-mapped
        mapped_df (Dataframe): The mapping dataframe that has the mappings

    Returns:
        Dataframe: A dataframe with the newly mapped values
    """

    for index, row in mapped_df.iterrows():
        df[target_column] = df[target_column].replace([row[0]], row[1])

    return df


def main():
    load_env_var("config/env.yml")
    survey_data_df = load_survey_data()
    print(survey_data_df.head())


if __name__ == "__main__":
    main()
