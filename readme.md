# Averages extension for weewx #

## Description ##

The Averages extension for `weewx` calculates temperature maxima and minima as well as temperature and rainfall  averages for each month and generates a JSON format file suitable for plotting this data using Highcharts. A sample HTML page and the Javascript necessary to render a Highcharts plot of the resulting data are included with the Averages extension.

A sample plot produced using the Averages extension is included below:

![Example monthly temeperature and rainfall avereges plot](https://github.com/gjr80/weewx-averages/blob/master/chart.png)

The Averages extension consists of a `weewx` Search List Extension (SLE) that calculates the monthly aggregates, a skin that generates JSON format data file containing the monthly data and an example HTML page and supporting javascript that displays the monthly temperature and rainfall data on a Highcharts generated graph.


## Pre-Requisites ##

The Averages extension requires `weewx v3.0.0` or greater. Some optional features of the Averages extension require `weewx 3.6.0` or greater. Refer to the [User's Guide](https://github.com/gjr80/weewx-averages/wiki/User's-Guide "Averages extension User's Guide").  

## Installation ##

The [Averages extension wiki](https://github.com/gjr80/weewx-averages/wiki "Averages extension wiki") contains installation and customization instructions for the extension.

## Support ###

General support issues may be raised in the Google Groups [weewx-user forum](https://groups.google.com/group/weewx-user "Google Groups weewx-user forum"). 
 
## Licensing ##

The Averages extension for weewx is licensed under the GNU Public License v3.