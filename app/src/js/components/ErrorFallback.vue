<template>
  <div>
    <h1 class="mt-4">404: {{ 'Page not found.' | translate }}</h1>
    <p>
      <router-link :to="{name: 'index'}">{{ 'Back to homepage.' | translate }}</router-link>
    </p>
  </div>
</template>

<script>
  import translate from '../translate';

  export default {
    filters: {
      translate,
    }
  }
</script>
