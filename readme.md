# Averages extension for WeeWX #

## Description ##

The *Averages* extension for WeeWX calculates temperature maxima and minima as well as temperature and rainfall averages for each month and generates a JSON format file suitable for plotting this data using Highcharts. A sample HTML page and the JavaScript necessary to render a Highcharts plot of the resulting data are included with the *Averages* extension.

An example plot produced using the *Averages* extension is included below:

![Example monthly temperature and rainfall averages plot](https://github.com/gjr80/weewx-averages/blob/master/chart.png "Example monthly temperature and rainfall averages plot")

The *Averages* extension consists of a WeeWX Search List Extension (SLE) that calculates the monthly aggregates, a skin that generates JSON format data file containing the monthly data and a sample HTML page and supporting JavaScript that displays the monthly temperature and rainfall data on a Highcharts generated graph.


## Pre-Requisites ##

The *Averages* extension requires WeeWX v3.0.0 or greater. Refer to the [User's Guide](https://github.com/gjr80/weewx-averages/wiki/User's-Guide "Averages extension User's Guide").  

## Installation ##

Most user's should install the *Averages* extension using the [Quick-Start Guide](https://github.com/gjr80/weewx-averages/wiki/Quick-Start-Guide "Averages extension Quick-Start Guide"). Further details along with manual installation, uninstallation and customization instructions can be found in the [User's Guide](https://github.com/gjr80/weewx-averages/wiki/User's-Guide "Averages extension User's Guide").

## Support ###

General support issues may be raised in the Google Groups [weewx-user forum](https://groups.google.com/group/weewx-user "Google Groups weewx-user forum"). Specific bugs in the *Averages* extension code should be the subject of a new issue raised via the [Issues Page](https://github.com/gjr80/weewx-averages/issues "Averages extension Issues").
 
## Licensing ##

The *Averages* extension for WeeWX is licensed under the [GNU Public License v3](https://github.com/gjr80/weewx-averages/blob/master/LICENSE "Averages extension License").