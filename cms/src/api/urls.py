from django.conf.urls import include, url
from rest_framework import routers
from api.views import AuthorViewSet, MemorialViewSet, LanguageViewSet, GenreViewSet, PeriodViewSet, MemorialTypeViewSet, \
    AuthorNameViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'names', AuthorNameViewSet, basename='names')
router.register(r'memorials', MemorialViewSet,  basename='memorial')
router.register(r'languages', LanguageViewSet, basename='language')
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'periods', PeriodViewSet, basename='period')
router.register(r'memorialTypes', MemorialTypeViewSet, basename='memorialType')

urlpatterns = [
    url(r'^', include(router.urls)),
]
