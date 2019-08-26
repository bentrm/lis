import Vue from 'vue/dist/vue.esm';
import {debounce} from '../utils';


Vue.component('search-filter', {
  props: ['id', 'label', 'param', 'placeholder'],
  template: '#search-filter-template',
  methods: {
    onInput: debounce(function(e) {
      const input = e.target;
      this.$emit('change', this.param, input.value);
    }, 500)
  }
});
