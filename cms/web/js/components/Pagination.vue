<template>
  <nav>
    <ul class="pagination">
      <li
        v-for="n in totalPages"
        :class="{'page-item': true, 'active': n === currentPage}"
      >
        <button
          class="page-link"
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
    props: ['currentPage', 'totalPages'],
    methods: {
      emitChange: function (pageNumber) {
        this.$emit('change', pageNumber);
      }
    }
  };
</script>
