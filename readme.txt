Averages - weewx extension that calculates monthly averages and generates JSON
format file suitable for plotting these averages using Highcharts.

The Averages extension consists of a weewx Search List Extension (SLE) that
calculates the monthly averages, a skin that generates JSON format data file
containing the monthly averages data and an example HTML page that displays a
monthly averages plot using Highcharts.


Pre-Requisites

weewx v3.0.0 or greater. weewx 3.6.0 or greater is required if the
report_timing option is used to control when the monthly averages JSON file is
generated.


File Locations

As weewx file locations vary by system and installation method, the following
symbolic names, as per the weewx User's Guide - Installing weewx, are used in
these instructions:

- $BIN_ROOT (Executables)
- $SKIN_ROOT (Skins and templates)
- $HTML_ROOT (Web pages and images)

Where applicable the nominal location for your system and installation type
should be used in place of the symbolic name


Installation Instructions

1)  Download the Averages extension from the 'releases' tab on the
weewx-averages gitHub site (https://github.com/gjr80/weewx-averages/releases).

2)  Run the installer

    $ ./wee_extension install=averages-X.Y.Z.tar.gz

    This command assumes the user is currently in the $BIN_ROOT folder.

3)  The units, number and date formats for the generated JSON format data file
are set at the  [[HighchartsAverages]] section in the [StdReport] section
of weewx.conf. The default settings are:

    [[HighchartsAverages]]
        [[[Units]]]
            [[[[Groups]]]]
                group_rain         = mm         # Options are 'inch' or 'mm'
                group_temperature  = degree_C   # Options are 'degree_F' or 'degree_C'
            [[[[StringFormats]]]]
                inch = %.2f
                mm = %.1f
                degree_F = %.1f
                cm = %.2f
                degree_C = %.1f
            [[[[TimeFormats]]]]
                current = %-d %B %Y

        If you wish to use different units or formats then you should alter the
        above settings in weewx.conf. There is no need to change anything in
        the HighchartsAverages skin files, this should be avoided as any
        changes made to the HighchartsAverages skin files will be lost if the
        Averages extension is upgraded.

4)  By default the Averages extension places the generated files in the
$HTML_ROOT/json folder, nominally /home/weewx/public_html/json for a setup.py
install. If you wish to place the generated files in another directory then
edit the 'HTML_ROOT' setting under the [[HighchartsAverages]] section in the
[StdReport] section of weewx.conf.

5)  As monthly averages are slow changing and given the relatively long time to
calculates the averages for for large data sets, the monthly averages JSON
format data file is only generated once per day. If weewx 3.6.0a1 or later is
installed then the report_timing option will be used to generate the report at
midnight each day. If weewx 3.5.0 or earlier is installed then the stale_age
option will be used to generate the report every 24 hours. Whatever option is
installed, the setting can be changed under the [[HighchartsAverages]] section
in the [StdReport] section of weewx.conf.

6)  Restart weewx:

    $ sudo /etc/init.d/weewx stop
    $ sudo /etc/init.d/weewx start

7)  This will result in the monthly averages JSON format data file being
generated at either midnight or every 24 hours.


Manual Installation Instructions

1)  Download the Averages extension from the 'releases' tab on the
weewx-averages gitHub site (https://github.com/gjr80/weewx-averages/releases).

2)  Copy files as follows:

    $ cp averages/bin/user/*.py $BIN_ROOT/user
    $ cp -R averages/skins/* $SKIN_ROOT

3)  In weewx.conf, modify the [StdReport] section by adding the following
section:

    [[HighchartsAverages]]
        report_timing = @daily
        HTML_ROOT = public_html/json
        skin = HighchartsAverages
        [[[Units]]]
            [[[[Groups]]]]
                group_rain         = mm         # Options are 'inch' or 'mm'
                group_temperature  = degree_C   # Options are 'degree_F' or 'degree_C'
            [[[[StringFormats]]]]
                inch = %.2f
                mm = %.1f
                degree_F = %.1f
                cm = %.2f
                degree_C = %.1f
            [[[[TimeFormats]]]]
                current = %-d %B %Y

        If you wish to use different units or formats then you should alter the
        above settings in weewx.conf. There is no need to change anything in
        the HighchartsAverages skin files, this should be avoided as any
        changes made to the HighchartsAverages skin files will be lost if the
        Averages extension is upgraded.

        If you are using weewx v3.5.0 or earlier the report_timing option is
        not available and

        report_timing = @daily

        should be replaced with

        stale_age = 86400

        to generate the JSON format data file every 24 hours.

4)  By default the Averages extension places the generated files in the
$HTML_ROOT/json folder, nominally /home/weewx/public_html/json for a setup.py
install. If you wish to place the generated files in another directory then
edit the 'HTML_ROOT' setting under the [[HighchartsAverages]] section in the
[StdReport] section of weewx.conf.

5)  As monthly averages are slow changing and given the relatively long time to
calculates the averages for for large data sets, the monthly averages JSON
format data file is only generated once per day. If weewx 3.6.0a1 or later is
installed then the report_timing option will be used to generate the report at
midnight each day. If weewx 3.5.0 or earlier is installed then the stale_age
option will be used to generate the report every 24 hours. Whatever option is
installed, the setting can be changed under the [[HighchartsAverages]] section
in the [StdReport] section of weewx.conf.

6)  Restart Weewx:

    $ sudo /etc/init.d/weewx stop
    $ sudo /etc/init.d/weewx start

7)  This will result in the monthly averages JSON format data file being
generated at either midnight or every 24 hours.


Uninstallation Instructions

1)  Stop weewx:

    $ sudo /etc/init.d/weewx stop

2)  Run the uninstaller

    $ ./wee_extension uninstall=Averages

    This command assumes the user is currently in the $BIN_ROOT folder.

3)  If required restart weewx:

    $ sudo /etc/init.d/weewx start


Manual Uninstallation Instructions

1)  Stop weewx:

    $ sudo /etc/init.d/weewx stop

2)  Delete the Averages extension folders and files as follows:

    $ rm $BIN_ROOT/user/averagesSearchX.py
    $ rm -r $SKIN_ROOT/HighchartsAverages

3)  In weewx.conf, delete the [StdReport] [[HighchartsAverages]] section.

4)  If required restart weewx:

    $ sudo /etc/init.d/weewx start