import 'core-js/stable';
import 'regenerator-runtime/runtime';
import Vue from 'vue';
import Meta from 'vue-meta';
import VueRouter from 'vue-router';
import {
  AlertPlugin,
  ButtonGroupPlugin,
  ButtonPlugin,
  CardPlugin,
  CollapsePlugin,
  FormInputPlugin,
  ImagePlugin,
  InputGroupPlugin,
  LayoutPlugin,
  LinkPlugin,
  MediaPlugin,
  ModalPlugin,
  NavbarPlugin,
  PaginationPlugin,
  PopoverPlugin,
  TabsPlugin,
} from 'bootstrap-vue/dist/bootstrap-vue.esm';
import {dom} from '@fortawesome/fontawesome-svg-core';
import {Icon} from 'leaflet';
import router from './router';
import store from './state/store';
import './icons';
import AppView from './views/AppView.vue';

// this part resolve an issue where the markers would not appear
delete Icon.Default.prototype._getIconUrl;

Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png')
});

Vue.use(Meta);
Vue.use(VueRouter);
Vue.use(AlertPlugin);
Vue.use(ButtonGroupPlugin);
Vue.use(ButtonPlugin);
Vue.use(CardPlugin);
Vue.use(CollapsePlugin);
Vue.use(FormInputPlugin);
Vue.use(ImagePlugin);
Vue.use(InputGroupPlugin);
Vue.use(LayoutPlugin);
Vue.use(LinkPlugin);
Vue.use(MediaPlugin);
Vue.use(ModalPlugin);
Vue.use(NavbarPlugin);
Vue.use(PaginationPlugin);
Vue.use(PopoverPlugin);
Vue.use(TabsPlugin);

const AppComponent = Vue.extend(AppView);

new AppComponent({
  store,
  router
}).$mount('#App');

dom.watch();
