"""
averagesSearchX.py

A WeeWX Search List Extension to used to calculate monthly maximum, minimum and
mean temperature and rainfall observations.

Copyright (c) 2015-2020 Gary Roderick               gjroderick<at>gmail.com

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see http://www.gnu.org/licenses/.

Version: 1.0.0                                   Date: 25 May 2020

Revision History
    25 May 2020         v1.0.0
        - now WeeWX 3 and WeeWX 4 (python 2 or 3) compatible
        - renamed search list file and search list class
    30 September 2016   v0.5.0
        - now packaged as a weewx extension
        - reworked the SLE class:
            - took get_first_day() method out of the SLE class
            - consolidated SLE getMonthAveragesHighsLows() method into
              get_extension_list() method
            - reworked algorithm to calculate means, now use BoM definitions. 
              Refer class comments for details.
            - no longer use partial months at start and end of archive for
              anything, only use complete archive months. Note, any partial 
              months after the first complete month and before the last complete
              month are still 'included'.
    10 May 2016         v0.4.0
       - no change, version number upgrade only
    April 2016          v0.3.0
       - no change, version number upgrade only
    5 March 2016        v0.2.2
       - fixed bug in that entire months with no records caused MonthAverages to
         fail
    21 July 2015        v0.2.1
       - reworked comments
       - remove old redundant code
    19 March 2015       v0.2.0
       - no change, version number upgrade only
    22 February 2015    v0.1.0
       - initial implementation
"""
import datetime
import json
import time
import weewx

from datetime import date
from weewx.cheetahgenerator import SearchList
from weewx.units import getStandardUnitType, ValueTuple
from weeutil.weeutil import genMonthSpans

# import/setup logging, WeeWX v3 is syslog based but WeeWX v4 is logging based,
# try v4 logging and if it fails use v3 logging
try:
    # WeeWX4 logging
    import logging
    log = logging.getLogger(__name__)

    def logdbg(msg):
        log.debug(msg)

except ImportError:
    # WeeWX legacy (v3) logging via syslog
    import syslog

    def logmsg(level, msg):
        syslog.syslog(level, 'averagessearchlist: %s' % msg)

    def logdbg(msg):
        logmsg(syslog.LOG_DEBUG, msg)


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

    # get year number and month number applying offset as required
    _y, _m = dt.year + d_years, dt.month + d_months
    # calculate actual month number taking into account EOY rollover
    _a, _m = divmod(_m-1, 12)
    # calculate and return date object
    return date(_y+_a, _m+1, 1)


def round_none(value, places):
    """ Round value to 'places' places but also permit a value of None. """

    if value is not None:
        try:
            value = round(value, places)
        except TypeError:
            value = None
    return value


class MonthAverages(SearchList):

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

        # initialise those things we need to get going
        # get archive interval
        current_rec = db_lookup().getRecord(timespan.stop)
        _interval = current_rec['interval']
        # get our UoMs and Groups
        (rain_unit, rain_group) = getStandardUnitType(current_rec['usUnits'],
                                                      'rain')
        (temp_unit, temp_group) = getStandardUnitType(current_rec['usUnits'],
                                                      'outTemp')
        # since we can't use ValueHelpers for rounding of a 'vector' vt get
        # the number of decimal places to use for rounding temp and rain
        temp_round = int(self.generator.skin_dict['Units']['StringFormats'].get(temp_group, "1f")[-2])
        rain_round = int(self.generator.skin_dict['Units']['StringFormats'].get(rain_group, "1f")[-2])
        # Set up ValueTuples to hold our results, but in this case the 'value'
        # part of the vt will be a 12 element list ie (jan ... dec). We already
        # know the units but not the values so initialise each months value to
        # None.
        m_rain_avg_vt = ValueTuple([None for x in range(12)], rain_unit, rain_group)
        m_temp_mean_vt = ValueTuple([None for x in range(12)], temp_unit, temp_group)
        m_temp_max_vt = ValueTuple([None for x in range(12)], temp_unit, temp_group)
        m_temp_mean_max_vt = ValueTuple([None for x in range(12)], temp_unit, temp_group)
        m_temp_min_vt = ValueTuple([None for x in range(12)], temp_unit, temp_group)
        m_temp_mean_min_vt = ValueTuple([None for x in range(12)], temp_unit, temp_group)
        # set up some 2D lists to hold our month running totals and number of
        # years so we can calculate an average
        # m_xxxx_bin[0..11][0..1] - [0..11] - holds data for jan .. dec
        #                         - [0..1]  - [0] holds running total for Xxxx
        #                                   - [1] holds number of years of data
        #                                         added to running total
        m_rain_bin = [[0 for x in range(2)] for x in range(12)]
        m_temp_mean_max_bin = [[None for x in range(2)] for x in range(12)]
        m_temp_mean_min_bin = [[None for x in range(2)] for x in range(12)]
        m_temp_mean_bin = [[None for x in range(2)] for x in range(12)]
        # end of initialisation

        # get timestamp, month and year for our first (earliest) record
        _start_ts = db_lookup().firstGoodStamp()
        _start_month = date.fromtimestamp(_start_ts).month
        _start_year = date.fromtimestamp(_start_ts).year
        # get timestamp, month and year for our last (most recent) record
        _end_ts = timespan.stop
        _end_month = date.fromtimestamp(_end_ts).month
        _end_year = date.fromtimestamp(_end_ts).year
        # loop through each month timespan between our start and end timestamps
        for m_tspan in genMonthSpans(_start_ts, _end_ts):
            # skip any partial months at the start or end of our data
            if m_tspan.start + _interval * 60 < _start_ts or m_tspan.stop > _end_ts:
                # our span includes only part of a month
                continue
            # work out the month bin number
            _bin = datetime.datetime.fromtimestamp(m_tspan.start).month - 1
            # get the total rain for the month concerned
            _rain_sum_vt = db_lookup().getAggregate(m_tspan,
                                                    'rain',
                                                    'sum')
            # get the max temp for the month concerned
            _temp_max_vt = db_lookup().getAggregate(m_tspan,
                                                    'outTemp',
                                                    'max')
            # get the avg max temp for the month concerned
            _temp_mean_max_vt = db_lookup().getAggregate(m_tspan,
                                                         'outTemp',
                                                         'meanmax')
            # get the min temp for the month concerned
            _temp_min_vt = db_lookup().getAggregate(m_tspan,
                                                    'outTemp',
                                                    'min')
            # get the avg min temp for the month concerned
            _temp_mean_min_vt = db_lookup().getAggregate(m_tspan,
                                                         'outTemp',
                                                         'meanmin')
            # we have the raw data now update our bins for avgs and results for
            # max/min

            # avg rainfall
            # Add the month rainfall to the bin and increment the year counter.
            # Be careful of None values
            if _rain_sum_vt.value is not None:
                m_rain_bin[_bin][0] += _rain_sum_vt.value
                m_rain_bin[_bin][1] += 1

            # mean temp
            # If our bin already has data for this month then add the daily mean
            # and increment the year counter. Otherwise set the value for this
            # bin to the daily mean and set the year counter to 1
            if _temp_mean_max_vt.value is not None and _temp_mean_min_vt.value is not None:
                if m_temp_mean_bin[_bin][0]:
                    m_temp_mean_bin[_bin][0] += (_temp_mean_max_vt.value + _temp_mean_min_vt.value)/2
                    m_temp_mean_bin[_bin][1] += 1
                else:
                    m_temp_mean_bin[_bin][0] = (_temp_mean_max_vt.value + _temp_mean_min_vt.value)/2
                    m_temp_mean_bin[_bin][1] = 1

            # max temp
            # if the current value is greater than our max to date for this
            # month then we have a new max
            if m_temp_max_vt[0][_bin] is None or _temp_max_vt.value > m_temp_max_vt[0][_bin]:
                m_temp_max_vt[0][_bin] = _temp_max_vt.value

            # mean max temp
            # If our bin already has data for this month then add the daily
            # mean max and increment the year counter. Otherwise set the value
            # for this bin to the daily mean max and set the year counter to 1
            if _temp_mean_max_vt.value is not None:
                if m_temp_mean_max_bin[_bin][0]:
                    m_temp_mean_max_bin[_bin][0] += _temp_mean_max_vt.value
                    m_temp_mean_max_bin[_bin][1] += 1
                else:
                    m_temp_mean_max_bin[_bin][0] = _temp_mean_max_vt.value
                    m_temp_mean_max_bin[_bin][1] = 1

            # min temp
            # If the current value is less than our min to date for this month
            # then we have a new min. Watch out for None though.
            if m_temp_min_vt[0][_bin] is None or (_temp_min_vt.value is not None and _temp_min_vt.value < m_temp_min_vt[0][_bin]):
                m_temp_min_vt[0][_bin] = _temp_min_vt.value

            # mean min temp
            # If our bin already has data for this month then add the daily
            # mean min and increment the year counter. Otherwise set the value
            # for this bin to the daily mean min and set the year counter to 1
            if _temp_mean_min_vt.value is not None:
                if m_temp_mean_min_bin[_bin][0]:
                    m_temp_mean_min_bin[_bin][0] += _temp_mean_min_vt.value
                    m_temp_mean_min_bin[_bin][1] += 1
                else:
                    m_temp_mean_min_bin[_bin][0] = _temp_mean_min_vt.value
                    m_temp_mean_min_bin[_bin][1] = 1

        # we have pre-processed all the raw data now calculate the required
        # averages for each month and put them in their 'vector' vt.
        for _m_num in range(12):
            # avg rainfall
            # if we have 1 or more years of data then calc a simple average
            if m_rain_bin[_m_num][1] > 0:
                m_rain_avg_vt[0][_m_num] = m_rain_bin[_m_num][0] / m_rain_bin[_m_num][1]
            # otherwise we have no years of data so set our average to None
            else:
                m_rain_avg_vt[0][_m_num] = None

            # mean temp
            # if we have a total > 0 then calc a simple average
            if m_temp_mean_bin[_m_num][1] > 0:
                m_temp_mean_vt[0][_m_num] = m_temp_mean_bin[_m_num][0] / m_temp_mean_bin[_m_num][1]
            # otherwise we have no years of data so set our average to None
            else:
                m_temp_mean_vt[0][_m_num] = None

            # mean max temp
            # if we have a total > 0 then calc a simple average
            if m_temp_mean_max_bin[_m_num][1] > 0:
                m_temp_mean_max_vt[0][_m_num] = m_temp_mean_max_bin[_m_num][0] / m_temp_mean_max_bin[_m_num][1]
            # otherwise we have no years of data so set our average to None
            else:
                m_temp_mean_max_vt[0][_m_num] = None

            # mean min temp
            # if we have a total > 0 then calc a simple average
            if m_temp_mean_min_bin[_m_num][1] > 0:
                m_temp_mean_min_vt[0][_m_num] = m_temp_mean_min_bin[_m_num][0] / m_temp_mean_min_bin[_m_num][1]
            # otherwise we have no years of data so set our average to None
            else:
                m_temp_mean_min_vt[0][_m_num] = None

        # convert to the required units and extract the converted values into
        # a vector
        m_rain_avg_vec = self.generator.converter.convert(m_rain_avg_vt).value
        m_temp_mean_vec = self.generator.converter.convert(m_temp_mean_vt).value
        m_temp_max_vec = self.generator.converter.convert(m_temp_max_vt).value
        m_temp_mean_max_vec = self.generator.converter.convert(m_temp_mean_max_vt).value
        m_temp_min_vec = self.generator.converter.convert(m_temp_min_vt).value
        m_temp_mean_min_vec = self.generator.converter.convert(m_temp_mean_min_vt).value

        # round the values in our vectors
        m_rain_avg_vec = [round_none(x, rain_round) for x in m_rain_avg_vec]
        m_temp_mean_vec = [round_none(x, temp_round) for x in m_temp_mean_vec]
        m_temp_max_vec = [round_none(x, temp_round) for x in m_temp_max_vec]
        m_temp_mean_max_vec = [round_none(x, temp_round) for x in m_temp_mean_max_vec]
        m_temp_min_vec = [round_none(x, temp_round) for x in m_temp_min_vec]
        m_temp_mean_min_vec = [round_none(x, temp_round) for x in m_temp_mean_min_vec]

        # format our vectors in json format
        m_rain_avg_json = json.dumps(m_rain_avg_vec)
        m_temp_mean_json = json.dumps(m_temp_mean_vec)
        m_temp_max_json = json.dumps(m_temp_max_vec)
        # month_temp_mean_min_max is vector of 2 way tuples, each tuple is (min, max)
        m_temp_mean_min_max_json = json.dumps(list(zip(m_temp_mean_min_vec,
                                              m_temp_mean_max_vec)))
        m_temp_min_json = json.dumps(m_temp_min_vec)

        # create a dictionary with the tag names (keys) we want to use
        _result = {'monthRainAvgjson': m_rain_avg_json,
                   'monthTempMeanjson': m_temp_mean_json,
                   'monthTempMaxjson': m_temp_max_json,
                   'monthTempMeanMinMaxjson': m_temp_mean_min_max_json,
                   'monthTempMinjson': m_temp_min_json}

        t2 = time.time()
        if weewx.debug >= 2:
            logdbg("MonthAverages SLE executed in %0.3f seconds" % (t2 - t1))

        return [_result]
