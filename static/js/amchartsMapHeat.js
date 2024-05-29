am4core.ready(function() {
    
    // Themes begin
    am4core.useTheme(am4themes_animated);
    // Themes end
    
    // Create map instance
    var chart = am4core.create("mapHeatDiv", am4maps.MapChart);
    
    // Set map definition
    chart.geodata = am4geodata_polandLow;
    
    // Set projection
    chart.projection = new am4maps.projections.Mercator();

    chart.seriesContainer.draggable = false;
    chart.maxZoomLevel = 1;


    var groupData = [
      {
        "name": "nadwyżka",
        "color": "#77c7ff",
        "data": []
      },
      {
        "name": "równowaga",
        "color": "#c3cad8",
        "data": []
      },
      {
        "name": "deficyt",
        "color": "#ee8308",
        "data": []
      }
    ];
    
    // This array will be populated with country IDs to exclude from the world series
    var excludedCountries = ["AQ"];
    
    // Create a series for each group, and populate the above array
    groupData.forEach(function(group) {
      var series = chart.series.push(new am4maps.MapPolygonSeries());
      series.name = group.name;
      series.useGeodata = true;
      var includedCountries = [];
      group.data.forEach(function(country) {
        includedCountries.push(country.id);
        excludedCountries.push(country.id);
      });
      series.include = includedCountries;
    
      series.fill = am4core.color(group.color);
    
      // By creating a hover state and setting setStateOnChildren to true, when we
      // hover over the series itself, it will trigger the hover SpriteState of all
      // its countries (provided those countries have a hover SpriteState, too!).
      series.setStateOnChildren = true;
      series.calculateVisualCenter = true;
    
      // Country shape properties & behaviors
      var mapPolygonTemplate = series.mapPolygons.template;
      // Instead of our custom title, we could also use {name} which comes from geodata  
      mapPolygonTemplate.fill = am4core.color(group.color);
      mapPolygonTemplate.fillOpacity = 0.8;
      mapPolygonTemplate.nonScalingStroke = true;
      mapPolygonTemplate.tooltipPosition = "fixed"
    
      mapPolygonTemplate.events.on("over", function(event) {
        series.mapPolygons.each(function(mapPolygon) {
          mapPolygon.isHover = true;
        })
        event.target.isHover = false;
        event.target.isHover = true;
      })
    
      mapPolygonTemplate.events.on("out", function(event) {
        series.mapPolygons.each(function(mapPolygon) {
          mapPolygon.isHover = false;
        })
      })
    
      // States  
      var hoverState = mapPolygonTemplate.states.create("hover");
      hoverState.properties.fill = am4core.color("#0f3d5d");
    
      // Tooltip
      mapPolygonTemplate.tooltipText = "{title} {customData}"; // enables tooltip
      // series.tooltip.getFillFromObject = false; // prevents default colorization, which would make all tooltips red on hover
      // series.tooltip.background.fill = am4core.color(group.color);
    
      // MapPolygonSeries will mutate the data assigned to it, 
      // we make and provide a copy of the original data array to leave it untouched.
      // (This method of copying works only for simple objects, e.g. it will not work
      //  as predictably for deep copying custom Classes.)
      series.data = JSON.parse(JSON.stringify(group.data));
    });
    
    // The rest of the world.
    var worldSeries = chart.series.push(new am4maps.MapPolygonSeries());
    var worldSeriesName = "world";
    worldSeries.name = worldSeriesName;
    worldSeries.useGeodata = true;
    worldSeries.exclude = excludedCountries;
    worldSeries.fillOpacity = .2;
    // worldSeries.stroke = "black";
    // worldSeries.strokeWidth = 1;
    worldSeries.hiddenInLegend = true;
    worldSeries.mapPolygons.template.nonScalingStroke = true;
    
    // This auto-generates a legend according to each series' name and fill
    // chart.legend = new am4maps.Legend();
    
    // Legend styles
    // chart.legend.paddingLeft = 0;
    // chart.legend.paddingRight = 0;
    // chart.legend.marginTop = 150;
    // chart.legend.marginBottom = 0;
    // chart.legend.width = am4core.percent(90);
    
    // chart.legend.paddingTop = 100;

    // chart.legend.maxWidth = 300;
    // chart.legend.valign = "bottom";
    // chart.legend.contentAlign = "center";
    
    // let markerTemplate = chart.legend.markers.template;
    // markerTemplate.width = 20;
    // markerTemplate.height = 20;

    // // Legend items
    // chart.legend.itemContainers.template.interactionsEnabled = true;
    
    if(chart.logo) {
        chart.logo.disabled = true;
        }

    }); // end am4core.ready()