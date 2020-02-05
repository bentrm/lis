<template>
  <div v-if="labels.length">
    <dt>{{ title | translate }}</dt>
    <dd>
      <span v-for="{id, name} in labels" :key="id" class="badge badge-pill badge-secondary mr-1"
            v-html="name"/>
    </dd>
  </div>
</template>

<script>
  import translate from '../translate';

  export default {
    props: {
      title: String,
      labels: Array,
    },

    filters: {
      translate,
    },
  };
</script>
