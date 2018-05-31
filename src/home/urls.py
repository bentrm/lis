from django.urls import path
from .views import IndexView, ImpressumView

app_name = "home"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("impressum/", ImpressumView.as_view(), name="impressum"),
]
