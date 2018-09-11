from django.urls import include, path, re_path
from . import views

urlpatterns = [
    re_path(
        r"^(?P<version>(v1))/author/$",
        views.AuthorList.as_view(),
        name="api-author-list"
    ),
    re_path(
        r"^(?P<version>(v1))/author/(?P<pk>[0-9]+)/$",
        views.AuthorDetail.as_view(),
        name="api-author-detail"
    ),
    re_path(
        r"^(?P<version>(v1))/memorial/$",
        views.MemorialList.as_view(),
        name="api-memorial-list"
    ),
    re_path(
        r"^(?P<version>(v1))/memorial/(?P<pk>[0-9]+)/$",
        views.MemorialDetail.as_view(),
        name="api-memorial-detail"
    ),
    path("auth/", include('rest_framework.urls')),
]
