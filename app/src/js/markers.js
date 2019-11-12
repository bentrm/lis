import { icon, layer } from '@fortawesome/fontawesome-svg-core';
import {
  archive,
  birthdayCake,
  book,
  building,
  church,
  cross,
  graduationCap,
  info,
  landmark,
  lightbulb,
  mapMarker,
  monument,
  mountain,
  palette,
  road,
  square
} from './icons';


const symbols = {
  16: building,
  17: road,
  18: birthdayCake,
  19: building,
  20: cross,
  21: lightbulb,
  22: monument,
  23: monument,
  24: square,
  25: landmark,
  26: graduationCap,
  27: church,
  28: mountain,
  29: monument,
  30: palette,
  31: info,
  32: palette,
  33: book,
  34: archive,
};

/**
 * Returns the CSS class names used to insert FA icon via italic tag.
 * @param symbolId
 * @returns {String} CSS class names
 */
export const iconClassName = symbolId => {
  const { prefix, iconName } = symbols[symbolId] || monument;
  return `${prefix} fa-${iconName}`;
};

/**
 * Generates a new font awesome svg layer mapping a symbol id to a fa overlay icon.
 * @param symbolId
 * @returns {Layer}
 */
export default (symbolId) => {
  const symbol = symbols[symbolId] || monument;

  return layer(push => {
    push(icon(mapMarker, {
      styles: { 'color': '#69140e' },
      transform: { size: 48, x: 0, y: 0 },
    }));
    push(icon(symbol, {
      styles: { 'color': 'white' },
      transform: { x: 0, y: -4, size: 16 }
    }));
  }, {
    classes: ['fa-fw', 'fa-leaflet-layer', 'drop-shadow']
  });
};
