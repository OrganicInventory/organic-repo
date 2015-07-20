/*These lines are all chart setup.  Pick and choose which chart features you want to utilize. */
nv.addGraph(function() {
  var chart = nv.models.lineChart()
                .margin({left: 100, right:100, top:100})  //Adjust chart margins to give the x-axis some breathing room.
                .useInteractiveGuideline(true)  //We want nice looking tooltips and a guideline!
                .duration(350)  //how fast do you want the lines to transition?
                .showLegend(true)       //Show the legend, allowing users to turn on/off line series.
                .showYAxis(true)        //Show the y-axis
                .showXAxis(true)        //Show the x-axis
                .forceY([0])
                .interpolate('monotone')
      ;


  chart.xAxis     //Chart x-axis settings
      .axisLabel('Date')
      .axisLabelDistance(13)
      .tickPadding(15)
      .tickFormat(function(d) {
    return d3.time.format('%x')(new Date((d + 86400) * 1000))
});

  chart.yAxis     //Chart y-axis settings
      .axisLabel('Product Usage (oz)')
      .axisLabelDistance(15)
      .tickPadding(15)
      .tickFormat(d3.format('.02f'));

  /* Done setting the chart up? Time to render it!*/


  d3.select('#product_chart svg')    //Select the <svg> element you want to render the chart in.
      .datum(productdata)         //Populate the <svg> element with chart data...
      .call(chart);          //Finally, render the chart!

  //Update the chart when window resizes.
  nv.utils.windowResize(function() { chart.update() });
  return chart;
});