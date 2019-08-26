/**
 * Rounds a LatLng to the given number of digits.
 * @param lat: number
 * @param lng: number
 * @param precision: int
 * @returns {{lng: number, lat: number}}
 */
export const roundCenter = ({lat, lng}, precision = 4) => {
  const factor = Math.pow(10, precision);
  return {
    lat: Math.round(lat * factor) / factor,
    lng: Math.round(lng * factor) / factor,
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
