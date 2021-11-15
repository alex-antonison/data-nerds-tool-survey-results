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
    lower-case it and strip out white space from left and right of the string.

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
    and replace the original values with the mapped values in the source dataframe.
    This is helpful for cleaning up the results for analysis.

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


def process_survey_results(df, survey_column, mapping_df=None):
    """This method will produce individual dataframes with the specified `survey_column`
    results processed and ready for analysis.  Lastly it aggregates the results into a single count
    column.

    Args:
        df (dataframe): The survey dataframe that has the survey results
        survey_column (str): The survey column of interest
        mapping_df (dataframe, optional): If provided, this will be used to map values for a specified survey column. Defaults to None.

    Returns:
        dataframe: A dataframe that includes a single survey column with standardized and mapped results
    """

    df = df[["role", "years_experience", survey_column]]

    # convert survey column into an array
    df = df.assign(survey_column=df[survey_column].str.split(","))

    # only keep survey columns that have populated values
    df = df[pd.notnull(df["survey_column"])]

    # standardize all of the survey results
    df["survey_column"] = df.apply(lambda row: standardize_survey_list(row["survey_column"]), axis=1)

    # this pivots the list in each row to itself be its own row
    df = df.explode("survey_column")

    # reset index and rename column to the survey column
    # name provided
    df = df.reset_index(drop=True).drop(columns=survey_column).rename(columns={"survey_column": survey_column})

    # replace mapped values
    if mapping_df is not None:
        df = map_values_for_column(df, target_column=survey_column, mapped_df=mapping_df)

    # get rid of null and empty columns
    df = df[df[survey_column].notnull()]
    df = df[df[survey_column] != ""]

    # aggregate results
    df = df.groupby(list(df.columns)).size().reset_index(name="count")

    return df


def main():
    load_env_var("config/env.yml")

    # load survey data
    survey_data_df = load_survey_data()

    # load mapping data
    role_map_df = pd.read_csv(os.environ["role_mapping"])
    prog_language_map_df = pd.read_csv(os.environ["programming_language_mapping"])
    prog_package_map_df = pd.read_csv(os.environ["programming_package_mapping"])
    data_tool_mapping_df = pd.read_csv(os.environ["data_tool_mapping"])
    cloud_provider_mapping_df = pd.read_csv(os.environ["cloud_provider_mapping"])

    # standardize roles from survey results
    survey_data_df = map_values_for_column(survey_data_df, "role", role_map_df)

    # process the survey results
    programming_language_survey_df = process_survey_results(
        survey_data_df, survey_column="programming_language", mapping_df=prog_language_map_df
    )
    programming_package_survey_df = process_survey_results(
        survey_data_df, survey_column="programming_package", mapping_df=prog_package_map_df
    )
    data_tools_survey_df = process_survey_results(
        survey_data_df, survey_column="data_tool", mapping_df=data_tool_mapping_df
    )
    cloud_provider_survey_df = process_survey_results(
        survey_data_df, survey_column="cloud_provider", mapping_df=cloud_provider_mapping_df
    )

    # save out to csv
    programming_language_survey_df.to_csv(os.environ["output_programming_language"], index=False)
    programming_package_survey_df.to_csv(os.environ["output_programming_package"], index=False)
    data_tools_survey_df.to_csv(os.environ["output_data_tool"], index=False)
    cloud_provider_survey_df.to_csv(os.environ["output_cloud_provider"], index=False)


if __name__ == "__main__":
    main()
