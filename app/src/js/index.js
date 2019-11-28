import 'core-js/stable';
import 'regenerator-runtime/runtime';
import Vue from 'vue';
import Meta from 'vue-meta';
import VueRouter from 'vue-router';
import Vuex from 'vuex';
import { sync } from 'vuex-router-sync';
import { CardPlugin, ModalPlugin, MediaPlugin, NavbarPlugin, PopoverPlugin, TabsPlugin, ImagePlugin } from 'bootstrap-vue/dist/bootstrap-vue.esm';
import { dom } from '@fortawesome/fontawesome-svg-core';
import { Icon } from 'leaflet'
import routes from './routes';
import context from './context';
import './icons';
import App from './components/App.vue';

// this part resolve an issue where the markers would not appear
delete Icon.Default.prototype._getIconUrl;

Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png')
});

Vue.use(Meta);
Vue.use(Vuex);
Vue.use(VueRouter);
Vue.use(CardPlugin);
Vue.use(PopoverPlugin);
Vue.use(ModalPlugin);
Vue.use(NavbarPlugin);
Vue.use(TabsPlugin);
Vue.use(MediaPlugin);
Vue.use(ImagePlugin);

const store = new Vuex.Store(context);
const router = new VueRouter(routes);
const AppComponent = Vue.extend(App);

sync(store, router);

new AppComponent({
  store,
  router
}).$mount('#App');

dom.watch();
