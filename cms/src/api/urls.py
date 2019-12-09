from django.conf.urls import include, url
from rest_framework import routers

from api.views import LanguageViewSet, GenreViewSet, PeriodViewSet, MemorialTypeViewSet, \
    MemorialViewSet, AuthorViewSet, \
    MemorialPathViewSet, BlogPageViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('page', BlogPageViewSet, basename='page')
router.register('memorials', MemorialViewSet, basename='memorial')
router.register('paths', MemorialPathViewSet, basename='path')
router.register('authors', AuthorViewSet, basename='author')
router.register('languages', LanguageViewSet, basename='language')
router.register('genres', GenreViewSet, basename='genre')
router.register('periods', PeriodViewSet, basename='period')
router.register('memorialTypes', MemorialTypeViewSet, basename='memorialType')

urlpatterns = [
    url(r'^v2/', include(router.urls)),
]
