# encoding=utf-8
"""
simplecovid main project file to display case and death stats in a plot
"""

from uscovid import *
from otherdata import *

pd.set_option("display.date_yearfirst", True)

# Variable Definition- concat relative path with data file names
which: set = {'Georgia', 'Wisconsin', 'Michigan', 'Texas'}
datadir: str = 'rawdata'
stnam: str = os.path.join(datadir, "us-states.csv")
usfnam: str = os.path.join(datadir, "us.csv")
ldgfile: str = os.path.join(datadir, 'USdeaths leading 2015 to 2018.csv')
popfile: str = os.path.join(datadir, 'StatePopFIPS2020.csv')


# get state data and calculate incrementals, get us data
cd_us = getus(usfnam)
usgraph(cd_us, 'cdL', 'United States')
pdcovid: pd.DataFrame = get_states(stnam)

# ldg_us has CoD, #deaths, population, fatalities/100k, and
ldg_us = get_leading(ldgfile)
# States has columns state, FIPS, 2020Pop (population)
States: pd.DataFrame = get_pops(popfile)
# stdict is keyed on 2 digit state FIPS, value is state dataframe
stdict: dict = {}

# run state plots, limit with var which defined at top
for xstate in iter(States.state):
    if xstate in which:
        stdf = pdcovid.loc[pdcovid.state == xstate]
        # we can change indexing to date from state for other operations
        stdf.set_index('date', drop=False, append=False, inplace=True)
        # add newcalc, newdeath, and seq cols, save updated state dataset
        # to our statelist (no sense in trying to merge back to main df
        stdf = calc_delta(stdf)
        stdict[stdf.iat[0, 2]] = stdf
        stategraph(stdf, 'N')
