import 'core-js/stable';
import 'regenerator-runtime/runtime';
import Vue from 'vue';
import Meta from 'vue-meta';
import VueRouter from 'vue-router';
import { ButtonPlugin, ButtonGroupPlugin, CardPlugin, CollapsePlugin, ModalPlugin, MediaPlugin, NavbarPlugin, PopoverPlugin, TabsPlugin, ImagePlugin } from 'bootstrap-vue/dist/bootstrap-vue.esm';
import { dom } from '@fortawesome/fontawesome-svg-core';
import { Icon } from 'leaflet'
import router from './router';
import store from './state/store';
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
Vue.use(VueRouter);
Vue.use(ButtonPlugin);
Vue.use(ButtonGroupPlugin);
Vue.use(CardPlugin);
Vue.use(CollapsePlugin);
Vue.use(PopoverPlugin);
Vue.use(ModalPlugin);
Vue.use(NavbarPlugin);
Vue.use(TabsPlugin);
Vue.use(MediaPlugin);
Vue.use(ImagePlugin);

const AppComponent = Vue.extend(App);

new AppComponent({
  store,
  router
}).$mount('#App');

dom.watch();
