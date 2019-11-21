import { mapStateToPath, pathToMapState } from './utils';

const defaultMapCenter = { lng: 13.6811, lat: 51.0526 };
const defaultMapZoom = 8;

export default {

  state: {
    syncingMapState: false,
    mapCenter: defaultMapCenter,
    mapZoom: defaultMapZoom,
    mapMaxBounds: [{ lng: -10.0, lat: 35.0 }, { lng: 30.0, lat: 65.0 }],
    latestMapCenter: defaultMapCenter,
    latestMapZoom: defaultMapZoom
  },

  getters: {
    mapStatePath: state => {
      return mapStateToPath(state.latestMapCenter, state.latestMapZoom);
    }
  },

  mutations: {
    logMapState: state => {
      const route = state.route;
      if (route.params.mapStatePath) {
        const { center, zoom } = pathToMapState(route.params.mapStatePath);
        state.syncingMapState = true;
        state.mapCenter = center;
        state.mapZoom = zoom;
      }
    },

    syncMapState: state => {
      const route = state.route;
      if (route.params.mapStatePath) {
        const { center, zoom } = pathToMapState(route.params.mapStatePath);
        state.syncingMapState = true;
        state.mapCenter = center;
        state.mapZoom = zoom;
      }
    },

    endSyncMapState: state => {
      state.syncingMapState = false;
    }
  }

};
