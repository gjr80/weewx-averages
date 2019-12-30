"""install.py
Copyright (c) 2015-2016 Gary Roderick <gjroderick(at)gmail.com>

Released under GNU General Public License, Version 3, 29 June 2007.
Refer to the enclosed License file for your full rights.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details.

Installer for the WeeWX Averages extension.

Version: 1.0.0a1                                   Date: 30 December 2019

Revision History
    30 December 2019
        - removed code that used either report_timing or stale_age depending on
          WeeWX version
    30 September 2016   v0.5.0
        - initial implementation (bumped to v0.5.0 to align with supporting
          SLE version)
"""
import weewx

from distutils.version import StrictVersion
from setup import ExtensionInstaller

# TODO. Fix before release
REQUIRED_VERSION = "4.0.0b5"
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
        super(AveragesInstaller, self).__init__(
            version="1.0.0a1",
            name='Averages',
            description='Highcharts plots of WeeWX monthly averages.',
            author="Gary Roderick",
            author_email="gjroderick(at)gmail.com",
            config={
                'StdReport': {
                    'HighchartsAverages': {
                        'skin': 'HighchartsAverages',
                        'report_timing': '@monthly',
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
