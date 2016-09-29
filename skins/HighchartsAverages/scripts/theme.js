/**
*
* Theme distributed with Averages weewx extension. Based on Gray theme for 
* Highcharts JS by Torstein Honsi.
* 
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

    tooltip: {
        backgroundColor: 'rgba(255, 255, 204, .7)',
        borderWidth: 0,
        style: {
            color: '#555'
        }
    },

    plotOptions: {
        line: {
            dataLabels: {
                color: '#CCC'
            },
            marker: {
                lineColor: '#333'
            }
        },
        column: {
            shadow: false
        },
        spline: {
            marker: {
                lineColor: '#333'
            }
        },
        scatter: {
            marker: {
                lineColor: '#333'
            }
        },
        candlestick: {
            lineColor: 'white'
        }
    },

    toolbar: {
        itemStyle: {
            color: '#CCC'
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

    // scroll charts
    rangeSelector: {
        buttonTheme: {
            fill: {
                linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                stops: [
                    [0.4, '#888'],
                    [0.6, '#555']
                ]
            },
            stroke: '#000000',
            style: {
                color: '#CCC',
                fontWeight: 'bold'
            },
            states: {
                hover: {
                    fill: {
                        linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                        stops: [
                            [0.4, '#BBB'],
                            [0.6, '#888']
                        ]
                    },
                    stroke: '#000000',
                    style: {
                        color: 'white'
                    }
                },
                select: {
                    fill: {
                        linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                        stops: [
                            [0.1, '#000'],
                            [0.3, '#333']
                        ]
                    },
                    stroke: '#000000',
                    style: {
                        color: 'yellow'
                    }
                }
            }
        },
        inputStyle: {
            backgroundColor: '#333',
            color: 'silver'
        },
        labelStyle: {
            color: 'silver'
        }
    },

    navigator: {
        handles: {
            backgroundColor: '#666',
            borderColor: '#AAA'
        },
        outlineColor: '#CCC',
        maskFill: 'rgba(16, 16, 16, 0.5)',
        series: {
            color: '#7798BF',
            lineColor: '#A6C7ED'
        }
    },

    scrollbar: {
        barBackgroundColor: {
                linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                stops: [
                    [0.4, '#888'],
                    [0.6, '#555']
                ]
            },
        barBorderColor: '#CCC',
        buttonArrowColor: '#CCC',
        buttonBackgroundColor: {
                linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                stops: [
                    [0.4, '#888'],
                    [0.6, '#555']
                ]
            },
        buttonBorderColor: '#CCC',
        rifleColor: '#FFF',
        trackBackgroundColor: {
            linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
            stops: [
                [0, '#000'],
                [1, '#333']
            ]
        },
        trackBorderColor: '#666'
    },

    // special colors for some of the demo examples
    legendBackgroundColor: 'rgba(48, 48, 48, 0.8)',
    legendBackgroundColorSolid: 'rgb(70, 70, 70)',
    dataLabelsColor: '#444',
    textColor: '#E0E0E0',
    maskColor: 'rgba(255,255,255,0.3)'
};

// Apply the theme
var highchartsOptions = Highcharts.setOptions(Highcharts.theme);
