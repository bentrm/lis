<template>
  <div class="root">

  <div class="App d-flex flex-column">

    <sponsor-bar></sponsor-bar>

    <navbar></navbar>

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
  import translate from '../translate';
  import Navbar from './Navbar.vue';
  import SponsorBar from './SponsorBar.vue';


  export default {
    components: {
      Navbar,
      SponsorBar,
    },
    filters: {
      translate,
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
