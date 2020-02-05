<template>
  <div class="Author container mt-4">
    <div v-if="author" class="row">
      <author-profile :author="author"></author-profile>

      <div class="col-12">
        <b-button-group class="level-btn-group d-flex">
          <b-button
            v-if="author.levels.discover"
            :active="level === 'discover'"
            :to="{ params: {level: 'discover'}}"
            variant="primary"
          >{{'Discover' | translate}}
          </b-button>
          <b-button
            v-if="author.levels.research"
            :active="level === 'research'"
            :to="{ params: {level: 'research'}}"
            variant="primary"
          >{{'Research' | translate}}
          </b-button>
          <b-button
            v-if="author.levels.material"
            :active="level === 'material'"
            :to="{ params: {level: 'material'}}"
            variant="primary"
          >{{'Material' | translate}}
          </b-button>
        </b-button-group>
      </div>

      <div class="col-12">
        <h3 class="mt-2">{{ 'Content' | translate }}</h3>
        <ol>
          <li>
            <a href="#memorials">{{ 'Memorials' | translate }}</a>
          </li>
          <li v-for="[heading] in currentLevelParagraphs" :key="heading">
            <a :href="'#' + heading">{{ heading | humanize | capitalize | translate }}</a>
          </li>
        </ol>
      </div>

      <div v-if="level !== 'material'" class="col-12 mb-4">
        <h4 id="memorials" class="mt-2">{{ 'Memorials' | translate }}</h4>

        <ul class="list-unstyled">
          <li v-for="(memorial, index) in memorials" :key="memorial.id">
            <span v-if="currentMemorial && currentMemorial.id === memorial.id">
              <i class="fa-fw" :class="getMemorialIcon(memorial)"/>  {{ memorial.name }}
            </span>
            <b-link v-else :key="index"
                    :to="{ name: 'author-memorial-detail', params: {memorialId: memorial.id}}">
              <i class="fa-fw" :class="getMemorialIcon(memorial)"/> {{memorial.name}}
            </b-link>
          </li>
        </ul>

        <b-card id="current-memorial" v-if="currentMemorial" tag="article">
          <template v-slot:header>
            <div class="d-flex justify-content-between align-items-center">
              <div class="row">
                <div class="col-12 col-sm-3" v-if="currentMemorial.title_image">
                  <figure-image
                    :src="currentMemorial.title_image.mid"
                    :src-modal="currentMemorial.title_image.large"
                    :alt="currentMemorial.title_image.title"
                    :title="currentMemorial.title_image.title"
                    :captionModal="currentMemorial.title_image.caption"
                    :copyright="currentMemorial.title_image.copyright"
                  ></figure-image>
                </div>
                <div class="col">
                  <div class="d-flex justify-content-between align-items-center">
                    <h5 class="m-0 p-0">{{ currentMemorial.name }}</h5>
                    <b-button
                      :to="{name: 'memorial-detail', params: { memorialId: currentMemorial.id, mapStatePath: toPath(currentMemorial.position) }}">
                      <i class="fas fa-map-marker"></i>
                      {{ 'See on map' | translate }}
                    </b-button>
                  </div>
                  <div class="mt-2" v-if="currentMemorial.introduction"
                       v-html="currentMemorial.introduction"></div>

                </div>
              </div>
            </div>
          </template>
          <b-card-body>
            <paragraph
              v-if="level === 'discover' && currentMemorial.description.length"
              v-for="paragraph in currentMemorial.description"
              :key="paragraph.id"
              v-bind="paragraph.value"
            ></paragraph>
            <paragraph
              v-if="level === 'research' && currentMemorial.detailed_description.length"
              v-for="paragraph in currentMemorial.detailed_description"
              :key="paragraph.id"
              v-bind="paragraph.value"
            ></paragraph>
          </b-card-body>
          <template v-slot:footer v-if="currentMemorial.address || currentMemorial.contactInfo || currentMemorial.directions">
            <div class="row">
              <div class="col-12 col-sm-6 col-md-4" v-if="currentMemorial.address">
                <b>{{ 'Address' | translate }}</b>
                <address v-html="currentMemorial.address"></address>
              </div>
              <div class="col-12 col-sm-6 col-md-4" v-if="currentMemorial.contactInfo">
                <b>{{ 'Contact info' | translate }}</b>
                <div v-html="currentMemorial.contactInfo"></div>
              </div>
              <div class="col-12 col-sm-6 col-md-4" v-if="currentMemorial.directions">
                <b>{{ 'Directions' | translate }}</b>
                <i v-if="currentMemorial.directions" v-html="currentMemorial.directions"></i>
              </div>
            </div>
          </template>
        </b-card>
      </div>

      <author-article class="col-12" :content="currentLevelParagraphs"></author-article>
    </div>
  </div>
</template>

<script>
  import translate from '../translate';
  import {capitalize, humanize, humanizePosition, mapStateToPath, round} from '../utils';
  import AuthorArticle from '../components/AuthorArticle.vue';
  import Paragraph from '../components/Paragraph.vue';
  import CmsImage from '../components/CmsImage.vue';
  import AuthorProfile from './AuthorProfile.vue';
  import {iconClassName} from '../markers';
  import FigureImage from './FigureImage.vue';

  const ignoredProperties = ['id'];

  export default {

    props: {
      author: Object,
      memorials: Array,
      level: String,
      currentLevel: Object,
      currentMemorial: Object,
    },

    components: {
      AuthorProfile,
      FigureImage,
      CmsImage,
      AuthorArticle,
      Paragraph,
    },

    filters: {
      humanizePosition,
      humanize,
      translate,
      capitalize,
      round,
    },

    computed: {
      name() {
        const vm = this;
        return vm.author.also_known_as[0];
      },

      alternativeNames() {
        const vm = this;
        return vm.author.also_known_as.slice(1);
      },

      currentLevelParagraphs() {
        const vm = this;
        return Object.entries(vm.currentLevel || []).filter(
          ([heading, paragraphs]) => {
            return ignoredProperties.indexOf(heading) === -1 && paragraphs.length;
          },
        );
      },
    },

    methods: {
      getMemorialDetailRoute(id) {
        const vm = this;
        const {$route} = vm;
        return {
          name: 'author-memorial-detail',
          params: Object.assign({}, $route.params, {memorialId: id}),
          query: $route.query,
        };
      },

      getMemorialIcon(memorial) {
        return iconClassName(memorial.memorial_types[0].id);
      },

      toPath(position) {
        const [lng, lat] = position;
        return mapStateToPath({lng, lat});
      },
    },
  };
</script>

<style lang="scss">
  @import 'src/scss/variables';

  .Author {
    .blockquote {
      font-size: 1rem;
      border-right: 1px solid theme-color("primary");
      padding-right: 1rem;
      padding-left: 5rem;
    }

    .level-btn-group {
      margin-bottom: 20px;

      .btn.active::after {
        border-left: 15px solid transparent;
        border-right: 15px solid transparent;
        border-top: 15px solid darken(theme-color('primary'), 10%);
        bottom: -15px;
        content: ' ';
        left: calc(50% - 15px);
        position: absolute;
      }
    }
  }
</style>
