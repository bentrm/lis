<template>
  <div class="row">

    <div class="col-12 col-sm-4 col-md-3" v-if="author.title_image">
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

    <div class="col-12 col-sm-8 col-md-9">
      <h3 class="mt-0">
        <author-name :show-details="true" :isPseudonym="name.is_pseudonym" :title="name.title"
                     :firstName="name.first_name" :lastName="name.last_name"
                     :birthName="name.birth_name"/>
      </h3>

      <dl>
        <template v-if="author.also_known_as.length > 1">
          <dt>{{ 'Also known as' | translate }}</dt>
          <dd
            v-for="({is_pseudonym, title, first_name, last_name, birth_name}, index) in author.also_known_as.slice(1)"
            :key="index">
            <author-name :show-details="true" :isPseudonym="is_pseudonym" :title="title"
                         :firstName="first_name" :lastName="last_name" :birthName="birth_name"/>
          </dd>
        </template>

        <template v-if="author.yob">
          <dt>{{ 'Born' | translate }}</dt>
          <dd>{{ dateOfBirth }}</dd>
        </template>

        <template v-if="author.yod">
          <dt>{{ 'Died' | translate }}</dt>
          <dd>{{ dateOfDeath }}</dd>
        </template>
      </dl>

      <author-labels title="Languages" :labels="author.languages"/>
      <author-labels title="Genres" :labels="author.genres"/>
      <author-labels title="Periods" :labels="author.periods"/>
    </div>
  </div>
</template>

<script>
  import AuthorLabels from './AuthorLabels.vue';
  import PrettyDate from './PrettyDate.vue';
  import FigureImage from './FigureImage.vue';
  import AuthorName from './AuthorName.vue';
  import translate from '../translate';
  import {humanizeDate} from '../utils';

  export default {
    props: {
      author: Object,
    },

    components: {
      AuthorLabels,
      AuthorName,
      FigureImage,
      PrettyDate,
    },

    filters: {
      translate,
    },

    computed: {
      name() {
        const vm = this;
        return vm.author.also_known_as[0];
      },

      dateOfBirth() {
        const vm = this;
        const {author} = vm;
        return humanizeDate(author.dob, author.mob, author.yob, author.pob);
      },

      dateOfDeath() {
        const vm = this;
        const {author} = vm;
        return humanizeDate(author.dod, author.mod, author.yod, author.pod);
      },
    },
  };
</script>
