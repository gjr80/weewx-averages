/**
 * Theme distributed with Averages weewx extension
 * Based on Gray theme for Highcharts JS by Torstein Honsi
 **/

Highcharts.theme = {
    chart: {
        backgroundColor: 'rgb(208, 208, 208)',
        borderWidth: 1,
        borderColor: '#000000',
        borderRadius: 8,
        plotShadow: false,
        plotBorderWidth: 0,
    },

    colors: ["#B44242", "#4242B4", "#42B442", "#DF5353", "#aaeeee", "#ff0066", "#eeaaee",
        "#55BF3B", "#DF5353", "#7798BF", "#aaeeee"],

    labels: {
        style: {
            color: '#CCC'
        }
    },

    legend: {
        borderWidth: 0,
        itemStyle: {
            color: '#555'
        },
        itemHoverStyle: {
            color: '#FFF'
        },
        itemHiddenStyle: {
            color: '#999'
        },
        margin: 5,
        padding: 4,
        symbolPadding: 2
    },

    plotOptions: {
        column: {
            shadow: false
        },
    },

    subtitle: {
        style: {
            color: '#555',
        }
    },

    title: {
        margin: 5,
        style: {
            color: '#555',
            font: '16px Lucida Grande, Lucida Sans Unicode, Verdana, Arial, Helvetica, sans-serif'
        }
    },

    xAxis: {
        labels: {
            style: {
                color: '#555',
                fontWeight: 'bold',
                whiteSpace: 'nowrap'
            }
        },
        minorGridLineWidth: 0,
        minorTickInterval: 'auto',
        minorTickLength: 10,
        tickColor: '#555',
        title: {
            style: {
                color: '#555',
            }
        }
    },
    yAxis: {
        allowDecimals: false,
        gridLineColor: '#AAA',
        gridLineWidth: 1,
        labels: {
            style: {
                color: '#555',
            }
        },
        lineWidth: 1,
        minorTickColor: '#555',
        minorTickInterval: 'auto',
        minorTickLength: 2,
        minorTickWidth: 1,
        minTickInterval: null,
        tickWidth: 1,
        title: {
            style: {
                color: '#555',
                font: 'bold 12px Lucida Grande, Lucida Sans Unicode, Verdana, Arial, Helvetica, sans-serif'
            }
        }
    },

    toolbar: {
        itemStyle: {
            color: '#CCC'
        }
    },

    tooltip: {
        backgroundColor: 'rgba(255, 255, 204, .7)',
        borderWidth: 0,
        style: {
            color: '#555'
        }
    },

    navigation: {
        buttonOptions: {
            symbolStroke: '#DDDDDD',
            hoverSymbolStroke: '#FFFFFF',
            theme: {
                fill: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                    stops: [
                        [0.4, '#606060'],
                        [0.6, '#333333']
                    ]
                },
                stroke: '#000000'
            }
        }
    },
};

// Apply the theme
var highchartsOptions = Highcharts.setOptions(Highcharts.theme);
