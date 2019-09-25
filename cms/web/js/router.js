import VueRouter from 'vue-router/dist/vue-router.esm';
import Vue from 'vue/dist/vue.esm';
import MapView from './components/MapView.vue';
import MemorialCard from './components/MemorialCard.vue';


Vue.use(VueRouter);

export default new VueRouter({
  mode: 'history',
  routes: [{
    path: '/map/:mapStatePath?',
    component: MapView,
    name: 'map',
    props: true,
    children: [{
      path: 'memorial/:memorialId',
      name: 'memorial-detail',
      component: MemorialCard,
    }]
  }]
});

