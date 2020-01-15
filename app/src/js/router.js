import Vue from 'vue';
import Router from 'vue-router';
import AuthorDetailView from './components/AuthorDetailView.vue';
import AuthorListView from './components/AuthorListView.vue';
import BlogPageView from './components/BlogPageView.vue';
import MapView from './components/MapView.vue';
import MemorialCard from './components/MemorialCard.vue';

Vue.use(Router);

const router = new Router({
  mode: 'history',
  routes: [{
    path: '/',
    name: 'index',
    component: BlogPageView
  }, {
    path: '/page/:slug',
    name: 'blog-page',
    component: BlogPageView
  }, {
    path: '/map/',
    redirect: '/map/@13.5901,50.7121,8z'
  }, {
    path: '/map/:mapStatePath',
    component: MapView,
    name: 'map',
    props: true,
    children: [{
      path: 'memorial/:memorialId',
      name: 'memorial-detail',
      component: MemorialCard
    }]
  }, {
    path: '/authors',
    component: AuthorListView,
    name: 'author-list',
  }, {
    path: '/authors/:slug',
    redirect: '/authors/:slug/discover',
  }, {
    path: '/authors/:slug/:level',
    name: 'author-detail',
    component: AuthorDetailView
  }, {
    path: '*',
    redirect: {name: 'index'}
  }]
});

export default router;
