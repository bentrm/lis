import Vue from 'vue/dist/vue.esm';

const template = `
    <div class="Author-card media">
      <div class="media-body mr-4">
        <p class="p-0 h4">
          <a :href="url" class="stretched-link">
            <span v-if="first_name" class="small text-muted">{{ first_name }}</span>
            {{ last_name }}
          </a>
        </p>
      </div>
      <img
        v-if="thumb"
        :src="thumb"
        class="Author-badge border border-primary rounded-circle align-self-center"
      >
      <span v-else class="placeholder"></span>
    </div>
  `;

Vue.component('author-card', {
  props: ['thumb', 'url', 'academic_title', 'first_name', 'last_name', 'birth_name'],
  template,
});
