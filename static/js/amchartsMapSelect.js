// Create map instance
var chart = am4core.create("mapSelectDiv", am4maps.MapChart);

// Set map definition
chart.geodata = am4geodata_polandLow;

// Set projection
chart.projection = new am4maps.projections.Mercator();

chart.seriesContainer.draggable = false;
chart.maxZoomLevel = 1;

// Create map polygon series
var polygonSeries = chart.series.push(new am4maps.MapPolygonSeries());

// Make map load polygon (like country names) data from GeoJSON
polygonSeries.useGeodata = true;
// Add some custom data
polygonSeries.data = [{
//   "id": "PL-28",
//   "color": am4core.color("#3F4B3B"),
//   "description": ''
// } 
}]

// Configure series
var polygonTemplate = polygonSeries.mapPolygons.template;
polygonTemplate.tooltipText = "{name}";
polygonTemplate.fill = am4core.color("#2f90a8");
polygonTemplate.events.on("hit", function(ev) {
  var data = ev.target.dataItem.dataContext;
  const request = new XMLHttpRequest()
  request.open('POST', `/mapClick/${JSON.stringify(data.id)}`)
  request.send()

//   var info = document.getElementById("info");

//   if(info.innerHTML.indexOf(data.name) == -1) {
//     info.innerHTML += "<h3>" + data.name + "</h3>";
// }
//   else {
//     info.innerHTML=info.innerHTML.replace(data.name,'');

//   }

//   if (data.description) {
//     info.innerHTML += data.description;
//   }
//   else {
//     info.innerHTML += ""
//   }
//   console.log("You clicked on :" + ev.target.dataItem.dataContext.id);
  ev.target.isActive=!ev.target.isActive; 
});

// Create active state
var activeState = polygonTemplate.states.create("active");
activeState.properties.fill = am4core.color("#0f3d5d");

// Create hover state and set alternative fill color
// var hs = polygonTemplate.states.create("hover");
// hs.properties.fill = am4core.color("#0f3d5d");


if(chart.logo) {
  chart.logo.disabled = true;
  }