# encoding=utf-8
"""
uscovid imports and analyzes US covid19 cases and deaths.
Note: as I climb matplotlib learning curve I've realized it is best to work
within intended OO framework. Basic course: create a `.Figure` and one or more
`~matplotlib.axes.Axes` via `.pyplot.subplots`, then simply work
with instantiated classes of those Objects! this avoids a lot of messy code and
conflicts in debugging!
Roadmap:  I have extended covid-19 analysis in another app:
gmapsapi, github repo for that is gs_corona. TODO - merge that functionality
into this app.
"""
import datetime
import dateutil
import pandas as pd
import matplotlib.pyplot as plt
from dateutil.relativedelta import *

# txtprn = fg(255, 10, 10) + 'red text using 24bit colors.' + fg.rs

"""   this commented-out code is for color map mgmt - see plotly doc
cmapx = plt.cm.get_cmap('viridis')
cmapx_rgb = []
norm = plt.cm.colors.Normalize(vmin=0, vmax=255)
for i in range(0, 255):
    k = plt.cm.colors.colorConverter.to_rgb(viridis_cmap(norm(i)))
    viridis_rgb.append(k)
"""
# plt.style.use('fivethirtyeight')
pd.set_option("display.max_rows", 200)
pd.set_option("mode.chained_assignment", None)

def get_startdate():
    """ establishes the beginning of the interval to include in graphs
    :return: start date
    :rtype: datetime.date
    """
    xdt: datetime.date = datetime.datetime.now()
    xdt = xdt - dateutil.relativedelta.relativedelta(months=4)
    print("using %s as start date for plots" % (xdt.strftime('%B %d %y')))
    return xdt

def get_pops(filen: str):
    """ get_pops reads in projected 2020 pops for all states and U.S.
    """
    pops: pd.DataFrame = pd.read_csv(filen, header=0)
    pops.set_index('FIPS', drop=False, inplace=True)
    return pops

def valid8er(inp: str):
    if len(inp) >= 1:
        for i in range(0, len(inp)):
            if inp[i] in ['c', 'C', 'd', 'D']:
                # at least one cases or deaths option selected
                return 0
        return 'invalid option'
    else:
        return 'invalid option'

def getelapsed(dtin: pd.Series):
    """ takes a series of date strings and returns the number of elapsed days
    from the earliest to the last date
    """
    dmax = datetime.datetime.strptime(dtin.max(), '%Y-%m-%d')
    dmin = datetime.datetime.strptime(dtin.min(), '%Y-%m-%d')
    ddif: datetime.timedelta = dmax - dmin
    return ddif.days

def get_states(fnam: str):
    """create dataframe from case and death data by date for each state, this
    function populates the primary dataframe for simplecovid
    """
    pdfstate: pd.DataFrame = pd.read_csv(fnam, header=0, parse_dates=True)
    pdfstate.set_index(['state'], drop=False, inplace=True)
    pdfstate.astype({'cases': 'int32'}, copy=False).dtypes
    pdfstate.astype({'deaths': 'int32'}, copy=False).dtypes
    return pdfstate

def getus(fnam: str):
    """ getus reads the us-wide covid-19 cases and deaths data
    """
    uscovid = pd.read_csv(fnam, header=0, parse_dates=True)
    try:
        uscovid['newcases'] = [0 for x in list(range(len(uscovid.index)))]
        uscovid['newcases'] = uscovid.cases.diff()
        uscovid['newdeaths'] = [0 for x in list(range(len(uscovid.index)))]
        uscovid['newdeaths'] = uscovid.deaths.diff()
    except KeyError:
        print('looked beyond end of index function calcdelta')
    return uscovid

def usgraph(dfx: pd.DataFrame, option: str = 'CDL', start: datetime.date = None):
    """
    usgraph plots cases and deaths by day for the covid-19 outbreak
    :type option: str
    :param dfx: the dataframe used for graph
    :param option: string- 'c' aggreg cases, 'C' net new cases,
        'd' aggreg deaths, 'D' net new deaths
        'L' to plot on logarithmic scale
    :param start: bounds the plot data with a starting date
    :return: 0 if successful
    """
    vald8 = valid8er(option)
    if vald8!=0:
        exit(code=vald8)
    if start is None:
        # I default to 2nd week of March, when pandemic become public issue
        start = datetime.datetime.strptime("2020-03-01",'%Y-%m-%d')
    else:
        start = start + relativedelta(days=-1)
    dfx: pd.DataFrame = dfx.loc[dfx.date > start.strftime('%Y-%m-%d')]
    dasof = datetime.datetime.strptime(dfx.date.max(),'%Y-%m-%d')
    xx = dfx.date
    fig, ax = plt.subplots()  # Create a figure containing a single axes
    plt.rc('lines', linewidth=1)
    xdays: int = getelapsed(dfx.date)
    ax.set_xlim((1, xdays))
    ylbl = ''
    if 'L' in option:
        ax.set_yscale('log')
        ylbl = 'Logarithmic y-axis: '
    if 'c' in option:
        ax.plot(xx, dfx.cases, 'b', label='totalcases')
    if 'd' in option:
        ax.plot(xx, dfx.deaths, 'g', label='deaths')
    if 'C' in option:
        ax.plot(xx, dfx.newcases, 'b+', label='newcases')
        ax.plot(xx, dfx.newcases.rolling(window=7).mean(), 'b', label='new cases 7-day rolling')
    if 'D' in option:
        ax.plot(xx, dfx.newdeaths, 'g+', label='dailydeaths')
        ax.plot(xx, dfx.newdeaths.rolling(window=7).mean(), 'r', label='deaths/day 7-day rolling')

    plt.xlabel('days since first case')
    plt.ylabel(ylbl + 'number of people')
    plt.legend(loc="lower left")
    plt.title('U.S. Covid-19 trend from %s thru %s'
              % (start.strftime('%B %d %y'), dasof.strftime('%B %d %y')))
    plt.show()
    return 0

def calc_delta(pdf: pd.DataFrame, stpop: int=0):
    """ calc_delta is passed a pd.DataFrame for a state and indexed on Date.  derived fields added:
        a.  daily new cases and deaths
        b.  cases and deaths per 100k population
        c.  count of elapsed days since start of outbreak
    :param pdf: the master states DataFrame passed to this function
    :param stpop: population for this state
    :return pdf: a DataFrame with updated state data
    """
    # get integer num for existing and to-be-added columns:
    dcol: int = pdf.columns.get_loc('deaths')
    ccol: int = pdf.columns.get_loc('cases')
    pdf['cases'].astype('int')
    pdf['deaths'].astype('int')
    first = pdf.index.to_series().min()
    try:
        pdf['newcases'] = pdf.cases.diff()
        nccol = pdf.columns.get_loc('newcases')
        pdf.iat[0, nccol] = pdf.iloc[0, ccol]

        pdf['newdeaths'] = pdf.deaths.diff()
        ndcol = pdf.columns.get_loc('newdeaths')
        pdf.iat[0, ndcol] = pdf.iloc[0, dcol]
    except KeyError:
        print('looked beyond end of index function calcdelta')
        return None
    pdf['newcases'].astype('int')
    pdf['newdeaths'].astype('int')
    pdf['casesper100k'] = [0 for x in list(range(len(pdf.index)))]
    pdf['deathsper100k'] = [0 for x in list(range(len(pdf.index)))]
    pdf['casesper100k'].astype('float')
    pdf['deathsper100k'].astype('float')
    pdf['casesper100k'] = pdf['cases']/stpop
    pdf['deathsper100k'] = pdf['deaths']/stpop
    return pdf

def stategraph(stdf: pd.DataFrame, option: str, start: datetime.date= None):
    """
    stategraph plots covid-19 cases and deaths for a state
    :param stdf: DataFrame with date, state, and oneof: cases-deaths-newdeaths
    :type stdf: pd.DataFrame
    :param option: 'c' for aggreg cases, 'd' for aggreg deaths,
        'C' for daily cases, 'D' for daily deaths,
        'L' for logscale
    :type option: str
    :param start: the beginning date for the timespan for the plot
    :type start: datetime.date
    :return: zero if no error
    """
    vald8 = valid8er(option)
    if vald8!=0:
        exit(code=vald8)
    if start is None:
        start: datetime.date = datetime.datetime.strptime("2020-03-01",'%Y-%m-%d')
    else:
        start: datetime.date = start + relativedelta(days=-1)
    stdf = stdf.loc[stdf.date > start.strftime('%Y-%m-%d')]
    dthru = datetime.datetime.strptime(str(stdf.date.max()), '%Y-%m-%d')
    xx = stdf.date
    scol: int = stdf.columns.get_loc('state')
    # get name of this stateg
    st: str = stdf.iloc[0, scol]
    xlbl: str = ''
    fig, ax = plt.subplots()  # Create a figure containing a single axes.
    plt.rc('lines', linewidth=1)
    # calculate elapsed days and set range for x axis
    xdays = getelapsed(stdf.date)
    ax.set_xlim((1, xdays))
    if 'L' in option:
        # use a log scale when showing combined cases-deaths
        ax.set_yscale('log')
        xlbl = '[log scale], '
    if 'c' in option:
        ax.plot(xx, stdf.cases, 'b+', label='totalcases')
        xlbl = xlbl + 'aggr cases in blue'
    elif 'C' in option:
        ax.plot(xx, stdf.newcases, 'b+', label='dailycases', linewidth=1)
        xlbl = xlbl + 'daily cases in blue'
        Croll7 = stdf.newcases.rolling(window=7).mean()
        ax.plot(xx, Croll7, 'm', label='7-day roll avg. cases')
    else:
        print("Cases will not be shown in State graph")

    if 'd' in option:
        ax.plot(xx, stdf.deaths, 'g*', label='totaldeaths')
        xlbl = xlbl + ', aggr deaths in green'
    elif 'D' in option:
        ax.plot(xx, stdf.newdeaths, 'g*', label='dailydeaths', linewidth=1)
        xlbl = xlbl + ', daily deaths in green'
        Droll7 = stdf.newdeaths.rolling(window=7).mean()
        ax.plot(xx, Droll7, 'm', label='7-day roll avg. deaths')
    else:
        print("Deaths will not be shown in State graph")

    plt.xlabel('elapsed days')
    plt.ylabel(xlbl)
    plt.xticks([1, 30, 60, 90, xdays])  # x-axis label distribution
    plt.legend(loc="upper left")
    plt.title('%s Covid-19 trend, from %s through %s'
              % (st, start.strftime('%B %d %y'), dthru.strftime('%B %d %y')))
    plt.show()
    return 0
