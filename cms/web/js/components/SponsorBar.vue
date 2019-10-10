<template>
  <div class="navbar navbar-light">
    <span class="small d-none d-sm-block">
      Gefördert durch<br>
      Podpořeno
    </span>

    <a class="navbar-brand ml-md-auto" href="http://www.sn-cz2020.eu/" target="_blank" rel="noopener">
      <img :src="euLogo" alt="Logo EU Fonds" class="sponsor-logo img img-fluid">
      <img :src="snczLogo" alt="Logo SN CZ" class="sponsor-logo img img-fluid">
    </a>
  </div>
</template>

<script>
  import euLogo from '../../assets/logos/logo_eu.svg';
  import snczLogo from '../../assets/logos/logo_sn_cz.svg';


  export default {
    data () {
      return {
        euLogo,
        snczLogo
      };
    }
  }
</script>

<style lang="scss">
  .sponsor-logo {
    max-height: 2.5rem;
  }
</style>
