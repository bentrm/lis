<template>
  <div class="container">
    <div class="row">
      <div class="col">
        <h1 class="mt-4">{{ '404: Page not found.' | translate }}</h1>
        <p>
          <router-link
            class="navbar-brand"
            :to="{name: 'blog-page'}"
          >{{ 'Back to homepage.' | translate }}</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import translate from '../translate';

export default {
  filters: {
    translate
  }
};
</script>
