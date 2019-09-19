import VueRouter from 'vue-router/dist/vue-router.esm';
import Vue from 'vue/dist/vue.esm';
import MapFilter from './components/MapFilter.vue';
import MapView from './components/MapView.vue';
import MemorialCard from './components/MemorialCard.vue';
import api from './Api';


Vue.use(VueRouter);


export default new VueRouter({
  mode: 'history',
  routes: [{
    path: '/map/:mapState?',
    component: MapView,
    children: [{
      path: '',
      component: MapFilter,
      name: 'map',
      props: true,
    }, {
      path: 'memorial/:id',
      name: 'memorial-detail',
      component: MemorialCard,
      props (route) {
        const params = route.params;
        params.id = parseInt(params.id);
        return params;
      },
    }]
  }]
});

