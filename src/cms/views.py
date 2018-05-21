from django.contrib.auth import login, authenticate
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import View

from .forms import SignUpForm


class SignupView(View):
    form_class = SignUpForm
    template_name = 'cms/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect("/cms")

        return render(request, self.template_name, {'form': form})
