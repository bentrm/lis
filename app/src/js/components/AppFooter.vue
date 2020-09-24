<template>
    <div class="Footer container-fluid">
      <div class="container">
        <div class="row">
          <div class="col-12 col-sm-6 col-md-4 d-flex justify-content-center align-items-center">
            <router-link :to="{name: 'blog-page', params: { slug: 'tu-dresden' }}" class="stretched-link">
              <img :src="tudLogo" alt="TU Dresden" class="partner-logo img-fluid d-block m-4" />
            </router-link>
          </div>

          <div class="col-12 col-sm-6 col-md-4 d-flex justify-content-center align-items-center">
            <router-link
                :to="{name: 'blog-page', params: { slug: 'tu-liberec' }}"
                class="stretched-link"
            >
              <img :src="tulLogo" alt="TU Liberec" class="partner-logo img-fluid d-block m-4" />
            </router-link>
          </div>

          <div class="col-12 col-sm-6 col-md-4 d-flex justify-content-center align-items-center">
            <router-link :to="{name: 'blog-page', params: { slug: 'htw-dresden' }}" class="stretched-link">
              <img :src="htwLogo" alt="HTW Dresden" class="partner-logo img-fluid d-block m-4" />
            </router-link>
          </div>

          <div class="col-12 extras">
            <b-nav align="center">
              <b-nav-item :href="adminLink">{{ 'Admin' | translate }}</b-nav-item>
              <b-nav-item :to="{name: 'blog-page', params: { slug: 'partner'}}">{{ 'Project partner' | translate }}</b-nav-item>
              <b-nav-item :to="{name: 'blog-page', params: { slug: 'imprint' }}">{{ 'Imprint & data protection' | translate }}</b-nav-item>
              <b-nav-item :to="{name: 'blog-page', params: { slug: 'accessibility' }}">{{ 'Accessibility' | translate }}</b-nav-item>
            </b-nav>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
import htwLogo from '../../assets/logos/logo_htw_dresden.svg';
import tudLogo from '../../assets/logos/logo_tu_dresden.svg';
import tulLogo from '../../assets/logos/logo_tu_liberec.svg';
import translate from '../translate';
import {cmsHost} from '../config';

export default {
    filters: {
      translate
    },

    computed: {
      adminLink() {
        return `${cmsHost}/cms/admin`;
      }
    },

    data() {
      return {
        htwLogo,
        tudLogo,
        tulLogo
      };
    }
  };
</script>

<style lang="scss">
  @import '../../scss/variables';

  .Footer {
    //padding-top: 1rem;
    padding-bottom: 3rem;
    border-top: 0.8rem solid theme-color('primary');

    .partner-logo {
      max-height: 2.5rem;
    }

    .extras {
      border-top: 0.2rem solid theme-color('primary');
    }
  }
</style>
