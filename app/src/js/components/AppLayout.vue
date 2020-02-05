<template>
  <div class="App container-fluid">
    <div class="row">
      <div class="col p-0">
        <sponsor-bar></sponsor-bar>
      </div>
    </div>
    <div class="row">
      <div class="col p-0">
        <navbar></navbar>
      </div>
    </div>
    <div class="row">
      <div class="col p-0">
        <router-view></router-view>
      </div>
    </div>
    <div class="row">
      <div class="col p-0">
        <app-footer></app-footer>
      </div>
    </div>
  </div>
</template>

<script>
  import Navbar from './Navbar.vue';
  import SponsorBar from './SponsorBar.vue';
  import AppFooter from './AppFooter.vue';

  export default {
    components: {
      AppFooter,
      Navbar,
      SponsorBar
    }
  };
</script>
