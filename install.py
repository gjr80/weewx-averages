"""
install.py

Installer for the Averages extension for WeeWX.

Copyright (c) 2015-2016 Gary Roderick <gjroderick(at)gmail.com>

Released under GNU General Public License, Version 3, 29 June 2007.
Refer to the enclosed License file for your full rights.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details.


Version: 1.0.0                                     Date: 25 May 2020

Revision History
    25 May 2020         v1.0.0
        - bumped version only
    30 September 2016   v0.5.0
        - initial implementation (bumped to v0.5.0 to align with supporting
          SLE version)
"""
import weewx

from distutils.version import StrictVersion
from setup import ExtensionInstaller

REQUIRED_VERSION = "3.0.0"
AFW_VERSION = "1.0.0"


def loader():
    return AveragesInstaller()


class AveragesInstaller(ExtensionInstaller):
    def __init__(self):
        if StrictVersion(weewx.__version__) < StrictVersion(REQUIRED_VERSION):
            msg = "%s requires WeeWX %s or greater, found %s" % ('Averages ' + AFW_VERSION,
                                                                 REQUIRED_VERSION,
                                                                 weewx.__version__)
            raise weewx.UnsupportedFeature(msg)
        # If our weewx version is >= 3.6.0 then we can use report_timing to
        # control when the report is generated otherwise we can only use
        # stale_age. Call weewx.require_weewx_version(); if no error use
        # report_timing, if an error then catch it and use stale_age
        try:
            weewx.require_weewx_version('Averages', '3.6.0')
            _timing = 'report_timing'
            _timing_setting = '@monthly'
        except weewx.UnsupportedFeature:
            _timing = 'stale_age'
            _timing_setting = '86400'

        super(AveragesInstaller, self).__init__(
            version="1.0.0",
            name='Averages',
            description='Highcharts plots of WeeWX monthly averages.',
            author="Gary Roderick",
            author_email="gjroderick(at)gmail.com",
            config={
                'StdReport': {
                    'HighchartsAverages': {
                        'skin': 'HighchartsAverages',
                        _timing: _timing_setting,
                        'Units': {
                            'Groups': {
                                'group_rain':        'mm',
                                'group_temperature': 'degree_C',
                            },
                            'StringFormats': {
                                'degree_C': '%.1f',
                                'degree_F': '%.1f',
                                'cm':       '%.2f',
                                'inch':     '%.2f',
                                'mm':       '%.1f'
                            },
                            'TimeFormats': {
                                'current': '%-d %B %Y %H:%M'
                            }
                        },
                        'CopyGenerator': {
                            'copy_once': ['scripts/averages.js',
                                          'scripts/theme.js', 
                                          'averages.html']
                        },
                        'Generators': {
                            'generator_list': ['weewx.cheetahgenerator.CheetahGenerator', 
                                               'weewx.reportengine.CopyGenerator']
                        }
                    }
                }
            },
            files=[('bin/user',                         ['bin/user/averagesSearchX.py']),
                   ('skins/HighchartsAverages',         ['skins/HighchartsAverages/averages.html',
                                                         'skins/HighchartsAverages/skin.conf']),
                   ('skins/HighchartsAverages/json',    ['skins/HighchartsAverages/json/averages.json.tmpl']),
                   ('skins/HighchartsAverages/scripts', ['skins/HighchartsAverages/scripts/averages.js',
                                                         'skins/HighchartsAverages/scripts/theme.js'])
                   ]
        )
