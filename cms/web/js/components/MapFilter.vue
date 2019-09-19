<template>
    <form name="filter-form" class="p-2">
        <AuthorFilter
            id="author-filter"
            :api="api"
            v-on:change="onAuthorChange"
        ></AuthorFilter>
        <TagFilter
            :api="api"
            :id="'memorial-type'"
            :label="'Memorial type'"
            :param="'memorial_type'"
            :path="'/memorialTypes'"
            v-on:change="onFilterChange"></TagFilter>
    </form>
</template>

<script>
    import AuthorFilter from './AuthorFilter.vue';
    import TagFilter from './TagFilter.vue';


    export default {
        props: {
            api: Object
        },
        components: {
            AuthorFilter,
            TagFilter,
        },
        methods: {
            onAuthorChange: function (value) {
                const vm = this;
                vm.$emit('change', 'author', value);
            },
            onFilterChange: function (param, value) {
                const vm = this;
                vm.$emit('change', param, value);
            }
        }
    };
</script>
