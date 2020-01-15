<template>
  <div class="container mt-4">
    <div v-if="author" class="row">
      <div class="col" v-if="author.title_image">
        <figure-image
          :src="author.title_image.mid"
          :src-modal="author.title_image.large"
          :alt="author.title_image.title"
          :title="author.title_image.title"
          :caption="author.title_image.caption"
          :captionModal="author.title_image.caption"
          :copyright="author.title_image.copyright"
        ></figure-image>
      </div>

      <div class="col-12 col-sm-8">
        <h3 class="mt-0">{{ name }}</h3>

        <dl>
          <template v-if="author.also_known_as.length">
            <dt>{{ 'Also known as' | translate }}</dt>
            <dd
              v-for="({is_pseudonym, title, first_name, last_name}, index) in author.also_known_as"
              :key="index"
            >{{ title }} {{ first_name }} {{ last_name }}</dd>
          </template>

          <template v-if="author.yob">
            <dt>{{ 'Born' | translate }}</dt>
            <dd>
              <pretty-date
                :year="author.yob"
                :month="author.mob"
                :day="author.dob"
                :place="author.pob"
              ></pretty-date>
            </dd>
          </template>

          <template v-if="author.yod">
            <dt>{{ 'Died' | translate }}</dt>
            <dd>
              <pretty-date
                :year="author.yod"
                :month="author.mod"
                :day="author.dod"
                :place="author.pod"
              ></pretty-date>
            </dd>
          </template>

          <template v-if="author.languages.length">
            <dt>{{ 'Languages' | translate }}</dt>
            <dd>
              <span
                v-for="{id, name} in author.languages"
                :key="id"
                class="badge badge-pill badge-secondary mr-1"
              >{{ name }}</span>
            </dd>
          </template>

          <template v-if="author.genres.length">
            <dt>{{ 'Genres' | translate }}</dt>
            <dd>
              <span
                v-for="{id, name} in author.genres"
                :key="id"
                class="badge badge-pill badge-secondary mr-1"
              >{{ name }}</span>
            </dd>
          </template>

          <template v-if="author.periods.length">
            <dt>{{ 'Periods' | translate }}</dt>
            <dd>
              <span
                v-for="{id, name} in author.periods"
                :key="id"
                class="badge badge-pill badge-secondary mr-1"
              >{{ name }}</span>
            </dd>
          </template>
        </dl>
      </div>

      <div class="col-12">
        <b-button-group class="level-btn-group d-flex">
          <b-button
            v-if="author.levels.discover"
            :active="level === 'discover'"
            :to="{ params: {level: 'discover'}}"
            variant="primary"
          >{{'Discover' | translate}}</b-button>
          <b-button
            v-if="author.levels.research"
            :active="level === 'research'"
            :to="{ params: {level: 'research'}}"
            variant="primary"
          >{{'Research' | translate}}</b-button>
          <b-button
            v-if="author.levels.material"
            :active="level === 'material'"
            :to="{ params: {level: 'material'}}"
            variant="primary"
          >{{'Material' | translate}}</b-button>
        </b-button-group>
      </div>

      <div class="col-12">
        <h3 class="mt-2">{{ 'Content' | translate }}</h3>
        <ol>
          <li>
            <a href="#memorials">{{ 'Memorials' | translate }}</a>
          </li>
          <li v-for="[heading] in detail" :key="heading">
            <a :href="'#' + heading">{{ heading | humanize | capitalize | translate }}</a>
          </li>
        </ol>
      </div>

      <div v-if="level !== 'material'" class="col-12 mb-4">
        <h4 id="memorials" class="mt-2">{{ 'Memorials' | translate }}</h4>

        <b-card v-for="(memorial, index) in memorials" :key="memorial.id" no-body>
          <b-card-header header-tag="header" class="p-0" role="tab">
            <b-button
              block
              href="#"
              v-b-toggle="'memorial-accordion-' + index"
              variant="primary-outline"
            >
              <cms-image
                v-if="memorial.title_image"
                :src="memorial.title_image.thumb"
                :alt="memorial.title_image.title"
                :title="memorial.title_image.title"
                class="memorial-img rounded-circle img-fluid mr-2"
              ></cms-image>
              {{ memorial.name }}
            </b-button>
          </b-card-header>
          <b-collapse
            :id="'memorial-accordion-' + index"
            @show="onMemorialShow(memorial.id)"
            accordion="memorial-accordion"
            role="tabpanel"
          >
            <b-card-body v-if="currentMemorial && memorial.id === currentMemorial.id">
              <router-link
                :to="{name: 'memorial-detail', params: { mapStatePath: toPath(currentMemorial.position), memorialId: currentMemorial.id }}"
              >
                <h4>{{ currentMemorial.name }}</h4>
                <small
                  class="text-muted d-block"
                >{{ 'See on map' | translate }}: {{ currentMemorial.position| humanizePosition }}</small>
              </router-link>

              <div v-if="level === 'discover' && currentMemorial.description.length">
                <paragraph
                  v-for="paragraph in currentMemorial.description"
                  :key="paragraph.id"
                  v-bind="paragraph.value"
                ></paragraph>
              </div>
              <div v-if="level === 'research' && currentMemorial.detailed_description.length">
                <paragraph
                  v-for="paragraph in currentMemorial.detailed_description"
                  :key="paragraph.id"
                  v-bind="paragraph.value"
                ></paragraph>
              </div>
            </b-card-body>
          </b-collapse>
        </b-card>
      </div>

      <author-article class="col-12" :content="detail"></author-article>
    </div>
  </div>
</template>

<script>
import store from '../state/store';
import { fetchAuthor, fetchMemorial } from '../state/actions';
import api from '../Api';
import translate from '../translate';
import {
  capitalize,
  humanize,
  humanizePosition,
  mapStateToPath,
  round
} from '../utils';
import AuthorArticle from './AuthorArticle.vue';
import FigureImage from './FigureImage.vue';
import MapComponent from './Map.vue';
import Paragraph from './Paragraph.vue';
import PrettyDate from './PrettyDate.vue';
import CmsImage from './CmsImage.vue';

export default {
  components: {
    CmsImage,
    AuthorArticle,
    FigureImage,
    MapComponent,
    PrettyDate,
    Paragraph
  },

  filters: {
    humanizePosition,
    humanize,
    translate,
    capitalize,
    round
  },

  metaInfo() {
    return {
      title: this.name
    };
  },

  computed: {
    level() {
      return this.$route.params.level;
    },

    author() {
      return store.state.author.current;
    },

    name() {
      const vm = this;
      return [vm.author.title, vm.author.first_name, vm.author.last_name].filter(x => x).join(' ');
    },

    detail() {
      const ignoredProperties = ['id'];
      return Object.entries(store.state.author.detail || []).filter(
        ([heading, paragraphs]) => {
          return ignoredProperties.indexOf(heading) === -1 && paragraphs.length;
        }
      );
    },

    memorials() {
      return store.state.author.memorials;
    },

    currentMemorial() {
      return store.state.memorial.current;
    }
  },

  beforeRouteEnter(to, from, next) {
    const slug = to.params.slug;
    const level = to.params.level;
    store.dispatch(fetchAuthor, { slug, level }).then(() => next());
  },

  beforeRouteUpdate(to, from, next) {
    const slug = to.params.slug;
    const level = to.params.level;
    store.dispatch(fetchAuthor, { slug, level }).then(() => next());
  },

  methods: {
    onMemorialShow(id) {
      store.dispatch(fetchMemorial, { id });
    },

    toPath(position) {
      const [lng, lat] = position;
      return mapStateToPath({ lng, lat });
    }
  }
};
</script>

<style lang="scss">
@import '../../scss/variables';

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

.memorial-img {
  max-height: 30px;
}
</style>
