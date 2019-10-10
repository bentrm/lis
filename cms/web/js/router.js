import VueRouter from 'vue-router/dist/vue-router.esm';
import AuthorDetailView from './components/AuthorDetailView.vue';
import AuthorListView from './components/AuthorListView.vue';
import BlogPageView from './components/BlogPageView.vue';
import MapView from './components/MapView.vue';
import MemorialCard from './components/MemorialCard.vue';


export default new VueRouter({
  mode: 'history',
  routes: [{
    path: '/map/:mapStatePath?/',
    pathToRegexpOptions: {
      strict: true,
    },
    component: MapView,
    name: 'map',
    props: true,
    children: [{
      path: 'memorial/:memorialId/',
      name: 'memorial-detail',
      component: MemorialCard
    }]
  }, {
    path: '/authors/',
    component: AuthorListView,
    name: 'author-list',
  }, {
    path: '/authors/:slug/:level?',
    name: 'author-detail',
    component: AuthorDetailView,
    props: route => {
      return {
        slug: route.params.slug,
        currentLevel: route.params.level || 'discover'
      };
    }
  }, {
    path: '/:slug?/',
    name: 'blog-page',
    component: BlogPageView,
    props: route => {
      return {
        slug: route.params.slug || 'homepage'
      };
    }
  }]
});

