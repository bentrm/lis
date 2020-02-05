<template>
  <MemorialCard
    :title="current.title"
    :image="current.image"
    :position="current.position"
    :authors="current.authors"
    :address="current.address"
    :contactInfo="current.contactInfo"
    :directions="current.directions"
    :introduction="current.introduction"
    :description="current.description"
    :detailedDescription="current.detailedDescription" />
</template>


<script>
  import MemorialCard from '../components/MemorialCard.vue';
  import {fetchMemorial} from '../state/actions';
  import store from '../state/store';

  export default {

    components: {
      MemorialCard,
    },

    beforeRouteEnter(to, from, next) {
      const memorialId = to.params.memorialId;
      store.dispatch(fetchMemorial, {id: memorialId}).then(() => next());
    },

    beforeRouteUpdate(to, from, next) {
      const memorialId = to.params.memorialId;
      store.dispatch(fetchMemorial, {id: memorialId}).then(() => next());
    },

    computed: {
      current() {
        return store.state.memorial.current;
      }
    },
  };
</script>
