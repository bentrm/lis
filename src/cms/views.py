"""Additional views for the CMS."""

from django.contrib.auth import login, authenticate
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import View

from .forms import SignupForm


class SignupView(View):
    """A simple view class that allows Editors to register for the CMS."""

    form_class = SignupForm
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
