<template>
  <span>{{ formattedDate }}</span>
</template>

<script>
  import {getCurrentLanguage} from '../translate';


  export default {
    props: {
      day: Number,
      month: Number,
      year: Number,
      place: String
    },

    computed: {
      formattedDate () {
        const vm = this;
        let output = '';
        if (vm.year && vm.month && vm.day) {
          output += new Date(vm.year, (vm.month - 1), vm.day).toLocaleDateString(getCurrentLanguage());
        }
        if (vm.place) {
          output += ` (${vm.place})`;
        }
        return output;
      }
    }
  }
</script>
