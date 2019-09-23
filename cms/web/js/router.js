import VueRouter from 'vue-router/dist/vue-router.esm';
import Vue from 'vue/dist/vue.esm';
import MapFilter from './components/MapFilter.vue';
import MapView from './components/MapView.vue';
import MemorialCard from './components/MemorialCard.vue';


Vue.use(VueRouter);

export default new VueRouter({
  mode: 'history',
  routes: [{
    path: '/map/:mapState?',
    component: MapView,
    props: true,
    children: [{
      path: '',
      component: MapFilter,
      name: 'map',
      props: true,
    }, {
      path: 'memorial/:id',
      name: 'memorial-detail',
      component: MemorialCard,
      props: true,
    }]
  }]
});

