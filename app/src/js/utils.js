import moment from 'moment';
import {getCurrentLanguage} from './translate';

export const round = value => {
  return Math.round(value * 10000) / 10000;
};

export const humanizePosition = ([lat, lng]) => {
  return `${round(lat)}, ${round(lng)}`;
};

export const capitalize = value => {
  if (!value) return '';
  return value.charAt(0).toUpperCase() + value.slice(1);
};

export const humanize = value => {
  if (!value) return '';
  return value.split('_').join(' ');
};

export const humanizeDate = (day, month, year, place) => {
  let output = '';
  if (year && month && day) {
    moment.locale(getCurrentLanguage());
    output += moment([year, month, day]).format('LL');
  } else if (year) {
    output += year;
  }
  if (place) {
    output += ` (${place})`;
  }
  return output;
};

export const getDeviceWidth = () => {
  return window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
};

export const getDeviceHeight = () => {
  return window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;
};

/**
 * Encodes a map view center as a String.
 * @param lng
 * @param lat
 * @param zoom
 * @returns {string}
 */
export const mapStateToPath = ({ lng, lat }, zoom = 18) => {
  lng = round(lng);
  lat = round(lat);
  zoom = Math.round(zoom * 10) / 10;
  return `@${lng},${lat},${zoom}z`;
};

/**
 * Decodes a map view String into an Object.
 * @param path
 * @returns {{center: (*|string)[], zoom: (*|string)}}
 */
export const pathToMapState = path => {
  const str = path.trim();
  const [lng, lat, zoom] = path.slice(1, str.length - 1).split(',');
  return {
    center: { lat: Number(lat), lng: Number(lng) },
    zoom: Number(zoom)
  };
};

/**
 * Debounces function invocation.
 * @param func
 * @param wait
 * @param immediate
 * @returns {Function}
 */
export const debounce = (func, wait, immediate) => {
  let timeout;
  return function () {
    const context = this, args = arguments;
    const later = function () {
      timeout = null;
      if (!immediate) func.apply(context, args);
    };
    const callNow = immediate && !timeout;
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
    if (callNow) func.apply(context, args);
  };
};

/**
 *
 * @param value
 * @param index
 * @param self
 * @returns {boolean}
 */
export const unique = (value, index, self) => {
  return self.indexOf(value) === index;
};
