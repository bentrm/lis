<template>
  <div class="root">

  <div class="App d-flex flex-column">

    <sponsor-bar></sponsor-bar>

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

    <router-view></router-view>
  </div>

  <div class="Footer">
    <div class="container-fluid">
      <div class="row">
        <div class="col-12">
          <router-link :to="{name: 'blog-page', params: { slug: 'partner'}}" class="small d-none d-sm-block">{{ 'Project partner' | translate }}</router-link>
        </div>
        <div class="col-12 row justify-content-center">
          <div class="col-12 col-sm-6 col-md-4 d-flex justify-content-center align-items-center">
            <router-link :to="{name: 'blog-page', params: { slug: 'tu-dresden' }}" class="stretched-link">
              <img src="/static/app/files/logo_tu_dresden.svg" alt="TU Dresden" class="partner-logo img-fluid d-block m-2">
            </router-link>
          </div>
          <div class="col-12 col-sm-6 col-md-4 d-flex justify-content-center align-items-center">
            <router-link :to="{name: 'blog-page', params: { slug: 'tu-liberec' }}" class="stretched-link">
              <img src="/static/app/files/logo_tu_liberec.svg" alt="TU Liberec" class="partner-logo img-fluid d-block m-2">
            </router-link>
          </div>
          <div class="col-12 col-sm-6 col-md-4 d-flex justify-content-center align-items-center">
            <router-link :to="{name: 'blog-page', params: { slug: 'htw-dresden' }}" class="stretched-link">
              <img src="/static/app/files/logo_htw_dresden.svg" alt="HTW Dresden" class="partner-logo img-fluid d-block m-2">
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
  </div>
</template>

<script>
  import '../../assets/logos/logo_htw_dresden.svg';

  import '../../assets/logos/logo_tu_dresden.svg';
  import '../../assets/logos/logo_tu_liberec.svg';
  import router from '../router';
  import translate, {currentLanguage} from '../translate';
  import SearchBar from './SearchBar.vue';
  import SponsorBar from './SponsorBar.vue';


  export default {
    components: {
      SearchBar,
      SponsorBar,
    },
    filters: {
      translate,
    },
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
      },
    },
    router
  }
</script>

<style lang="scss">
  @import '../../scss/variables';

  .partner-logo {
    max-height: 2.5rem;
  }

  .Footer {
    padding-top: 1rem;
    padding-bottom: 3rem;
    border-top: .8rem solid theme-color("primary");
  }
</style>
