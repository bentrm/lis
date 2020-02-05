<template>
  <span>{{ formattedDate }}</span>
</template>

<script>
  import moment from 'moment';
  import 'moment/locale/de';
  import 'moment/locale/cs';
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
          moment.locale(getCurrentLanguage());
          output += moment([vm.year, vm.month, vm.day]).format('LL');
        } else if (vm.year) {
          output += vm.year;
        }
        if (vm.place) {
          output += ` (${vm.place})`;
        }
        return output;
      }
    }
  }
</script>
