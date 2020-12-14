# encoding=utf-8
"""
simplecovid main project file to display case and death stats in a plot
"""

# from get_historical import *
import os
from uscovid import *
from ctp_imports import *
from get_historical import get_codhistory

pd.set_option("display.date_yearfirst", True)

# Definitions
asofdate = "2020-07-01"
# identify states (by FIPS) to plot
# st_fips = [1,4,5,6,8,9,10,11,12,13,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,
#           44,45,46,47,48,49,50,51,53,54,55,56]
st_fips = [8,13,18,26,36,40]
datadir: str = 'rawdata'
stnam: str = os.path.join(datadir, "us-states.csv")
usfnam: str = os.path.join(datadir, "us.csv")
ldgfile: str = os.path.join(datadir, 'USdeaths 2015-2018 ICD-10.csv')
histcodfile: str = os.path.join(datadir, 'USmort by COD LT rates.csv')
popfile: str = os.path.join(datadir, 'StatePopFIPS2020.csv')
covNDfnam: str = os.path.join(datadir, 'covtracking_NDdaily.csv')

# get state data, population data, and create a state-fips dictionary
cd_us = getus(usfnam)
pdcovid: pd.DataFrame = get_states(stnam)
States: pd.DataFrame = get_pops(popfile)
state_dict: dict = States.to_dict()
print("*"*80)
print("*   the following states will be plotted:")
print("* ")
for x in st_fips:
    print("*   %s " %(state_dict['state'][x]))
print("* ")
print("*"*80)
print(" ")   # prints a box

# ldg_us has CoD, #deaths, population, fatalities/100k
# ldg_us = get_leading(ldgfile)
hist_COD = get_codhistory(histcodfile)
# covid_tracking_project state and US files:
# NDdaily = get_ctpstate(covNDfnam)
# covUSdaily = get_covUS(covfnam, CTP_US_COLNUM, CTP_US_RENAME)
# cov_USdaily = chg_cols(covUSdaily, CTP_US_RENAME)
usgraph(cd_us, 'C', get_startdate())
usgraph(cd_us, 'D', get_startdate())

state_dict['state_ts'] = {}
state_dict['state_ts'].fromkeys(state_dict['FIPS'].keys(), None)
for xstate in iter(States.index):
    # var which defined at top can be used to select states to show
    if xstate in st_fips:
        stdf = pdcovid.loc[pdcovid.fips==xstate]
        thispop: int = state_dict['2020Pop'][xstate]
        # we can change indexing to date from state for other operations
        stdf.set_index('date', drop=False, append=False, inplace=True)
        # add newcalc, newdeath, and seq cols, save updated state df to list
        stdf = calc_delta(stdf, thispop)
        state_dict['state_ts'][xstate] = stdf
        stategraph(stdf, 'C', get_startdate())
        # stategraph(stdf, 'CDL', get_startdate())