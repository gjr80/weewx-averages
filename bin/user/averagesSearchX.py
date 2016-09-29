#
# Copyright (c) 2015-2016 Gary Roderick <gjroderick(at)gmail.com>
#
# Released under GNU General Public License, Version 3, 29 June 2007.
# Refer to the enclosed License file for your full rights.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# Search List Extension class to support generation of JSON data file for use
# by Highcharts to plot monthly maximum, minimum and mean termperature and
# rainfall observations.
#
# Version: 0.5.0                                   Date: 25 September 2016
#
# Revision History
#  25 September 2016
#      v0.5.0   - now packaged as a weewx extension
#               - reworked the SLE class:
#                   - took get_first_day() method out of the SLE class
#                   - consolidated SLE getMonthAveragesHighsLows() method into
#                     get_extension_list() method
#                   - reworked algorithm to calculate means, now use BoM
#                     definitions. Refer class comments for details.
#                   - no longer use partial months at start and end of archive
#                     for anything, only use complete archive months. Note, any
#                     partial months after the first complete month and before
#                     the last complete month are still 'included'.
#  10 May 2016
#      v0.4.0   - no change, version number upgrade only
#  April 2016
#      v0.3.0   - no change, version number upgrade only
#  5 March 2016
#      v0.2.2   - fixed bug in that entire months with no records caused
#                monthAverages to fail
#  21 July 2015
#      v0.2.1   - reworked comments
#               - remove old redundant code
#  19 March 2015
#      v0.2.0   - no change, version number upgrade only
#  22 February 2015
#      v0.1.0   - initial implementation
#
import datetime
import json
import syslog
import time
import weewx

from datetime import date
from weewx.cheetahgenerator import SearchList
from weewx.units import getStandardUnitType, ValueTuple
from weeutil.weeutil import genMonthSpans

def logmsg(level, msg):
    syslog.syslog(level, 'averagesSearchX: %s' % msg)

def logdbg(msg):
    logmsg(syslog.LOG_DEBUG, msg)

def logdbg2(msg):
    if weewx.debug >= 2:
        logmsg(syslog.LOG_DEBUG, msg)

def loginf(msg):
    logmsg(syslog.LOG_INFO, msg)

def logerr(msg):
    logmsg(syslog.LOG_ERR, msg)

def get_first_day(dt, d_years=0, d_months=0):
    """ Return date object that is the 1st of month containing a given datetime
        object.

        Returns a date object for the 1st day on the month containing dt. dt is
        first offset by D-years and d_months. Positive offset steps forward in
        time, negative offset steps back in time.

        Parameters:
            dt:       datetime object for which the 1st of the month is
                      required.
            d_years:  Number of years to be added to dt before calculating 1st
                      of the month.
            d_months: Number of months to be added to dt before calculating 1st
                      of the month.

        Returns a date object for the 1st of the required month.
    """

    # Get year number and month number applying offset as required
    _y, _m = dt.year + d_years, dt.month + d_months
    # Calculate actual month number taking into account EOY rollover
    _a, _m = divmod(_m-1, 12)
    # Calculate and return date object
    return date(_y+_a, _m+1, 1)

def roundNone(value, places):
    """ Round value to 'places' places but also permit a value of None. """

    if value is not None:
        try:
            value = round(value, places)
        except Exception, e:
            value = None
    return value

class monthAverages(SearchList):

    def __init__(self, generator):
        SearchList.__init__(self, generator)

    def get_extension_list(self, timespan, db_lookup):
        """ Returns json format month avg/max/min stats for use by HighCharts.

            The following stats are calculated for each month (jan ... dec):
                - average rainfall
                - mean temperature
                - maximum temperature
                - mean maximum temperature
                - minimum temperature
                - mean minimum temperature

            The following definitions are used:

            Average rainfall. The average rainfall for each month, calculated
            over all years of record.

            Maximum temperature. The highest temperature, for each month,
            observed at the site over all years of record.

            Mean maximum temperature. The average daily maximum temperature,
            for each month, calculated over all years of record.

            Minimum temperature. The lowest temperature, for each month,
            observed at the site over all years of record.

            Mean minimum temperature. The average daily minimum temperature,
            for each month, calculated over all years of record.

            Mean temperature. The mean of the daily mean temperature, for each
            month, observed at the site over all years of record. The daily
            mean temperature is defined as the sum of the daily maximum
            temperature and the daily minimum temperature divided by two.

            References:

            'Average annual & monthly maximum, minimum, & mean temperature' -
                http://www.bom.gov.au/jsp/ncc/climate_averages/temperature/index.jsp
            'Climate statistics for Australian locations' -
                http://www.bom.gov.au/climate/cdo/about/definitionstemp.shtml

            Results are calculated using daily summary data from daily summary
            tables. Aggregates are calculated as follows:
                - average rainfall. Calculate the total rainfall for each Jan,
                  Feb...Dec then calculate a simple average by dividing each
                  month total by the number of years of those months in our
                  data.
                - mean temp. Sum the mean temperature for each Jan, Feb...Dec
                  then calculate s simple average by dividing each month total
                  by the number of years of those months in our data.
                - maximum and minimum temp. Maximum and minimum tempeature
                  obeserved in each Jan, Feb...Dec.
                - mean maximum temp. Sum the mean maximum temp for each Jan,
                  Feb...Dec then calculate s simple average by dividing each
                  month total by the number of years of those months in our
                  data.
                - mean minimum temp. Sum the mean minimum temp for each Jan,
                  Feb...Dec then calculate s simple average by dividing each
                  month total by the number of years of those months in our
                  data.

            Partial months of data at the start and end of the archive are
            ignored. Incomplete or partial months between the first and last
            months of data are included in the calculations.

            Returned values are JSON strings representing results for Jan, Feb
            thru Dec. Months that have no data are returned as Null. Unit
            conversion and rounding is applied to the JSON results as per
            skin.conf/weewx.conf override settings.

            Returns:
                monthRainAvgjson:        12 way array containing month avg 
                                         rainfall
                monthTempMeanjson:       12 way array containing month mean temp
                monthTempMaxjson:        12 way array containing month max temp
                monthTempMeanMinMaxjson: 12 way array containing 2 way array 
                                         month (mean min, mean max) temp 
                monthTempMinjson:        12 way array containing month min temp

            Parameters:
                timespan: An instance of weeutil.weeutil.TimeSpan. This will
                          hold the start and stop times of the domain of
                          valid times.
                db_lookup: An instance of weewx.archive.Archive
        """

        t1 = time.time()

        # Initialise those things we need to get going
        # Get archive interval
        current_rec = db_lookup().getRecord(timespan.stop)
        _interval = current_rec['interval']
        # Get our UoMs and Groups
        (rainUnit, rainGroup) = getStandardUnitType(current_rec['usUnits'],
                                                    'rain')
        (tempUnit, tempGroup) = getStandardUnitType(current_rec['usUnits'],
                                                    'outTemp')
        # Since we can't use ValueHelpers for rounding of a 'vector' vt get
        # the number of decimal places to use for rounding temp and rain
        tempRound = int(self.generator.skin_dict['Units']['StringFormats'].get(tempGroup, "1f")[-2])
        rainRound = int(self.generator.skin_dict['Units']['StringFormats'].get(rainGroup, "1f")[-2])
        # Set up ValueTuples to hold our results, but in this case the 'value'
        # part of the vt will be a 12 element list ie (jan ... dec). We already
        # know the units but not the values so initialise each months value to
        # None.
        mRainAvg_vt = ValueTuple([None for x in range(12)], rainUnit, rainGroup)
        mTempMean_vt = ValueTuple([None for x in range(12)], tempUnit, tempGroup)
        mTempMax_vt = ValueTuple([None for x in range(12)], tempUnit, tempGroup)
        mTempMeanMax_vt = ValueTuple([None for x in range(12)], tempUnit, tempGroup)
        mTempMin_vt = ValueTuple([None for x in range(12)], tempUnit, tempGroup)
        mTempMeanMin_vt = ValueTuple([None for x in range(12)], tempUnit, tempGroup)
        # Set up some 2D lists to hold our month running totals and number of
        # years so we can calculate an average
        # mXxxxBin[0..11][0..1] - [0..11] - holds data for jan .. dec
        #                       - [0..1]  - [0] holds running total for Xxxx
        #                                 - [1] holds number of years of data
        #                                       added to running total
        mRainBin = [[0 for x in range(2)] for x in range(12)]
        mTempMeanMaxBin = [[None for x in range(2)] for x in range(12)]
        mTempMeanMinBin = [[None for x in range(2)] for x in range(12)]
        mTempMeanBin = [[None for x in range(2)] for x in range(12)]
        # End of initialisation

        # Get timestamp, month and year for our first (earliest) record
        _start_ts = db_lookup().firstGoodStamp()
        _start_month = date.fromtimestamp(_start_ts).month
        _start_year = date.fromtimestamp(_start_ts).year
        # Get timestamp, month and year for our last (most recent) record
        _end_ts = timespan.stop
        _end_month = date.fromtimestamp(_end_ts).month
        _end_year = date.fromtimestamp(_end_ts).year
        # Loop through each month timespan between our start and end timestamps
        for m_tspan in genMonthSpans(_start_ts, _end_ts):
            # Skip any partial months at the start or end of our data
            if m_tspan.start + _interval * 60 < _start_ts or m_tspan.stop > _end_ts:
                # our span includes only part of a month
                continue
            # Work out the month bin number
            _bin = datetime.datetime.fromtimestamp(m_tspan.start).month - 1
            # Get the total rain for the month concerned
            _rainSum_vt = db_lookup().getAggregate(m_tspan,
                                                   'rain',
                                                   'sum')
            # Get the max temp for the month concerned
            _tempMax_vt = db_lookup().getAggregate(m_tspan,
                                                   'outTemp',
                                                   'max')
            # Get the avg max temp for the month concerned
            _tempMeanMax_vt = db_lookup().getAggregate(m_tspan,
                                                      'outTemp',
                                                      'meanmax')
            # Get the min temp for the month concerned
            _tempMin_vt = db_lookup().getAggregate(m_tspan,
                                                   'outTemp',
                                                   'min')
            # Get the avg min temp for the month concerned
            _tempMeanMin_vt = db_lookup().getAggregate(m_tspan,
                                                      'outTemp',
                                                      'meanmin')
            # We have the raw data now update our bins for avgs and results for
            # max/min

            # Avg rainfall
            # Add the month rainfall to the bin and increment the year counter.
            # Be careful of None values
            if _rainSum_vt.value is not None:
                mRainBin[_bin][0] += _rainSum_vt.value
                mRainBin[_bin][1] += 1

            # Mean temp
            # If our bin already has data for this month then add the daily mean
            # and increment the year counter. Otherwise set the value for this
            # bin to the daily mean and set the year counter to 1
            if _tempMeanMax_vt.value is not None and _tempMeanMin_vt.value is not None:
                if mTempMeanBin[_bin][0]:
                    mTempMeanBin[_bin][0] += (_tempMeanMax_vt.value + _tempMeanMin_vt.value)/2
                    mTempMeanBin[_bin][1] += 1
                else:
                    mTempMeanBin[_bin][0] = (_tempMeanMax_vt.value + _tempMeanMin_vt.value)/2
                    mTempMeanBin[_bin][1] = 1

            # Max temp
            # If the current value is greater than our max to date for this
            # month then we have a new max
            if _tempMax_vt.value > mTempMax_vt[0][_bin]:
                mTempMax_vt[0][_bin] = _tempMax_vt.value

            # Mean max temp
            # If our bin already has data for this month then add the daily
            # mean max and increment the year counter. Otherwise set the value
            # for this bin to the daily mean max and set the year counter to 1
            if _tempMeanMax_vt.value is not None:
                if mTempMeanMaxBin[_bin][0]:
                    mTempMeanMaxBin[_bin][0] += _tempMeanMax_vt.value
                    mTempMeanMaxBin[_bin][1] += 1
                else:
                    mTempMeanMaxBin[_bin][0] = _tempMeanMax_vt.value
                    mTempMeanMaxBin[_bin][1] = 1

            # Min temp
            # If the current value is less than our min to date for this month
            # then we have a new min. Watch out for None though.
            if mTempMin_vt[0][_bin] is None or (_tempMin_vt.value is not None and _tempMin_vt.value < mTempMin_vt[0][_bin]):
                mTempMin_vt[0][_bin] = _tempMin_vt.value

            # Mean min temp
            # If our bin already has data for this month then add the daily
            # mean min and increment the year counter. Otherwise set the value
            # for this bin to the daily mean min and set the year counter to 1
            if _tempMeanMin_vt.value is not None:
                if mTempMeanMinBin[_bin][0]:
                    mTempMeanMinBin[_bin][0] += _tempMeanMin_vt.value
                    mTempMeanMinBin[_bin][1] += 1
                else:
                    mTempMeanMinBin[_bin][0] = _tempMeanMin_vt.value
                    mTempMeanMinBin[_bin][1] = 1

        # We have pre-processed all the raw data now calculate the required
        # averages for each month and put them in their 'vector' vt.
        for _mNum in range (12):
            # Avg rainfall
            # If we have 1 or more years of data then calc a simple average
            if mRainBin[_mNum][1] > 0:
                mRainAvg_vt[0][_mNum] = mRainBin[_mNum][0] / mRainBin[_mNum][1]
            # Otherwise we have no years of data so set our average to None
            else:
                mRainAvg_vt[0][_mNum] = None

            # Mean temp
            # If we have a total > 0 then calc a simple average
            if mTempMeanBin[_mNum][1] > 0:
                mTempMean_vt[0][_mNum] = mTempMeanBin[_mNum][0] / mTempMeanBin[_mNum][1]
            # Otherwise we have no years of data so set our average to None
            else:
                mTempMean_vt[0][_mNum] = None

            # Mean max temp
            # If we have a total > 0 then calc a simple average
            if mTempMeanMaxBin[_mNum][1] > 0:
                mTempMeanMax_vt[0][_mNum] = mTempMeanMaxBin[_mNum][0] / mTempMeanMaxBin[_mNum][1]
            # Otherwise we have no years of data so set our average to None
            else:
                mTempMeanMax_vt[0][_mNum] = None

            # Mean min temp
            # If we have a total > 0 then calc a simple average
            if mTempMeanMinBin[_mNum][1] > 0:
                mTempMeanMin_vt[0][_mNum] = mTempMeanMinBin[_mNum][0] / mTempMeanMinBin[_mNum][1]
            # Otherwise we have no years of data so set our average to None
            else:
                mTempMeanMin_vt[0][_mNum] = None


        # Convert to the required units and extract the converted values into
        # a vector
        mRainAvg_vec = self.generator.converter.convert(mRainAvg_vt).value
        mTempMean_vec = self.generator.converter.convert(mTempMean_vt).value
        mTempMax_vec = self.generator.converter.convert(mTempMax_vt).value
        mTempMeanMax_vec = self.generator.converter.convert(mTempMeanMax_vt).value
        mTempMin_vec = self.generator.converter.convert(mTempMin_vt).value
        mTempMeanMin_vec = self.generator.converter.convert(mTempMeanMin_vt).value

        # Round the values in our vectors
        mRainAvg_vec =  [roundNone(x, rainRound) for x in mRainAvg_vec]
        mTempMean_vec =  [roundNone(x, tempRound) for x in mTempMean_vec]
        mTempMax_vec =  [roundNone(x, tempRound) for x in mTempMax_vec]
        mTempMeanMax_vec =  [roundNone(x, tempRound) for x in mTempMeanMax_vec]
        mTempMin_vec =  [roundNone(x, tempRound) for x in mTempMin_vec]
        mTempMeanMin_vec =  [roundNone(x, tempRound) for x in mTempMeanMin_vec]

        # Format our vectors in json format
        mRainAvg_json = json.dumps(mRainAvg_vec)
        mTempMean_json = json.dumps(mTempMean_vec)
        mTempMax_json = json.dumps(mTempMax_vec)
        # monthTempMeanMinMax is vector of 2 way tuples, each tuple is (min, max)
        mTempMeanMinMax_json = json.dumps(zip(mTempMeanMin_vec,
                                              mTempMeanMax_vec))
        mTempMin_json = json.dumps(mTempMin_vec)

        # Create a dictionary with the tag names (keys) we want to use
        _result = {'monthRainAvgjson'        : mRainAvg_json,
                   'monthTempMeanjson'       : mTempMean_json,
                   'monthTempMaxjson'        : mTempMax_json,
                   'monthTempMeanMinMaxjson' : mTempMeanMinMax_json,
                   'monthTempMinjson'        : mTempMin_json}

        t2 = time.time()
        logdbg2("monthAverages SLE executed in %0.3f seconds" % (t2 - t1))

        return [_result]