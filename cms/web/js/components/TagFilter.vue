<template>
  <div class="form-group">
    <label :for="id">
      {{ label }}
    </label>
    <input
      :id="id"
      :name="id"
      class="content-filter"
      type="text"
    >
  </div>
</template>

<script>
  import Tagify from '@yaireo/tagify';


  export default {
    props: ['api', 'id', 'label', 'param', 'path'],
    mounted: function () {
      const vm = this;

      vm.$nextTick(() => {
        const element = document.querySelector(`input#${vm.id}`);
        this.tagify = new Tagify(element, {
          dropdown: {
            enabled: 0,
            classname: 'filter-suggestion-list'
          },
          enforceWhitelist: true,
          readonly: true,
          whitelist: [],
        });

        this.tagify.on('add', this.emitChange);
        this.tagify.on('remove', this.emitChange);

        vm.getTags();
      });
    },
    methods: {
      getTags: function () {
        const vm = this;
        vm.api
          .getResults(this.path, {limit: 1000})
          .then(response => {
            this.tagify.settings.whitelist = response.results.map(({id, title}) => {
              return {
                code: id,
                value: title
              };
            });
          });
      },
      emitChange: function () {
        const value = this.tagify.value.map(x => x.code);
        this.$emit('change', this.param, value);
      }
    }
  };
</script>
