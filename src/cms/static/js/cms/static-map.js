(function() {
  function createStaticMap(mapId, position, icon) {
    const point = new ol.geom.Point(position).transform("EPSG:4326", "EPSG:3857");
    var feature = new ol.Feature({
        geometry: point
      });

      var iconStyle = new ol.style.Style({
        image: new ol.style.Icon({
          anchor: [0.5, 46],
          anchorXUnits: 'fraction',
          anchorYUnits: 'pixels',
          src: icon
        })
      });

      feature.setStyle(iconStyle);

      var vectorSource = new ol.source.Vector({
        features: [feature]
      });

      var vectorLayer = new ol.layer.Vector({
        source: vectorSource
      });
    const map = new ol.Map({
        controls: [
          new ol.control.Attribution()
        ],
        interactions: [],
        layers: [
          new ol.layer.Tile({
            source: new ol.source.OSM()
          }),
          vectorLayer
        ],
        target: mapId,
        view: new ol.View({
          center: point.getCoordinates(),
          zoom: 14
        })
      });
  }

  window.createStaticMap = createStaticMap;
})();
