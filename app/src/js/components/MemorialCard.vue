<template>
  <div class="card memorial-card">
    <span class="close" v-on:click="$emit('hide')">
      <i class="fas fa-times"></i>
    </span>

    <figure-image
      class="card-img-top m-0"
      v-if="image"
      :src="image.banner"
      :src-modal="image.large"
      :alt="image.title"
      :title="image.title"
      :captionModal="image.caption"
      :copyright="image.copyright"
    ></figure-image>

    <div class="card-body">
      <h5>
        {{ title }}
        <small class="d-block">
          <router-link
            :to="{name: 'memorial-detail', params: { mapStatePath: path }}"
          >{{ position | humanizePosition }}</router-link>
        </small>
      </h5>

      <div>
        <ul class="list-unstyled">
          <li v-for="author in authors" :key="author.id">
            <div class="author-card media">
              <cms-image
                  v-if="author.title_image"
                  :src="author.title_image.thumb"
                  :alt="author.title_image.title"
                  :title="author.title_image.title"
                  class="author-img border border-primary rounded-circle img-fluid mr-2 align-self-center"
                ></cms-image>

              <div class="media-body">
                <router-link :to="{name: 'author-detail', params: { slug: author.slug }}">
                  <span v-if="author.first_name">{{ author.first_name }}</span>
                  {{ author.last_name }}
                </router-link>

                <small class="text-muted d-block">
                  <pretty-date
                    v-if="author.yob"
                    :year="author.yob"
                    :month="author.mob"
                    :day="author.dob"
                    :place="author.pob"
                  ></pretty-date>

                  <span v-if="author.yob && author.yod">-</span>

                  <pretty-date
                    v-if="author.yod"
                    :year="author.yod"
                    :month="author.mod"
                    :day="author.dod"
                    :place="author.pod"
                  ></pretty-date>
                </small>
              </div>
            </div>
          </li>
        </ul>
      </div>

      <div v-if="introduction">
        <div v-html="introduction"></div>
      </div>
      <div v-if="address">
        <b>{{ 'Address' | translate }}</b>
        <address v-html="address"></address>
      </div>
      <div v-if="contactInfo">
        <b>{{ 'Contact info' | translate }}</b>
        <div v-html="contactInfo"></div>
      </div>
      <div v-if="directions">
        <b>{{ 'Directions' | translate }}</b>
        <i v-if="directions" v-html="directions"></i>
      </div>
    </div>
  </div>
</template>

<script>
import translate from '../translate';
import { humanizePosition, mapStateToPath } from '../utils';
import Paragraph from './Paragraph.vue';
import PrettyDate from './PrettyDate.vue';
import FigureImage from './FigureImage.vue';
import CmsImage from './CmsImage.vue';

export default {
  props: {
    title: String,
    image: Object,
    position: Array,
    authors: Array,
    address: String,
    contactInfo: String,
    directions: String,
    introduction: String,
    description: Array,
    detailedDescription: Array
  },
  components: {
    CmsImage,
    FigureImage,
    Paragraph,
    PrettyDate
  },
  filters: {
    humanizePosition,
    translate
  },

  data() {
    return {
      showImage: false
    };
  },

  computed: {
    path() {
      return mapStateToPath(this.position);
    }
  }
};
</script>

<style lang="scss">
@import '../../scss/variables';

.memorial-card {
  .close {
    color: white;
    position: absolute;
    top: 10px;
    right: 10px;
    filter: drop-shadow(0 0 2px black);
  }

  .blockquote {
    font-size: 0.8rem;
  }

  .footnotes {
    font-size: $font-size-sm;

    ol {
      padding-left: 1.5rem;
    }
  }

  .author-card {
    .author-img {
      max-height: 30px;
    }
  }
}
</style>
