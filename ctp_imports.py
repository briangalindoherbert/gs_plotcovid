# encoding=utf-8
""" ctp_imports integrates raw data on covid from the coovidtrackingproject, using functions I wrote
for the gmapsapi app
"""

from typing import OrderedDict

import pandas as pd

def get_covUS(fnam: str, col_nums: set, renamec: OrderedDict) -> pd.DataFrame:
    """ getGA reads the daily GA covid stats file from covidtracking project
    :param fnam: the path plus name for the file to be read. 1. identify dtypes
    for incoming file and use it in creating pd.DF, 2. add calculated columns
    from one or more existing columns, 3. re-order the columns for usability
    :type fnam: str
    :param col_nums: list of integers identifying columns to import from csv file
    :type col_nums: frozenset
    :param renamec: sequence of pairs with new columns old columns
    :type renamec: OrderedDict
    :return: usdf
    :rtype: pd.DataFrame
    """
    usdf: pd.DataFrame = pd.read_csv(fnam, header=0, chunksize=25, usecols=lambda c: c in set(col_nums))

    df_dt = pd.DataFrame([dfcol.dtypes for dfcol in usdf])
    dt_dict = df_dt.max().to_dict()

    usdf: pd.DataFrame = pd.read_csv(fnam, header=0, dtype=dt_dict, usecols=lambda c: c in set(col_nums))
    return usdf

def chg_cols(usdf: pd.DataFrame, renamec: OrderedDict):
    usdf.rename(columns=renamec, inplace=True, errors='raise')
    usdf.Date = pd.to_datetime(usdf.Date, format='%Y%m%d', errors='ignore')

    # Pandas doc says to insert col use list(range(len(<df>.index)))
    usdf['dPosTest'] = list(range(len(usdf.index)))
    usdf['dPosTest'] = usdf['aggPosTest'].diff(periods=-1)

    usdf['dailyPosRate'] = list(range(len(usdf.index)))
    usdf['dailyPosRate'] = usdf['dPosTest'] / usdf['dResults']
    usdf = usdf.round({'dailyPosRate': 3})

    usdf['daggICU'] = list(range(len(usdf.index)))
    usdf['daggICU'] = usdf['aggICU'].diff(periods=-1)

    return usdf

def get_ctpstate(fnam: str):
    """ ge_ctpstate reads the daily ctp stats for a particular state
    :param fnam: the path plus name for the file to be read
    :type fnam:
    :return:
    :rtype:
    """
    stdf = pd.read_csv(fnam, header=0, parse_dates=True)
    stdf.set_index('date')
    return stdf

def get_corr(dfx: pd.DataFrame):
    """
    get_corr looks for a time-lag correlation between positive tests and hospital admissions and deaths
    :param dfx: a dataframe with either U.S. or State level covid-19 data
    :type dfx:
    :return:
    :rtype:
    """
