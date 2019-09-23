import {icon, layer} from '@fortawesome/fontawesome-svg-core';
import {
  faArchive,
  faBirthdayCake,
  faBook,
  faBuilding,
  faChurch,
  faCross,
  faGraduationCap,
  faInfo,
  faLandmark,
  faLightbulb,
  faMapMarker,
  faMonument,
  faMountain,
  faPalette,
  faRoad,
  faSquare
} from '@fortawesome/free-solid-svg-icons';


const symbols = {
  16: faBuilding,
  17: faRoad,
  18: faBirthdayCake,
  19: faBuilding,
  20: faCross,
  21: faLightbulb,
  22: faMonument,
  23: faMonument,
  24: faSquare,
  25: faLandmark,
  26: faGraduationCap,
  27: faChurch,
  28: faMountain,
  29: faMonument,
  30: faPalette,
  31: faInfo,
  32: faPalette,
  33: faBook,
  34: faArchive
};

/**
 * Generates a new font awesome svg layer mapping a symbol id to a fa overlay icon.
 * @param symbolId
 * @returns {Layer}
 */
export default (symbolId) => {
  const symbol = symbols[symbolId] || faMonument;

  return layer(push => {
    push(icon(faMapMarker, {
      styles: {'color': '#69140e'},
      transform: {size: 48, x: 0, y: 0},
    }));
    push(icon(symbol, {
      styles: {'color': 'white'},
      transform: {x: 0, y: -4, size: 16}
    }));
  }, {
    classes: ['fa-fw', 'fa-leaflet-layer', 'drop-shadow']
  });
};
