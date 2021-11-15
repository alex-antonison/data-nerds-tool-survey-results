import pandas as pd
import pytest

from process_survey_results import map_values_for_column, standardize_survey_list


@pytest.mark.unit_test
def test_standardize_survey_list():
    """This test ensures that the standardize_survey_list method correctly cleans up the
    different items returning a clean list for analysis
    """
    test_list = ["Pandas", "pandas ", "tidyveRse", " Looker"]

    standardized_list = standardize_survey_list(test_list)
    # sorting to ensure order for test
    standardized_list.sort()
    assert standardized_list == ["looker", "pandas", "tidyverse"]


@pytest.mark.unit_test
def test_map_values_for_column():
    """This test shows that the mapping function correctly maps only the target column
    and correctly maps the desired values"""

    source_df = pd.DataFrame({"col1": ["blue", "red"], "col2": ["val1", "val2"], "col3": ["val3", "val4"]})
    mapping_df = pd.DataFrame({"orig_col": ["blue", "red"], "mapped_col": ["green", "yellow"]})
    target_column = "col1"

    final_df = pd.DataFrame({"col1": ["green", "yellow"], "col2": ["val1", "val2"], "col3": ["val3", "val4"]})

    pd.testing.assert_frame_equal(map_values_for_column(source_df, target_column, mapping_df), final_df)
