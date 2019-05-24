"""API url patterns."""

from django.urls import include, path, re_path
from . import views

urlpatterns = [
    re_path(
        r"^(?P<version>(v1))/tag/genre/$",
        views.GenreList.as_view(),
        name="api-genre-list",
    ),
    re_path(
        r"^(?P<version>(v1))/tag/language/$",
        views.LanguageList.as_view(),
        name="api-language-list",
    ),
    re_path(
        r"^(?P<version>(v1))/tag/memorial/$",
        views.MemorialTypeList.as_view(),
        name="api-memorial-type-list",
    ),
    re_path(
        r"^(?P<version>(v1))/tag/period/$",
        views.PeriodList.as_view(),
        name="api-period-list",
    ),
    re_path(
        r"^(?P<version>(v1))/$",
        views.SearchView.as_view(),
        name="api-search-list",
    ),
    re_path(
        r"^(?P<version>(v1))/author/$",
        views.AuthorList.as_view(),
        name="api-author-list",
    ),
    re_path(
        r"^(?P<version>(v1))/author/(?P<pk>[0-9]+)/$",
        views.AuthorDetail.as_view(),
        name="api-author-detail",
    ),
    re_path(
        r"^(?P<version>(v1))/memorial/$",
        views.MemorialList.as_view(),
        name="api-memorial-list",
    ),
    re_path(
        r"^(?P<version>(v1))/memorial/(?P<pk>[0-9]+)/$",
        views.MemorialDetail.as_view(),
        name="api-memorial-detail",
    ),
    path("auth/", include("rest_framework.urls")),
]
