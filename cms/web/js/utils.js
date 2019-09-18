/**
 * Returns a decoded map view Object.
 * @param href The url that may include an encoded map view.
 */
export const getMapView = href => {
  const pathNameParts = href.split('/');
  const positionIdx = pathNameParts.findIndex(isViewPath);
  return positionIdx ? pathToMapCenter(pathNameParts[positionIdx]) : undefined;
};

/**
 * Replaces or adds an encoded map view path component to the given href.
 * @param href
 * @param mapView
 * @returns {string}
 */
export const setMapView = (pathname, {center, zoom}) => {
  if (pathname.endsWith('/')) {
    pathname = pathname.substr(0, pathname.length - 1);
  }

  const pathNameParts = pathname.split('/');
  const positionIdx = pathNameParts.findIndex(isViewPath);
  const pathComponent = mapCenterToPath(center, zoom);

  if (positionIdx > -1) {
    pathNameParts[positionIdx] = pathComponent;
  } else {
    pathNameParts.push(pathComponent);
  }

  return pathNameParts.join("/");
};

/**
 * Tests a String for being a valid encoded view center encoded.
 * @param x The string.
 * @returns {boolean | *}
 */
export const isViewPath = x => x.startsWith('@') && x.endsWith('z');

/**
 * Encodes a map view center as a String.
 * @param lon
 * @param lat
 * @param zoom
 * @returns {string}
 */
export const mapCenterToPath = ([lon, lat], zoom) => {
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
export const pathToMapCenter = path => {
  const str = path.trim();
  const [lng, lat, zoom] = path.slice(1, str.length - 1).split(',');
  return {
    center: [lat, lng],
    zoom,
  };
};

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
