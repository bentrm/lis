"""Additional views for the CMS."""

from dal import autocomplete
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from . import models, tags, forms

class SignupView(View):
    """A simple view class that allows Editors to register for the CMS."""

    form_class = forms.SignupForm
    template_name = "cms/signup.html"

    def get(self, request, *args, **kwargs):
        """Return the form view."""
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        """Validate and save the form authenticating the new user."""
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect("/cms")

        return render(request, self.template_name, {'form': form})


class LanguageAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return tags.LanguageTag.objects.none()

        qs = tags.LanguageTag.objects.order_by("title")
        if self.q:
            filter = (
                Q(title__contains=self.q)
                | Q(title_de__contains=self.q)
                | Q(title_cs__contains=self.q)
            )
            qs = qs.filter(filter)

        return qs


class LocationTypeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return tags.LocationTypeTag.objects.none()

        qs = tags.LocationTypeTag.objects.order_by("title")
        if self.q:
            filter = (
                Q(title__contains=self.q)
                | Q(title_de__contains=self.q)
                | Q(title_cs__contains=self.q)
            )
            qs = qs.filter(filter)

        return qs


class GenreAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return tags.GenreTag.objects.none()

        qs = tags.GenreTag.objects.order_by("title")
        if self.q:
            filter = (
                Q(title__contains=self.q)
                | Q(title_de__contains=self.q)
                | Q(title_cs__contains=self.q)
            )
            qs = qs.filter(filter)

        return qs


class ContactTypeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return tags.ContactTypeTag.objects.none()

        print(self.q)

        qs = tags.ContactTypeTag.objects.order_by("title")
        if self.q:
            filter = (
                Q(title__contains=self.q)
                | Q(title_de__contains=self.q)
                | Q(title_cs__contains=self.q)
            )
            qs = qs.filter(filter)

        return qs


class LiteraryPeriodAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return tags.LiteraryPeriodTag.objects.none()

        qs = tags.LiteraryPeriodTag.objects.order_by("sort_order")
        if self.q:
            filter = (
                Q(title__contains=self.q)
                | Q(title_de__contains=self.q)
                | Q(title_cs__contains=self.q)
            )
            qs = qs.filter(filter)

        return qs
