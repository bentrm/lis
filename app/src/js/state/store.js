import Vue from 'vue';
import Vuex from 'vuex';
import { fetchMemorial, fetchPage, fetchAuthor, levels } from './actions';
import api from '../Api';
import { pathToMapState } from '../utils';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
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

    SET_CURRENT_PAGE(state, { page }) {
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

    async [fetchPage]({ commit, state }, { slug }) {
      let page = state.page.bySlug[slug];

      if (!page) {
        page = await api.getPage(slug);
        commit('ADD_PAGE_BY_SLUG', { slug, page });
      }

      commit('SET_CURRENT_PAGE', { page });
    }
  }
});
