# utf-8
"""
uscovid imports and analyzes US covid19 cases and deaths
"""
import pandas as pd
from pylab import *


pd.set_option("display.max_rows", 200)
pd.set_option("mode.chained_assignment", None)
# os module fx join-  builds fq (fully qualified) dir+filename

def get_states(fnam: str):
    """create dataframe from case and death data by date for each state, this
    function populates the primary dataframe for simplecovid
    """
    pdfstate = pd.read_csv(fnam, header=0, parse_dates=True)
    pdfstate.set_index(['state'], drop=False, inplace=True)
    pdfstate.astype({'cases': 'int32'}).dtypes
    pdfstate.astype({'deaths': 'int32'}).dtypes
    return pdfstate

def getus(fnam: str):
    """ getus reads the us-wide covid-19 cases and deaths data
    """
    uscovid = pd.read_csv(fnam, header=0, parse_dates=True)
    # pdcovid.date.astype(pd.datetime)
    uscovid.set_index(['date'])
    return uscovid

def usgraph(dfx: pd.DataFrame, option: str, gtitle: str):
    """
    usgraph plots cases and deaths by day for the covid-19 outbreak
    :param dfx: the dataframe used for graph
    :param option: string with c to include cases, d to include deaths, L to plot on
    logarithmic scale
    :param gtitle: text title for the graph
    :return: 0 if successful
    """
   # stg = pd.DataFrame(tupag[7][1])
    x: list = dfx.date
    fig, ax = plt.subplots()  # Create a figure containing a single axes.
    if 'L' in option:
        ax.set_yscale('log')
    if 'c' in option:
        ax.plot(x, dfx.cases, 'b')
    if 'd' in option:
        ax.plot(x, dfx.deaths, 'g')
    plt.xlabel('days since first case')
    plt.ylabel('number of people')
    plt.title('Covid19: %s' %(gtitle))
    plt.show()
    stg = None
    return 0

def calc_delta(pdf: pd.DataFrame):
    """ calc_delta calculates change in cases and deaths by state and adds
    a field for each in DataFrame. calc_delta adds count of elapsed days
    EXPECTS a hierarchically indexed df on 1.State and 2.Date
    note: .loc and .iat use python-standard zero-based indices
    :param pdf: the master states DataFrame passed to this function
    """
    # get integer num for existing and to-be-added columns:
    dcol: int = pdf.columns.get_loc('deaths')
    ccol: int = pdf.columns.get_loc('cases')
    cols: int = len(pdf.columns)
    nccol: int = cols
    ndcol: int = nccol + 1
    seqcol: int = ndcol + 1
    try:
        pdf['newcases'] = pdf.cases.diff()
        pdf.iloc[0, nccol] = pdf.iloc[0, ccol]
        pdf['newdeaths'] = pdf.deaths.diff()
        pdf.iloc[0, ndcol] = pdf.iloc[0, dcol]
    except KeyError:
        print('looked beyond end of index function calcdelta')
    pdf['seq'] = None
    for i in range(0, len(pdf)):
        pdf.iloc[i, seqcol] = (i + 1)
    return pdf

def stategraph(stdf: pd.DataFrame, option: str):
    """
    stategraph plots covid-19 cases and deaths for a state
    :param stdf: DataFrame with date, state, and oneof: cases-deaths-newdeaths
    :param option: 'c' for aggreg cases, 'd' for aggreg deaths,
        'C' for daily cases, 'N' for daily deaths,
        'L' for logscale

    :return: zero if no error
    """
    # get a list of dates or sequence to plot
    x: list = stdf.seq
    scol: int = stdf.columns.get_loc('state')
    # get name of this state
    st: str = stdf.iloc[0, scol]
    xlbl: str = ''
    fig, ax = plt.subplots()  # Create a figure containing a single axes.
    if 'L' in option:
        # use a log scale when showing combined cases-deaths
        ax.set_yscale('log')
        xlbl = '[log scale], '
    if 'c' in option:
        ax.plot(x, stdf.cases, 'b')
        xlbl = xlbl + 'aggr cases in blue '
    if 'C' in option:
        ax.plot(x, stdf.newcases, 'b')
        xlbl = xlbl + 'daily cases in blue '
    if 'd' in option:
        ax.plot(x, stdf.deaths, 'g')
        xlbl = xlbl + 'aggr deaths in green'
    if 'N' in option:
        ax.plot(x, stdf.newdeaths, 'g')
        xlbl = xlbl + 'daily deaths in green'

    plt.xlabel('elapsed days')
    plt.ylabel(xlbl)
    plt.title('%s Covid-19 trends since start of outbreak' %(st))
    plt.show()
    stg = None
    return 0
