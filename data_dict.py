# encoding=utf-8
"""
data_dict contains collections that define:
    1. columns to import from csv's
    2. Name for columns paired with original column name from import
    3. Order of columns to enhance readability/productivity working with the data
"""

from typing import List, Dict, Set

CTP_ST_COLNUM: Set = set([0, 1, 5, 6, 8, 16, 19, 20, 22, 23, 24, 28, 30, 31])
# CTP_COL_NUMS: FrozenSet = frozenset(["0", "1", "5", "6", "8", "16", "19", "20", "22", "23", "24", "28", "30", "31"])
CTP_ST_RENAME = dict(
	{"date": "Date", "state": "State", "hospitalizedCurrently": "curHosp", "hospitalizedCumulative": "aggHosp",
	 "inIcuCumulative": "aggICU", "death": "aggDeaths", "totalTestsViral": "aggResults",
	 "positiveTestsViral": "aggPosTest", "positiveCasesViral": "aggVCases", "fips": "FIPS",
	 "positiveIncrease": "dVCases", "totalTestResultsIncrease": "dResults", "deathIncrease": "dDeaths",
	 "hospitalizedIncrease": "daggHosp"})
CTPD_PREF_ORDER: List = ['Date', 'State', 'FIPS', 'aggResults', 'dResults', 'aggPosTest', 'dPosTest', 'dailyPosRate',
                         'aggVCases', 'dVCases', 'curHosp', 'aggHosp', 'daggHosp', 'aggICU', 'daggICU', 'aggDeaths',
                         'dDeaths']

CTP_US_COLNUM: Set = set([0, 2, 5, 6, 7, 8, 13, 17, 19, 20, 22, 23])
CTP_US_RENAME: Dict = dict(
	{"date": 'Date', "positive": "aggCases", "hospitalizedCurrently": "curHosp", "hospitalizedCumulative": 'aggHosp',
	 "IcuCurrently": "curICU", "inIcuCumulative": "aggICU", "death": 'Deaths', "totalTestResults": "aggResults",
	 "deathIncrease": 'dDeaths', "hospitalizedIncrease": "dHosp", "positiveIncrease": "dPosTest",
	 "totalTestResultsIncrease": "dResults"})
CTPD_PREF_ORDER: List = ['Date', 'positive', 'aggResults', 'dResults', 'aggPosTest', 'dPosTest', 'dailyPosRate',
                         'aggVCases', 'dVCases', 'curHosp', 'aggHosp', 'daggHosp', 'aggICU', 'daggICU', 'aggDeaths',
                         'dDeaths']


# this is the raw US daily format for covtracking_USdaily.csv
# date,states,positive,negative,pending,hospitalizedCurrently,hospitalizedCumulative,inIcuCurrently,
# inIcuCumulative,onVentilatorCurrently,onVentilatorCumulative,recovered,dateChecked,death,hospitalized,
# lastModified,total,totalTestResults,posNeg,deathIncrease,hospitalizedIncrease,negativeIncrease,
# positiveIncrease,totalTestResultsIncrease,hash
