# encoding=utf-8
""" otherdata has imports for population, mortality, and other data
to use for comparison and correlation with covid-19 data
"""

import os

import pandas as pd

datadir = "rawdata"

def get_leading(filen: str):
    """get_leading reads leading cod data from file to a DataFrame
    """
    df = pd.read_csv(filen, header=0)
    # cols: int = len(df.columns)
    df['annual'] = list(range(len(df.index)))
    try:
        df['annual'] = df['deaths'] / 4
        df['perpop'] = 100*df['annual']/df['pop']
    except KeyError:
        print('looked beyond end of index in func get_leading()')
    return df

def get_covtrak(filen: str):
    """ covidtracking.com provides an api to query their covid-19 data,
    get_covtrak_api uses the project's api to query values for a state
    :param filen: string containing file to read
    """
    fqfile = os.path.join(datadir, filen)
    covtrak = pd.read_csv(fqfile, header=0)
    return covtrak

def get_codhistory(filen: str):
    """
    get_codhistory reads the CDC history leading cause of death file that spans
    from 1960 to 2017
    :param filen:
    :type filen:
    :return:
    :rtype:
    """
    codhist = pd.read_csv(filen, header=0)
    codhist['per100'] = hist_COD['2017']/1000
    return codhist
