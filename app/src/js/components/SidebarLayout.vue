<template>
  <div :class="fluid ? 'container-fluid' : 'container'">
    <div class="row">

      <main class="col" v-if="!isSmallDevice">
        <slot></slot>
      </main>

      <div class="Sidebar col col-sm-6 col-lg-4 p-0">
        <b-card class="h-100" no-body>
          <b-tabs card pills small fill>
            <slot name="sidebar"></slot>
          </b-tabs>
        </b-card>
      </div>

    </div>
  </div>
</template>

<script>
  import {getDeviceWidth} from '../utils';

  export default {
    props: {
      fluid: {
        type: Boolean,
        default: true,
      }
    },
    data() {
      return {
        isSmallDevice: getDeviceWidth() < 576,
      };
    }
  }
</script>
