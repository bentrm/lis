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
        <h3 class="mt-0">{{ author.title }} {{ author.first_name }} {{ author.last_name }}</h3>

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

      <div v-if="author.levels" class="col-12">
        <div class="level-btn-group btn-group d-flex" role="group">
          <button
            v-for="(url, name) in author.levels"
            :key="name"
            v-on:click="onClick(name)"
            type="button"
            :class="['btn', 'btn-primary', {'active': currentLevel === name}]"
          >{{ name | capitalize | translate }}</button>
        </div>
      </div>

      <div class="col-12">
        <h3>{{ 'Content' | translate }}</h3>
        <ol>
          <li v-if="currentLevel !== 'material'">
            <a href="#memorials">{{ 'Memorials' | translate }}</a>
          </li>
          <li v-for="[heading] in levelContent" :key="heading">
            <a :href="'#' + heading">{{ heading | humanize | capitalize | translate }}</a>
          </li>
        </ol>
      </div>

      <div v-if="currentLevel !== 'material'" class="col-12">
        <h4 id="memorials">{{ 'Memorials' | translate }}</h4>

        <div class="list-group my-4">
          <button
            type="button"
            class="list-group-item list-group-item-action"
            v-for="memorial in memorials"
            v-on:click="onMemorialSelect(memorial.id)"
            :key="memorial.id"
            :class="{'active': currentMemorial && (memorial.id === currentMemorial.id)}"
          >
            <cms-image
              v-if="memorial.title_image"
              :src="memorial.title_image.thumb"
              :alt="memorial.title_image.title"
              :title="memorial.title_image.title"
              class="memorial-img rounded-circle img-fluid mr-2"
            ></cms-image>
            {{ memorial.name }}
          </button>
        </div>
      </div>

      <div v-if="currentMemorial" class="col-12">
        <router-link
          :to="{name: 'memorial-detail', params: { mapStatePath: toPath(currentMemorial.position), memorialId: currentMemorial.id }}"
        >
          <h4>{{ currentMemorial.name }}</h4>
          <small
            class="text-muted d-block"
          >{{ 'See on map' | translate }}: {{ currentMemorial.position| humanizePosition }}</small>
        </router-link>

        <div v-if="currentLevel === 'discover' && currentMemorial.description.length">
          <paragraph
            v-for="paragraph in currentMemorial.description"
            :key="paragraph.id"
            v-bind="paragraph.value"
          ></paragraph>
        </div>
        <div v-if="currentLevel === 'research' && currentMemorial.detailed_description.length">
          <paragraph
            v-for="paragraph in currentMemorial.detailed_description"
            :key="paragraph.id"
            v-bind="paragraph.value"
          ></paragraph>
        </div>
      </div>

      <author-article class="col-12" :content="levelContent"></author-article>
    </div>
  </div>
</template>

<script>
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
  props: {
    slug: String,
    currentLevel: String
  },

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

  data() {
    return {
      author: null,
      memorials: [],
      currentMemorial: null,
      level: null
    };
  },

  computed: {
    levelContent() {
      const ignoredProperties = ['id'];
      return Object.entries(this.level || []).filter(
        ([heading, paragraphs]) => {
          console.log(paragraphs);
          return ignoredProperties.indexOf(heading) === -1 && paragraphs.length;
        }
      );
    }
  },

  created() {
    this.fetchAuthor(this.slug);
    this.fetchLevel(this.slug, this.currentLevel);
  },

  watch: {
    author() {
      this.fetchMemorials();
    },
    slug() {
      this.fetchAuthor(this.slug);
    },
    currentLevel() {
      this.fetchLevel(this.slug, this.currentLevel);
    }
  },

  methods: {
    fetchAuthor(slug) {
      api.getAuthor(slug).then(json => (this.author = json));
    },
    fetchMemorials() {
      api
        .getMemorials({
          author: this.author.id,
          limit: 25
        })
        .then(json => (this.memorials = json.results));
    },
    fetchLevel(slug, level) {
      api.getLevel(slug, level).then(json => (this.level = json));
    },
    onClick(level) {
      const vm = this;
      vm.$router.push({
        name: 'author-detail',
        params: { ...vm.$route.params, level }
      });
    },

    onMemorialSelect(id) {
      api.getMemorial(id).then(json => (this.currentMemorial = json));
    },

    toPath(position) {
      return mapStateToPath(position);
    }
  }
};
</script>

<style lang="scss">
@import '../../scss/variables';

.level-btn-group {
  margin-bottom: 20px;

  button.active::after {
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
