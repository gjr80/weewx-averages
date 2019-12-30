/**
*
* Copyright (c) 2015-2019 Gary Roderick <gjroderick(at)gmail.com>
*
* Released under GNU General Public License, Version 3, 29 June 2007.
* Refer to the enclosed License file for your full rights.
*
*
* Javascript code to initialise and render WeeWX monthly averages plot using
* Highcharts.
*
*
* Version: 1.0.0a1                                 Date: 30 December 2019
*
* Revision History
*   30 December 2019    v1.0.0
*       - version number change only
*   30 September 2016   v0.5.0
*       - now packaged as a weewx extension
*       - added config to allow users to change common look and feel
*         settings without delving into the code
*  10 May 2016          v0.4.0
*       - no change, version number upgrade only
*  April 2016           v0.3.0
*       - no change, version number upgrade only
*  5 March 2016         v0.2.2
*       - no change, version number upgrade only
*  21 July 2015         v0.2.1
*       - remove old redundant code
*  19 March 2015        v0.2.0
*       - no change, version number upgrade only
*  22 February 2015     v0.1.0
*       - initial implementation
*
**/

var config = {
    /**
    *
    * Below are some options the user may wish to tweak to set the look and
    * feel of the plot. All control various options detailed in the Highcharts
    * API Reference.
    *
    **/

    json_source: 'json/averages.json',  // path to the JSON file holding the source data
    render_to: 'monthaveragesplot',      // id of the HTML element where the chart will be rendered
    title: 'Monthly Temperature and Rainfall Averages',  // plot title. String
    show_legend: true,                      // display plot legend. true|false
    av_temp_range_label: 'Mean Temp Range', // legend label for mean temperature range plot. String
    av_temp_range_color: '#CC3399',         // color for mean temperature range plot. String, color name or RGB
    av_temp_range_opacity: 0.4,             // opacity for mean temperature range plot. Number
    av_temp_label: 'Mean Temp',             // legend label for mean temperature plot. String
    av_temp_color: '#BA55D3',               // color for mean temperature plot. String, color name or RGB
    max_temp_label: 'Max Temp',             // legend label for max temperature plot. String
    max_temp_color: '#FF0000',              // color for max temperature plot. String, color name or RGB
    min_temp_label: 'Min Temp',             // legend label for min temperature plot. String
    min_temp_color: '#0000FF',              // color for min temperature plot. String, color name or RGB
    avg_rainfall_label: 'Avg Rainfall',     // legend label for average rainfall plot. String
    avg_rainfall_color: '#72B2C4',          // color for avg rainfall plot. String, color name or RGB
    background_color_stop1: '#FCFFC5',      // 1st color to be used in background gradient. String, color name or RGB
    background_color_stop2: '#E0E0FF',      // 2nd color to be used in background gradient. String, color name or RGB
    marker_symbol: 'circle',                // marker symbol to be used for each point of each plot (except rainfall). String
    marker_enabled: false,                  // enable marker symbol for each plot(except rainfall). true|false
    updated_align: 'right',                 // alignment of 'Updated: ' label. 'right'|'left'
    updated_font_size: '10px',              // font size of 'Updated: ' label. String
    updated_x_offset: -25,                  // x offset of 'Updated: ' label. Number
    // month names to display on x-axis
    months: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    x_axis_line_color: '#555',              // x-axis line color. String, color name or RGB
    x_axis_line_width: 1,                   // x-axis line width in pixels. Nubmer
    x_axis_title_color: '#555',             // x-axis title color. String, color name or RGB
    // x-axis font
    x_axis_title_font: 'bold 12px Lucida Grande, Lucida Sans Unicode, Verdana, Arial, Helvetica, sans-serif',
    y_axis_line_color: '#555',              // y-axes line color. String, color name or RGB
    y_axis_line_width: 1,                   // y-axes line width in pixels. Nubmer
    x_axis_title_color: '#555',             // y-axes title color. String, color name or RGB
    // y-axes font
    y_axis_title_font: 'bold 12px Lucida Grande, Lucida Sans Unicode, Verdana, Arial, Helvetica, sans-serif',
    enable_tooltip: true,                   // display tooltip. true|false
    tooltip_font_size: '10px',              // tooltip font size. String
};

/**
*
* Edit anything below here at your own risk; get it wrong and your plot may not
* display and you will need to troubleshoot the JS yourself. All parameters are
* as described in the Highcharts API reference.
*
**/

$(document).ready(function() {

    var optionsAverages = {
        chart: {
            plotBackgroundColor: {
                linearGradient: { x1: 0, y1: 0, x2: 1, y2: 1 },
                stops: [
                    [0, config.background_color_stop1],
                    [1, config.background_color_stop1]
                ]
            },
            renderTo: config.render_to
        },
        legend: {
            enabled: config.show_legend,
            symbolHeight: 12,
            symbolRadius: 0,
            symbolWidth: 12,
        },
        plotOptions: {
            areasplinerange: {
                lineWidth: 0,
                marker: {
                    enabled: config.marker_enabled,
                    radius: 1,
                    symbol: config.marker_symbol
                },
                tooltip: {
                    valueSuffix: ''
                },
            },
            column: {
                borderWidth: 0,
                tooltip: {
                    valueSuffix: ''
                },
            },
            spline: {
                lineWidth: 1,
                marker: {
                    enabled: config.marker_enabled,
                    radius: 1,
                    symbol: config.marker_symbol
                },
                tooltip: {

                    valueSuffix: ''
                },
            },
        },
        series: [{
            name: config.av_temp_range_label,
            type: 'areasplinerange',
            color: config.av_temp_range_color,
            fillOpacity: config.av_temp_range_opacity,
            zIndex: 4,
        }, {
            name: config.av_temp_label,
            type: 'spline',
            color: config.av_temp_color,
            zIndex: 3,
        }, {
            name: config.max_temp_label,
            type: 'spline',
            color: config.max_temp_color,
            zIndex: 2,
        }, {
            name: config.min_temp_label,
            type: 'spline',
            color: config.min_temp_color,
            zIndex: 1,
        }, {
            name: config.avg_rainfall_label,
            type: 'column',
            color: config.avg_rainfall_color,
            zIndex: 0,
            yAxis: 1
        }],
        subtitle: {
            align: config.updated_align,
            style: {
                fontSize: config.updated_font_size
            },
            text: '',
            x: config.updated_x_offset
        },
        title: {
            text: config.title
        },
        tooltip: {
            crosshairs: [true, false],
            enabled: config.enable_tooltip,
            shared: true,
            style: {
                fontSize: config.tooltip_font_size,
            },
            // need to initialise valueSuffix now so we can set it later
            valueSuffix: ''
        },
        xAxis: {
            categories: config.months,
            lineColor: config.x_axis_line_color,
            lineWidth: config.x_axis_line_width,
            title: {
                style: {
                    color: config.x_axis_title_color,
                    font: config.x_axis_title_font
                }
            },
        },
        yAxis: [{
            endOnTick: true,
            lineColor: config.y_axis_line_color,
            lineWidth: config.y_axis_line_width,
            minorGridLineWidth: 0,
            showLastLabel: true,
            startOnTick: true,
            title: {
                style: {
                    color: config.x_axis_title_color,
                    font: config.x_axis_title_font
                },
                // need to initialise text now so we can set it later
                text: ''
            },
        },{
            lineColor: config.y_axis_line_color,
            lineWidth: config.y_axis_line_width,
            title: {
                // need to initialise text now so we can set it later
                text: ''
            },
            opposite: true
        }]
    };

    $.getJSON(config.json_source, function(seriesData) {
        optionsAverages.series[0].data = seriesData[0].temperatureplot.series.outTempMeanMinMax.data;
        optionsAverages.series[1].data = seriesData[0].temperatureplot.series.outTempMean.data;
        optionsAverages.series[2].data = seriesData[0].temperatureplot.series.outTempMax.data;
        optionsAverages.series[3].data = seriesData[0].temperatureplot.series.outTempMin.data;
        optionsAverages.series[4].data = seriesData[0].rainplot.series.rainAvg.data;
        optionsAverages.yAxis[0].title.text = 'Temperature ' + seriesData[0].temperatureplot.yAxisLabel.text;
        optionsAverages.yAxis[1].title.text = 'Rainfall ' + seriesData[0].rainplot.yAxisLabel.text;
        optionsAverages.plotOptions.areasplinerange.tooltip.valueSuffix = seriesData[0].temperatureplot.yAxisUnits.text;
        optionsAverages.plotOptions.spline.tooltip.valueSuffix = seriesData[0].temperatureplot.yAxisUnits.text;
        optionsAverages.plotOptions.column.tooltip.valueSuffix = seriesData[0].rainplot.yAxisUnits.text;
        optionsAverages.subtitle.text = 'Updated: ' + seriesData[0].generated;
        var chart = new Highcharts.Chart(optionsAverages);
    });
});