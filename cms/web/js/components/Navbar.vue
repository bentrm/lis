<template>
  <div class="MainNav">
    <header class="navbar navbar-expand-lg navbar-dark bg-primary">
      <router-link
        class="navbar-brand"
        :to="{name: 'blog-page'}"
      >
        <i
          class="fas fa-globe"
          data-fa-transform="shrink-10 up-2"
          data-fa-mask="fas fa-bookmark"></i>
        {{ 'Literary landscape' | translate }}
      </router-link>

      <button
        class="navbar-toggler ml-auto"
        type="button"
        data-toggle="collapse"
        data-target="#headerMenu">
        <i class="fas fa-bars"></i>
      </button>

      <div class="collapse navbar-collapse" id="headerMenu">
        <ul class="navbar-nav">
          <li class="nav-item">
            <router-link class="nav-link" :to="{name: 'map'}">{{ 'Map' | translate }}</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" :to="{name: 'author-list'}">{{ 'Authors' | translate }}</router-link>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" data-toggle="dropdown" href="#" role="button">{{ 'More' | translate }}</a>
            <div class="dropdown-menu">
              <router-link class="dropdown-item" :to="{name: 'blog-page', params: { slug: 'about' }}">{{ 'About' | translate }}</router-link>
              <router-link class="dropdown-item" :to="{name: 'blog-page', params: { slug: 'imprint' }}">{{ 'Imprint & data protection' | translate }}</router-link>
              <a class="dropdown-item" href="/admin">{{ 'Admin' | translate }}</a>
            </div>
          </li>

          <li class="nav-item dropdown">
            <form action="/i18n/setlang/" method="POST">
              <input type="hidden" name="csrfmiddlewaretoken" :value="csrfToken">
              <input type="hidden" name="next" value="">

              <a class="nav-link dropdown-toggle" data-toggle="dropdown" href="#" role="button">{{ selectedLanguage.name }}</a>
              <div class="dropdown-menu">
                <button
                  v-for="(name, code) in languages"
                  name="language"
                  :value="code"
                  type="submit"
                  class="dropdown-item"
                >
                  {{ name }}
                </button>
              </div>
            </form>
          </li>
        </ul>

        <search-bar class="flex-grow-1"></search-bar>
      </div>
    </header>
  </div>
</template>

<script>
  import translate, {currentLanguage} from '../translate';
  import SearchBar from './SearchBar.vue';


  export default {
    components: { SearchBar },

    filters: { translate },

    data () {
      return {
        languages: {
          en: 'English',
          de: 'Deutsch',
          cs: 'Česky',
        }
      };
    },

    computed: {

      selectedLanguage () {
        let code = currentLanguage();
        let name = this.languages[code];
        return {code, name};
      },

      next () {
        return window.location.href;
      },

      csrfToken () {
        const cookies = document.cookie;
        const dict = cookies.split(';').reduce((acc, cur) => {
          const [key, value] = cur.trim().split('=');
          acc[key] = value;
          return acc;
        }, {});
        return dict.csrftoken || '';
      }
    },
  }
</script>

<style lang="scss">

</style>
