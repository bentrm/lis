<template>
  <div class="form-group">
    <label :for="id">
      Author
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
    props: ['id', 'api'],
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

        vm.getAuthors();
      });
    },
    methods: {
      getAuthors: function () {
        const vm = this;
        vm.api
          .getAuthors(this.path, {ordering: 'last_name', limit: 1000})
          .then(response => {
            this.tagify.settings.whitelist = response.results.map(author => {
              const {id, first_name, last_name} = author;
              return {
                code: id,
                value: `${first_name} ${last_name}`
              };
            });
          });
      },
      emitChange: function () {
        const value = this.tagify.value.map(x => x.code);
        this.$emit('change', value);
      }
    }
  };
</script>

