"""Additional views for the CMS."""

from dal import autocomplete
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from . import forms
from .models import GenreTag, LanguageTag, MemorialTag, PeriodTag, AgeGroupTag
from cms.models import Author


class SignupView(View):
    """A simple view class that allows Editors to register for the CMS."""

    form_class = forms.SignupForm
    template_name = "cms/signup.html"

    def get(self, request, *args, **kwargs):
        """Return the form view."""
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        """Validate and save the form authenticating the new user."""
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect("/cms")

        return render(request, self.template_name, {"form": form})


class GenericAutocompleteView(autocomplete.Select2QuerySetView):
    """Generic autocomplete view to search title fields."""

    def get_result_label(self, item):
        return item.i18n_title

    def get_selected_result_label(self, item):
        return item.i18n_title

    def get_queryset(self):
        """Return queryset filtered by user authentication status and search term."""
        if not self.request.user.is_authenticated:
            return self.model.objects.none()

        qs = self.model.objects.order_by("title")
        if self.q:
            q_en = Q(title__contains=self.q)
            q_de = Q(title_de__contains=self.q)
            q_cs = Q(title_cs__contains=self.q)
            qs = qs.filter(q_en | q_de | q_cs)
        return qs


class AuthorAutocompleteView(GenericAutocompleteView):
    """Author autocomplete view."""

    model = Author


class LanguageAutocomplete(GenericAutocompleteView):
    """Language tag autocomplete view."""

    model = LanguageTag


class LocationTypeAutocomplete(GenericAutocompleteView):
    """Location type tag autocomplete view."""

    model = MemorialTag


class GenreAutocomplete(GenericAutocompleteView):
    """Genre tag autocomplete view."""

    model = GenreTag


class LiteraryPeriodAutocomplete(GenericAutocompleteView):
    """Literary period tag autocomplete view."""

    model = PeriodTag


class AgeGroupAutocomplete(GenericAutocompleteView):
    """Age group tag autocomplete view."""

    model = AgeGroupTag
