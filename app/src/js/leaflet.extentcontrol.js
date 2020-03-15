import translate from './translate';
import {Control, DomEvent, DomUtil} from 'leaflet';

export default Control.extend({

  options: {
    title: translate('Zoom to feature extent'),
    extent: null
  },

  setExtent(extent) {
    this.options.extent = extent;
  },

  onAdd(map) {

    const extentName = 'leaflet-control-extent';
    const container = DomUtil.create('div', extentName + ' leaflet-bar');
    const options = this.options;

    this._map = map;

    this._link = DomUtil.create('a', extentName + '-btn', container);
    this._link.href = '#';
    this._link.title = options.title;
    this._link.setAttribute('role', 'button');
    this._link.setAttribute('aria-label', options.title);

    DomUtil.create('i', 'fas fa-expand-arrows-alt', this._link);

    DomEvent
      .on(this._link, 'click', DomEvent.stopPropagation)
      .on(this._link, 'click', DomEvent.preventDefault)
      .on(this._link, 'click', this._onClick, this)
      .on(this._link, 'dblclick', DomEvent.stopPropagation);

    return container;
  },

  _onClick() {
    if (this.options.extent) {
      this._map.fitBounds(this.options.extent);
    }
  }

});
