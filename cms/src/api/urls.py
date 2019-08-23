from django.conf.urls import include, url
from rest_framework import routers
from wagtail.api.v2.endpoints import PagesAPIEndpoint
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.documents.api.v2.endpoints import DocumentsAPIEndpoint
from wagtail.images.api.v2.endpoints import ImagesAPIEndpoint

from api.views import LanguageViewSet, GenreViewSet, PeriodViewSet, MemorialTypeViewSet, MemorialApiEndpoint, \
    AuthorApiEndpoint, AuthorViewSet, MemorialViewSet

# Create the router. "wagtailapi" is the URL namespace
api_router = WagtailAPIRouter("wagtailapi")

# Add the three endpoints using the "register_endpoint" method.
# The first parameter is the name of the endpoint (eg. pages, images). This
# is used in the URL of the endpoint
# The second parameter is the endpoint class that handles the requests
api_router.register_endpoint("pages", PagesAPIEndpoint)
api_router.register_endpoint("authors", AuthorApiEndpoint)
api_router.register_endpoint("memorials", MemorialApiEndpoint)
api_router.register_endpoint("images", ImagesAPIEndpoint)
api_router.register_endpoint("documents", DocumentsAPIEndpoint)

router = routers.DefaultRouter(trailing_slash=False)
router.register('memorials', MemorialViewSet, basename="memorial")
router.register('authors', AuthorViewSet, basename='author')
router.register('languages', LanguageViewSet, basename='language')
router.register('genres', GenreViewSet, basename='genre')
router.register('periods', PeriodViewSet, basename='period')
router.register('memorialTypes', MemorialTypeViewSet, basename='memorialType')

urlpatterns = [
    url(r'^v2/pages/', api_router.urls),
    url(r'^v2/', include(router.urls)),
]
