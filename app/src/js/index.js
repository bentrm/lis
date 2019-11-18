import { dom } from '@fortawesome/fontawesome-svg-core';
import { CardPlugin, ModalPlugin, MediaPlugin, NavbarPlugin, PopoverPlugin, TabsPlugin, ImagePlugin } from 'bootstrap-vue';
import Meta from 'vue-meta';
import 'core-js/stable';
import 'regenerator-runtime/runtime';
import VueRouter from 'vue-router';
import Vue from 'vue/dist/vue.esm';
import '../scss/main.scss';
import App from './components/App.vue';
import './icons';

import { Icon } from 'leaflet'
import 'leaflet/dist/leaflet.css'


// this part resolve an issue where the markers would not appear
delete Icon.Default.prototype._getIconUrl;

Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png')
});

Vue.use(VueRouter);
Vue.use(Meta);
Vue.use(CardPlugin);
Vue.use(PopoverPlugin);
Vue.use(ModalPlugin);
Vue.use(NavbarPlugin);
Vue.use(TabsPlugin);
Vue.use(MediaPlugin);
Vue.use(ImagePlugin);

const AppComponent = Vue.extend(App);

new AppComponent().$mount('#App');
dom.watch();
