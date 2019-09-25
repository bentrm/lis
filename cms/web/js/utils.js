/**
 * Encodes a map view center as a String.
 * @param lon
 * @param lat
 * @param zoom
 * @returns {string}
 */
export const mapStateToPath = ([lon, lat], zoom) => {
  lon = Math.round(lon * 10000) / 10000;
  lat = Math.round(lat * 10000) / 10000;
  zoom = Math.round(zoom * 10) / 10;
  return `@${lon},${lat},${zoom}z`;
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
    center: [Number(lat), Number(lng)],
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
  return function() {
    const context = this, args = arguments;
    const later = function() {
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
