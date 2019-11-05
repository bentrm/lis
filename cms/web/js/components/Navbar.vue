<template>
  <div class="MainNav">
    <b-navbar toggleable="lg" type="dark" variant="primary">
      <b-navbar-brand :to="{name: 'blog-page'}">
        <i class="fas fa-globe" data-fa-transform="shrink-10 up-2" data-fa-mask="fas fa-bookmark"></i>
        {{ 'Literary landscape' | translate }}
      </b-navbar-brand>

      <b-navbar-toggle target="header-menu">
        <i class="fas fa-bars"></i>
      </b-navbar-toggle>

      <b-collapse id="header-menu" is-nav>
        <b-navbar-nav>
          <b-nav-item :to="{name: 'map'}">{{ 'Map' | translate }}</b-nav-item>
          <b-nav-item :to="{name: 'author-list'}">{{ 'Authors' | translate }}</b-nav-item>
          <b-nav-item-dropdown :text="'More' | translate">
            <b-dropdown-item
              :to="{name: 'blog-page', params: { slug: 'about' }}"
            >{{ 'About' | translate }}</b-dropdown-item>
            <b-dropdown-item
              :to="{name: 'blog-page', params: { slug: 'imprint' }}"
            >{{ 'Imprint & data protection' | translate }}</b-dropdown-item>
            <b-dropdown-item href="/admin">{{ 'Admin' | translate }}</b-dropdown-item>
          </b-nav-item-dropdown>

          <form action="/i18n/setlang/" method="POST">
            <input type="hidden" name="csrfmiddlewaretoken" :value="csrfToken" />
            <input type="hidden" name="next" :value="$route.fullPath" />
            <b-nav-item-dropdown :text="selectedLanguage.name">
              <button
                v-for="(name, code) in languages"
                name="language"
                :key="code"
                :value="code"
                type="submit"
                class="dropdown-item"
              >{{ name }}</button>
            </b-nav-item-dropdown>
          </form>
        </b-navbar-nav>

        <search-bar class="flex-grow-1"></search-bar>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<script>
import translate, { currentLanguage } from '../translate';
import SearchBar from './SearchBar.vue';

export default {
  components: { SearchBar },
  filters: { translate },

  data() {
    return {
      languages: {
        en: 'English',
        de: 'Deutsch',
        cs: 'Česky'
      }
    };
  },

  computed: {
    selectedLanguage() {
      let code = currentLanguage();
      let name = this.languages[code];
      return { code, name };
    },

    csrfToken() {
      const cookies = document.cookie;
      const dict = cookies.split(';').reduce((acc, cur) => {
        const [key, value] = cur.trim().split('=');
        acc[key] = value;
        return acc;
      }, {});
      return dict.csrftoken || '';
    }
  }
};
</script>

<style lang="scss">
</style>
