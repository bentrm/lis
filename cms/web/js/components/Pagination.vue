<template>
  <nav>
    <ul class="pagination">
      <li
        v-for="n in totalPages"
        class="page-item"
      >
        <button
          :class="{'page-link': true, 'active': n === currentPage}"
          :data-page="n"
          v-on:click="emitChange(n)"
        >
          {{ n }}
        </button>
      </li>
    </ul>
  </nav>
</template>

<script>
  export default {
    props: ['param', 'currentPage', 'totalPages'],
    methods: {
      emitChange: function (pageNumber) {
        this.$emit('change', pageNumber);
      }
    }
  };
</script>
