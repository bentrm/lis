<template>
  <div class="card memorial-card">
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
          <router-link :to="{name: 'memorial-detail', params: { mapStatePath: path }}">
            {{ position | humanizePosition }}
          </router-link>
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
                <router-link
                  :to="{name: 'author-memorial-detail', hash: '#current-memorial', params: { slug: author.slug, level: 'discover', memorialId: id }}">
                  <author-name :show-details="false" :title="author.also_known_as[0].title"
                               :firstName="author.also_known_as[0].first_name"
                               :lastName="author.also_known_as[0].last_name"
                               :birthName="author.also_known_as[0].birth_name"/>

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
  import {humanizePosition, mapStateToPath} from '../utils';
  import Paragraph from './Paragraph.vue';
  import PrettyDate from './PrettyDate.vue';
  import FigureImage from './FigureImage.vue';
  import CmsImage from './CmsImage.vue';
  import AuthorName from './AuthorName.vue';

  export default {
    props: {
      id: [Number, String],
      title: String,
      image: Object,
      position: Array,
      authors: Array,
      address: String,
      contactInfo: String,
      directions: String,
      introduction: String,
      description: Array,
      detailedDescription: Array,
    },
    components: {
      AuthorName,
      CmsImage,
      FigureImage,
      Paragraph,
      PrettyDate,
    },
    filters: {
      humanizePosition,
      translate,
    },

    data() {
      return {
        showImage: false,
      };
    },

    computed: {
      path() {
        const [lng, lat] = this.position;
        return mapStateToPath({lng, lat});
      },
    },
  };
</script>

<style lang="scss">
  @import '../../scss/variables';

  .memorial-card {
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
