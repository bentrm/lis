import {dom} from '@fortawesome/fontawesome-svg-core';
import {ModalPlugin, NavbarPlugin, PopoverPlugin} from 'bootstrap-vue';
import 'core-js/stable';
import 'regenerator-runtime/runtime';
import VueRouter from 'vue-router';
import Vue from 'vue/dist/vue.esm';
import '../scss/main.scss';
import App from './components/App.vue';
import './icons';


Vue.use(VueRouter);
Vue.use(PopoverPlugin);
Vue.use(ModalPlugin);
Vue.use(NavbarPlugin);

const AppComponent = Vue.extend(App);

new AppComponent().$mount('#App');
dom.watch();
