<template>
  <author-detail
    v-if="author"
    :author="author"
    :memorials="memorials"
    :level="$route.params.level"
    :current-level="currentLevel"
    :current-memorial="currentMemorial">
  </author-detail>
</template>

<script>
  import AuthorDetail from '../components/AuthorDetail.vue';
  import api from '../Api';

  export default {

    data() {
      return {
        author: null,
        memorials: [],
        currentLevel: null,
        currentMemorial: null
      };
    },

    components: {
      AuthorDetail
    },

    metaInfo() {
      const vm = this;
      const {author} = vm;
      if (author) {
        return {
          title: [author.first_name, author.last_name].join(' ')
        };
      }
    },

    async beforeRouteEnter(to, from, next) {
      const {slug: slugParam, level: levelParam, memorialId: memorialIdParam} = to.params;
      const author = await api.getAuthor(slugParam);
      const memorials = await api.getMemorials({ author: author.id }).then(json => json.results);
      const currentLevel = await api.getLevel(slugParam, levelParam);
      const currentMemorial = memorialIdParam ? await api.getMemorial(memorialIdParam) : null;

      return next(vm => {
        vm.author = author;
        vm.memorials = memorials;
        vm.currentLevel = currentLevel;
        vm.currentMemorial = currentMemorial;
      });
    },

    async beforeRouteUpdate(to, from, next) {
      const vm = this;
      const {slug: fromSlugParam, level: fromLevelParam, memorialId: fromMemorialIdParam} = from.params;
      const {slug: toSlugParam, level: toLevelParam, memorialId: toMemorialIdParam} = to.params;

      let newSlug = fromSlugParam !== toSlugParam;
      if (newSlug) {
        vm.author = await api.getAuthor(toSlugParam);
        vm.memorials = await api.getMemorials({ author: author.id }).then(json => json.results);
        vm.currentLevel = await api.getLevel(toSlugParam, toLevelParam);
      }
      if (fromLevelParam !== toLevelParam && !newSlug) {
        vm.currentLevel = await api.getLevel(toSlugParam, toLevelParam);
      }
      if (fromMemorialIdParam !== toMemorialIdParam) {
        vm.currentMemorial = toMemorialIdParam ? await api.getMemorial(toMemorialIdParam) : null;
      }

      return next();
    }
  };
</script>
