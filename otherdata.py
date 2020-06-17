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
    ldgcause = pd.read_csv(filen, header=0)
    ldgcause['annual'] = ldgcause['deaths'] / 4
    return ldgcause

def get_pops(filen: str):
    """ get_pops reads in projected 2020 pops for all states and U.S.
    """
    pops: pd.DataFrame = pd.read_csv(filen, header=0)
    return pops

def get_covtrak(filen: str):
    """ covidtracking.com provides an api to query their covid-19 data,
    get_covtrak_api uses the project's api to query values for a state
    :param filen: string containing file to read
    """
    fqfile = os.path.join(datadir, filen)
    covtrak = pd.read_csv(fqfile, header=0)
    return covtrak
