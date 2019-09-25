import L from 'leaflet';

export default L.Control.extend({

  options: {
    title: 'Zoom to feature extent',
    layer: null
  },

  onAdd (map) {
    const extentName = 'leaflet-control-extent';
    const container = L.DomUtil.create('div', extentName + ' leaflet-bar');
    const options = this.options;

    this._map = map;

    this._link = L.DomUtil.create('a', extentName + '-btn', container);
    this._link.href = '#';
    this._link.title = options.title;
    this._link.setAttribute('role', 'button');
    this._link.setAttribute('aria-label', options.title);

    L.DomUtil.create('i', 'fas fa-expand-arrows-alt', this._link);

    L.DomEvent
      .on(this._link, 'click', L.DomEvent.stopPropagation)
      .on(this._link, 'click', L.DomEvent.preventDefault)
      .on(this._link, 'click', this._onClick, this)
      .on(this._link, 'dblclick', L.DomEvent.stopPropagation);

    return container;
  },

  _onClick () {
    if (this.options.layer.getLayers().length) {
      this._map.fitBounds(this.options.layer.getBounds());
    }
  }

});
