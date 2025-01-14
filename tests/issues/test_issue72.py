import pandas as pd
import numpy as np

import pandas_profiling
from pandas_profiling.model.base import Variable


from pandas_profiling.config import config


# https://github.com/pandas-profiling/pandas-profiling/issues/72
def test_issue72_higher():
    # Showcase (and test) different ways of interfacing with config/profiling report
    config["low_categorical_threshold"].set(2)
    config["check_recoded"].set(False)

    df = pd.DataFrame({"A": [1, 2, 3, 3]})
    df["B"] = df["A"].apply(str)
    report = pandas_profiling.ProfileReport(df)

    # 3 > 2, so numerical
    assert report.get_description()["variables"]["A"]["type"] == Variable.TYPE_NUM
    # Strings are always categorical
    assert report.get_description()["variables"]["B"]["type"] == Variable.TYPE_CAT


def test_issue72_equal():
    df = pd.DataFrame({"A": [1, 2, 3, 3]})
    df["B"] = df["A"].apply(str)
    report = pandas_profiling.ProfileReport(
        df, low_categorical_threshold=3, check_recoded=False
    )

    # 3 == 3, so numerical
    assert report.get_description()["variables"]["A"]["type"] == Variable.TYPE_NUM
    # Strings are always categorical
    assert report.get_description()["variables"]["B"]["type"] == Variable.TYPE_CAT


def test_issue72_lower():
    config["low_categorical_threshold"].set(10)

    df = pd.DataFrame({"A": [1, 2, 3, 3, np.nan]})
    df["B"] = df["A"].apply(str)
    report = df.profile_report(check_recoded=False)

    # 3 < 10, so categorical
    assert report.get_description()["variables"]["A"]["type"] == Variable.TYPE_CAT
    # Strings are always categorical
    assert report.get_description()["variables"]["B"]["type"] == Variable.TYPE_CAT
