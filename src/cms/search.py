from wagtail.search.backends.elasticsearch6 import (
    Elasticsearch6Index,
    Elasticsearch6Mapping,
    Elasticsearch6SearchBackend,
    Elasticsearch6SearchQueryCompiler,
    Elasticsearch6SearchResults,
)


class CustomElasticsearchMapping(Elasticsearch6Mapping):
    pass


class CustomElasticsearchIndex(Elasticsearch6Index):
    pass


class CustomElasticsearchSearchQueryCompiler(Elasticsearch6SearchQueryCompiler):
    mapping_class = CustomElasticsearchMapping

    def _process_lookup(self, field, lookup, value):
        column_name = self.mapping.get_field_column_name(field)

        if lookup == "bboverlaps":
            extent = value.extent
            shape = {
                "geo_shape": {
                    column_name: {
                        "shape": {
                            "type": "envelope",
                            "coordinates": [extent[:2], extent[:-2]],
                        },
                        "relation": "within",
                    }
                }
            }
            return shape

        return super()._process_lookup(field, lookup, value)


class CustomElasticsearchSearchResults(Elasticsearch6SearchResults):
    pass


class CustomElasticsearchSearchBackend(Elasticsearch6SearchBackend):
    mapping_class = CustomElasticsearchMapping
    index_class = CustomElasticsearchIndex
    query_compiler_class = CustomElasticsearchSearchQueryCompiler
    results_class = CustomElasticsearchSearchResults


SearchBackend = CustomElasticsearchSearchBackend
