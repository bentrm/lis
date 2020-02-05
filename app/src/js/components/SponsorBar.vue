<template>
  <div class="d-flex justify-content-between align-items-center px-3 py-0">
    <p class="small m-0 p-0">
      Gefördert durch
    <br />Podpořeno
    </p>

    <a
      class="p-0"
      href="http://www.sn-cz2020.eu/"
      target="_blank"
      rel="noopener"
    >
      <img
        :src="euLogo"
        alt="Logo EU Fonds"
        class="eu-logo img img-fluid"
        style="max-height: 2.5rem;"
      />
      <img
        :src="snczLogo"
        alt="Logo SN CZ"
        class="eu-logo img img-fluid"
        style="max-height: 4.5rem;"
      />
    </a>
  </div>
</template>

<script>
  import euLogo from '../../assets/logos/logo_eu.svg';
  import snczLogo from '../../assets/logos/logo_sn_cz.svg';

  export default {
  data() {
    return {
      euLogo,
      snczLogo
    };
  }
};
</script>
