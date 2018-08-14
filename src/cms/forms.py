
from django.utils.translation import gettext_lazy as _
from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group


class SignupForm(UserCreationForm):
    """A signup form that checks for a keyword before allowing users to register as an editor."""

    keyword = forms.CharField(max_length=30, label=_("Keyword"), help_text=_("Keyword"))
    first_name = forms.CharField(max_length=30, label=_("First name"))
    last_name = forms.CharField(max_length=30, label=_("Last name"))
    email = forms.EmailField(max_length=254, label=_("Email"))

    def clean_keyword(self):
        """Check keyword."""
        keyword = self.cleaned_data["keyword"]

        if keyword != settings.LIS_SIGNUP_KEYWORD:
            raise forms.ValidationError(_("Invalid keyword."))
        return keyword

    def save(self, commit=True):
        """Create new user adding her to the editors group."""
        new_user = super(SignupForm, self).save(commit=True)
        editors_group = Group.objects.get(name="Editors")
        editors_group.user_set.add(new_user)

    class Meta:
        model = User
        fields = ("keyword", "username", "first_name", "last_name", "email", "password1", "password2")
