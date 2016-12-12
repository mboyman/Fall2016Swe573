var draw = kendo.drawing;
var geom = kendo.geometry;

var gradient = new draw.LinearGradient({
    start: [0, 0], // Bottom left
    end: [0, 1],   // Top left
    stops: [{
        offset: 1,
        color: "rgb(160, 160, 160)",
        opacity: 0.7
    }, {
        offset: 1,
        color: "rgb(160, 160, 160)",
        opacity: 0.7
    }]
});

function getChartLostConnectionData(chart, chartData, parameters) {
    var dateData = new Array();
    var diff = differenceDateTime(parameters.from, chartData[0].Date);
    var comPeriod = moment.duration(parameters.communucationPeriod * 60000 * 3); //CommPeriod convert to ms multiple 3  
    if (moment.duration(Math.abs(diff)) > moment.duration(comPeriod))
    {
        var data = {
            xSlot: [parameters.from, chartData[0].Date],
            ySlot: [0, chart.yAxis.max]
        }
        dateData.push(data);
        data = {
            xSlot: [],
            ySlot: []
        }
    }
    for (var i = 1; i < chartData.length; i++) {
       
        var fTime = chartData[i].Date;
        var lTime = chartData[i - 1].Date;

        diff = differenceDateTime(fTime, lTime);
       
        if (moment.duration(Math.abs(diff)) > moment.duration(comPeriod)) {
            var data = {
                xSlot: [lTime, fTime],
                ySlot: [0, chart.yAxis.max]
            }
            dateData.push(data);
        }
        data = {
            xSlot: [],
            ySlot: []
        }
    }
    return dateData;
}

function adjustChartRange(Data, chart, parameters) {
    if (parameters.showLimits) {
        if (Data[0] != null) {
            var TempMax = getMaxData(Data);
            chart.yAxis.max = TempMax * 1.125;

            if (parameters.maxLimit > TempMax) {
                chart.yAxis.max = parameters.maxLimit * 1.25;
            }
        }
    }
    chart.xAxis.min = parameters.from;
    chart.xAxis.max = parameters.to;
}



function getChartSeries(chartData, parameters) {
    if (!chartData)
        return [];

    var series = new Array();

    var currentSeries = {
        color: parameters.normalColor,
        data: [],
        markers: {
            visible: false,
        }
    }

    if (!parameters.showLimits) {

        for (var i = 0; i < chartData.length; i++) {
            var item = chartData[i];
            var xval = item.Date;
            var yval = item.Data;

            currentSeries.data.push([xval, yval]);
        }
        series.push(currentSeries);
        return series;

    }
    series.push(currentSeries);

    for (var i = 0; i < chartData.length; i++) {
        var item = chartData[i];

        var xval = item.Date;
        var yval = item.Data;

        currentSeries.data.push([xval, yval]);

        if (yval > parameters.maxLimit || yval < parameters.minLimit) {
            if (currentSeries.color != parameters.outOfRangeColor && i > 0) {
                currentSeries.data.pop();
                var lastVal = currentSeries.data[currentSeries.data.length - 1];
                currentSeries = {
                    color: parameters.outOfRangeColor,
                    data: [],
                    markers: {
                        visible: false,
                    }
                }
                series.push(currentSeries);
                currentSeries.data.push([lastVal[0], lastVal[1]]);
            }
        }
        else {
            if (currentSeries.color != parameters.normalColor) {
                currentSeries = {
                    color: parameters.normalColor,
                    data: [],
                    markers: {
                        visible: false,
                    },
                }
                series.push(currentSeries);
            }
        }
        currentSeries.data.push([xval, yval]);
    }
    return series;
}

function differenceDateTime(now, then) {
    //var ms = moment(then, "DD/MM/YYYY HH:mm:ss").diff(moment(now, "DD/MM/YYYY HH:mm:ss"));
    var ms = then - now;
    return moment.duration(ms);
}

function getMaxData(numArray) {
    var max = numArray[0].Data;
    for (var i = 0; i < numArray.length; i++) {
        if (max < numArray[i].Data) {
            max = numArray[i].Data;
        }
    }
    return max;
}

function DrawKendoChart(data, chart, parameters) {

    var ChartData = getChartSeries(data, parameters);
    for (var i = 0; i < ChartData.length; i++) {
        chart.series.push(ChartData[i]);
    }

    adjustChartRange(data, chart, parameters);
    chart.render = function () {
        var xAxis = this.getAxis("xAxis");
        var yAxis = this.getAxis("yAxis");


        if (parameters.showLostConnection) {
            var conLostData = getChartLostConnectionData(chart, data, parameters);
            var group = new kendo.drawing.Group()
            for (var i = 0; i < conLostData.length; i++) {

                var xSlot = xAxis.slot(conLostData[i].xSlot[0], conLostData[i].xSlot[1]);
              
                var ySlot = yAxis.slot(0, 100);

                var rect = new geom.Rect([
                  // Origin X, Y
                  xSlot.origin.x, ySlot.origin.y
                ], [
                  // Width, height
                  xSlot.width(), ySlot.height()
                ]);

                var path = draw.Path.fromRect(rect, {
                    stroke: null,
                    fill: gradient
                });
                group.append(path);
            }

            this._plotArea.appendVisual(group);
        }

        if (parameters.showLimits) {
            var maxTempValueSlot = yAxis.slot(parameters.maxLimit);
            var minTempValueSlot = yAxis.slot(parameters.minLimit);
            var dateRange = xAxis.range();
            var dateSlot = xAxis.slot(dateRange.min, dateRange.max);
            var lineMax = new kendo.drawing.Path({
                stroke: {
                    color: "red",
                    width: 1,
                    opacity: 0.5
                }
            }).moveTo(dateSlot.origin.x, maxTempValueSlot.origin.y)
            .lineTo(dateSlot.bottomRight().x, maxTempValueSlot.origin.y);

            var lineMin = new kendo.drawing.Path({
                stroke: {
                    color: "red",
                    width: 1,
                    opacity: 0.5
                }
            }).moveTo(dateSlot.origin.x, minTempValueSlot.origin.y)
           .lineTo(dateSlot.bottomRight().x, minTempValueSlot.origin.y);

            this.surface.draw(lineMax);
            this.surface.draw(lineMin);
        }
    }

}