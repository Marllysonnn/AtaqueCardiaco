am5.ready(function() {

  // Create root element
  var root = am5.Root.new("chartduo");

  // Set themes
  root.setThemes([
    am5themes_Animated.new(root)
  ]);

  root.container.set("layout", root.verticalLayout);
 
  // Create container to hold charts
  var chartContainer = root.container.children.push(am5.Container.new(root, {
    layout: root.horizontalLayout,
    width: am5.p100,
    height: am5.p100
  }));

  // Create the 1st chart
  var chart = chartContainer.children.push(
    am5percent.PieChart.new(root, {
      endAngle: 270,
      innerRadius: am5.percent(60)
    })
  );

  var series = chart.series.push(
    am5percent.PieSeries.new(root, {
      valueField: "homens_ataque",
      categoryField: "age",
      endAngle: 270,
      alignLabels: false
    })
  );

  series.children.push(am5.Label.new(root, {
    centerX: am5.percent(50),
    centerY: am5.percent(50),
    text: "Homens com Ataque Cardíaco: {valueSum}",
    populateText: true,
    fontSize: "1.5em"
  }));

  series.slices.template.setAll({
    cornerRadius: 8
  });

  series.states.create("hidden", {
    endAngle: -90
  });

  series.labels.template.setAll({
    textType: "circular"
  });

  // Create the 2nd chart
  var chart2 = chartContainer.children.push(
    am5percent.PieChart.new(root, {
      endAngle: 270,
      innerRadius: am5.percent(60)
    })
  );

  var series2 = chart2.series.push(
    am5percent.PieSeries.new(root, {
      valueField: "mulheres_ataque",
      categoryField: "age",
      endAngle: 270,
      alignLabels: false,
      tooltip: am5.Tooltip.new(root, {}) // a separate tooltip needed for this series
    })
  );

  series2.children.push(am5.Label.new(root, {
    centerX: am5.percent(50),
    centerY: am5.percent(50),
    text: "Mulheres com Ataque Cardíaco: {valueSum}",
    populateText: true,
    fontSize: "1.5em"
  }));

  series2.slices.template.setAll({
    cornerRadius: 8
  });

  series2.states.create("hidden", {
    endAngle: -90
  });

  series2.labels.template.setAll({
    textType: "circular"
  });

  // Duplicate interaction
  series.slices.template.events.on("pointerover", function(ev) {
    var slice = ev.target;
    var dataItem = slice.dataItem;
    var otherSlice = getSlice(dataItem, series2);

    if (otherSlice) {
      otherSlice.hover();
    }
  });

  series.slices.template.events.on("pointerout", function(ev) {
    var slice = ev.target;
    var dataItem = slice.dataItem;
    var otherSlice = getSlice(dataItem, series2);

    if (otherSlice) {
      otherSlice.unhover();
    }
  });

  series.slices.template.on("active", function(active, target) {
    var slice = target;
    var dataItem = slice.dataItem;
    var otherSlice = getSlice(dataItem, series2);

    if (otherSlice) {
      otherSlice.set("active", active);
    }
  });

  // Same for the 2nd series
  series2.slices.template.events.on("pointerover", function(ev) {
    var slice = ev.target;
    var dataItem = slice.dataItem;
    var otherSlice = getSlice(dataItem, series);

    if (otherSlice) {
      otherSlice.hover();
    }
  });

  series2.slices.template.events.on("pointerout", function(ev) {
    var slice = ev.target;
    var dataItem = slice.dataItem;
    var otherSlice = getSlice(dataItem, series);

    if (otherSlice) {
      otherSlice.unhover();
    }
  });

  series2.slices.template.on("active", function(active, target) {
    var slice = target;
    var dataItem = slice.dataItem;
    var otherSlice = getSlice(dataItem, series);

    if (otherSlice) {
      otherSlice.set("active", active);
    }
  });

  // Fetch data from the endpoint
  fetch('/dados_histograma')
    .then(response => response.json())
    .then(data => {
      // Set data for the 1st chart
      series.data.setAll(data);

      // Set data for the 2nd chart
      series2.data.setAll(data);
    })
    .catch(error => {
      console.error('Error fetching data:', error);
    });

  function getSlice(dataItem, series) {
    var otherSlice;
    am5.array.each(series.dataItems, function(di) {
      if (di.get("category") === dataItem.get("category")) {
        otherSlice = di.get("slice");
      }
    });

    return otherSlice;
  }

  // Create legend
  var legend = root.container.children.push(am5.Legend.new(root, {
    x: am5.percent(50),
    centerX: am5.percent(50)
  }));

  // Trigger all the same for the 2nd series
  legend.itemContainers.template.events.on("pointerover", function(ev) {
    var dataItem = ev.target.dataItem.dataContext;
    var slice = getSlice(dataItem, series2);
    slice.hover();
  });

  legend.itemContainers.template.events.on("pointerout", function(ev) {
    var dataItem = ev.target.dataItem.dataContext;
    var slice = getSlice(dataItem, series2);
    slice.unhover();
  });

  legend.itemContainers.template.on("disabled", function(disabled, target) {
    var dataItem = target.dataItem.dataContext;
    var slice = getSlice(dataItem, series2);
    if (disabled) {
      series2.hideDataItem(slice.dataItem);
    } else {
      series2.showDataItem(slice.dataItem);
    }
  });

  legend.data.setAll(series.dataItems);

  series.appear(1000, 100);

}); // end am5.ready()
