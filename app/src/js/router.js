import Vue from 'vue';
import Router from 'vue-router';
import AuthorDetailView from './views/AuthorDetailView.vue';
import AuthorListView from './views/AuthorListView.vue';
import BlogPageView from './views/BlogPageView.vue';
import MapView from './views/MapView.vue';
import MemorialCardView from './views/MemorialCardView.vue';
import SearchView from './views/SearchView.vue';

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
    path: '/search',
    name: 'search',
    component: SearchView
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
      component: MemorialCardView
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
    component: AuthorDetailView,
    children: [
      {
        path: 'memorial/:memorialId',
        name: 'author-memorial-detail',
        component: MemorialCardView
      }
    ]
  }, {
    path: '*',
    redirect: {name: 'index'}
  }]
});

export default router;
