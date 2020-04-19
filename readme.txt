The Averages extension is a WeeWX extension that calculates temperature maxima
and minima as well as temperature and rainfall averages for each month and
generates a JSON format file suitable for plotting this data using Highcharts.

The Averages extension consists of a WeeWX Search List Extension (SLE) that
calculates the monthly data, a skin that generates JSON format data file
containing the monthly data and an example HTML page and supporting javascript
that displays a monthly temperature and rainfall averages plot using
Highcharts.


Pre-Requisites

WeeWX v3.0.0 or greater.


File Locations

As WeeWX file locations vary by system and installation method, the following
symbolic names, as per the WeeWX User's Guide - Installing WeeWX, are used in
these instructions:

- $BIN_ROOT (Executables)
- $SKIN_ROOT (Skins and templates)
- $HTML_ROOT (Web pages and images)

Where applicable the nominal location for your system and installation type
should be used in place of the symbolic name


Installation Instructions

1.  Download the Averages extension from the 'releases' tab on the
weewx-averages GitHub site (https://github.com/gjr80/weewx-averages/releases)
into a directory accessible from the WeeWX machine:

    $ wget -P $DOWNLOAD_ROOT https://github.com/gjr80/weewx-averages/releases/download/v1.0.0/averages-1.0.0.tar.gz

	where $DOWNLOAD_ROOT is the path to the directory where the Averages
	extension is to be downloaded.

2.  Run the installer

    $ wee_extension install=$DOWNLOAD_ROOT/averages-1.0.0.tar.gz

    This will result in output similar to the following:

        Request to install '/var/tmp/averages-1.0.0.tar.gz'
        Extracting from tar archive /var/tmp/averages-1.0.0.tar.gz
        Saving installer file to /home/weewx/bin/user/installer/Averages
        Saved configuration dictionary. Backup copy at /home/weewx/weewx.conf.20200419124410
        Finished installing extension '/var/tmp/averages-1.0.0.tar.gz'

3.  Restart WeeWX:

    $ sudo /etc/init.d/weewx restart

    or

    $ sudo service weewx restart

    or

    $ sudo systemctl restart weewx

4.  This will result in:

    -   the JSON format data file averages.json being generated at the next
        report cycle (and then at midnight on the first of the month
        (WeeWX v3.6.0 or later) or every 24 hours (WeeWX v3.5.0 or earlier))
         and copied to the default $HTML_ROOT/json directory,

	-	the averages.html file being copied once to the default $HTML_ROOT
	    directory, and

	-	the averages.js and theme.js files being copied once to the default
	    $HTML_ROOT/scripts directory.

5.  Once a WeeWX report generation cycle is complete the sample monthly
averages plot may be viewed by pointing your browser at
$HTML_ROOT/averages.html.

6.  The Averages extension installation can be further customized (eg file
locations, units etc) by referring to the Averages extension User's Guide in
the Averages extension GitHub wiki.

Manual Installation Instructions

1.  Download the Averages extension from the 'releases' tab on the
weewx-averages GitHub site (https://github.com/gjr80/weewx-averages/releases)
into a directory accessible from the WeeWX machine:

    $ wget -P $DOWNLOAD_ROOT https://github.com/gjr80/weewx-averages/releases/download/v1.0.0/averages-1.0.0.tar.gz

	where $DOWNLOAD_ROOT is the path to the directory where the Averages
	extension is to be downloaded.

2.  Unpack the extension as follows:

    $ tar xvfz averages-1.0.0.tar.gz

3.  Copy files as follows:

    $ cp averages/bin/user/*.py $BIN_ROOT/user
    $ cp -R averages/skins/* $SKIN_ROOT

4.  In weewx.conf, modify the [StdReport] section by adding the following
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

        If you are using weewx v3.5.0 or earlier the report_timing option is
        not available and

        report_timing = @daily

        should be replaced with

        stale_age = 86400

        to generate the JSON format data file every 24 hours.

5.  Restart Weewx:

    $ sudo /etc/init.d/weewx restart

    or

    $ sudo service weewx restart

    or

    $ sudo systemctl restart weewx

4.  This will result in:

    -   the JSON format data file averages.json being generated at the next
        report cycle (and then at midnight on the first of the month
        (WeeWX v3.6.0 or later) or every 24 hours (WeeWX v3.5.0 or earlier))
         and copied to the default $HTML_ROOT/json directory,

	-	the averages.html file being copied once to the default $HTML_ROOT
	    directory, and

	-	the averages.js and theme.js files being copied once to the default
	    $HTML_ROOT/scripts directory.

5.  Once a WeeWX report generation cycle is complete the sample monthly
averages plot may be viewed by pointing your browser at
$HTML_ROOT/averages.html.

6.  The Averages extension installation can be further customized (eg file
locations, units etc) by referring to the Averages extension User's Guide in
the Averages extension GitHub wiki.