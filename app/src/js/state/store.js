import Vue from 'vue';
import Vuex from 'vuex';
import translate from '../translate';
import { fetchMemorial, fetchPage, fetchAuthor, levels } from './actions';
import api from '../Api';
import { pathToMapState } from '../utils';

Vue.use(Vuex);

const defaultMapCenter = { lng: 13.6811, lat: 51.0526 };
const defaultMapZoom = 8;

export default new Vuex.Store({
  state: {
    // deprecated
    syncingMapState: false,
    mapCenter: defaultMapCenter,
    mapZoom: defaultMapZoom,
    mapMaxBounds: [{ lng: -10.0, lat: 35.0 }, { lng: 30.0, lat: 65.0 }],
    latestMapCenter: defaultMapCenter,
    latestMapZoom: defaultMapZoom,
    // -

    memorial: {
      current: null,
      byId: {}
    },

    author: {
      current: null,
      detail: null,
      memorials: null,
      bySlug: {}
    },

    level: {
      discover: {},
      research: {},
      material: {}
    },

    page: {
      error: false,
      current: null,
      bySlug: {}
    },

    map: {
      center: {
        lat: 51.0526,
        lng: 13.6811,
      },
      zoom: 8,
      maxBounds: [
        { lng: -10.0, lat: 35.0 },
        { lng: 30.0, lat: 65.0 }
      ]
    }
  },

  mutations: {
    // deprecated
    logMapState (state, {route}) {
      if (route.params.mapStatePath) {
          const { center, zoom } = pathToMapState(route.params.mapStatePath);
          state.syncingMapState = true;
          state.mapCenter = center;
          state.mapZoom = zoom;
        }
    },

    syncMapState(state, {route}) {
      if (route.params.mapStatePath) {
          const { center, zoom } = pathToMapState(route.params.mapStatePath);
          state.syncingMapState = true;
          state.mapCenter = center;
          state.mapZoom = zoom;
        }
    },

    endSyncMapState: state => {
      state.syncingMapState = false;
    },
    // -

    ADD_MEMORIAL_BY_ID(state, { id, memorial }) {
      state.memorial.byId[id] = memorial;
    },

    SET_CURRENT_MEMORIAL(state, { memorial }) {
      state.memorial.current = memorial;
    },

    ADD_AUTHOR_BY_SLUG(state, { slug, author }) {
      state.author.bySlug[slug] = author;
    },

    SET_CURRENT_AUTHOR(state, { author, detail, memorials }) {
      state.author.current = author;
      state.author.detail = detail;
      state.author.memorials = memorials;
    },

    ADD_LEVEL_BY_SLUG(state, { slug, level, detail }) {
      state.level[level][slug] = detail;
    },

    ADD_PAGE_BY_SLUG(state, { slug, page }) {
      state.page.bySlug[slug] = page;
    },

    SET_CURRENT_PAGE(state, { page, error }) {
      state.page.error = error;
      state.page.current = page;
    },

    RESET_MAP_STATE(state) {
      const path = state.route.params.mapStatePath;
      const mapState = pathToMapState(path);
      state.map = { ...state.map, ...mapState };
    }
  },

  actions: {
    async [fetchMemorial]({ commit, state }, { id }) {
      let memorial = state.memorial.byId[id];

      if (!memorial) {
        memorial = await api.getMemorial(id);
        commit('ADD_MEMORIAL_BY_ID', { id, memorial });
      }

      commit('SET_CURRENT_MEMORIAL', { memorial });
    },

    async [fetchAuthor]({ commit, state }, { slug, level = levels.discover }) {
      let author = state.author.bySlug[slug];
      let detail = state.level[level][slug];

      if (!author) {
        author = await api.getAuthor(slug);
        commit('ADD_AUTHOR_BY_SLUG', { slug, author });
      }

      if (!detail) {
        detail = await api.getLevel(slug, level);
        commit('ADD_LEVEL_BY_SLUG', { slug, level, detail });
      }

      const memorials = await api
        .getMemorials({ author: author.id, limit: 100 })
        .then(json => json.results);

      commit('SET_CURRENT_AUTHOR', { author, detail, memorials });
    },

    [fetchPage]({ commit, state }, { slug }) {
      let page = state.page.bySlug[slug];

      if (!page) {
        return api
          .getPage(slug)
          .then(page => commit('ADD_PAGE_BY_SLUG', { slug, page }))
          .then(() => commit('SET_CURRENT_PAGE', { page: state.page.bySlug[slug], error: false }))
          .catch(() => commit('SET_CURRENT_PAGE', {page: null, error: true}));
      } else {
        return commit('SET_CURRENT_PAGE', { page });
      }

    }
  }
});
