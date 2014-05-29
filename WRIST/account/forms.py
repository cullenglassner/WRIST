from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _

from django.contrib.auth import authenticate, get_user_model
from WRIST import settings


class UserCreationForm(forms.ModelForm):
    """
    Registration form
    """
    error_messages = {
        'duplicate_email': _("A user for that email already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    email = forms.EmailField(widget=forms.widgets.EmailInput, 
                             label=_("Email"), max_length=255)
    uid = forms.CharField(widget=forms.widgets.TextInput, 
                          label=_("UID"), max_length=16)
    password1 = forms.CharField(widget=forms.PasswordInput, 
                                label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label=_("Password confirmation"))

    class Meta:
        model = get_user_model()
        fields = ['email', 'uid', 'password1', 'password2']

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data["email"]
        try:
            get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    """
    Login form
    """
    email = forms.EmailField(widget=forms.widgets.TextInput)
    password = forms.CharField(widget=forms.widgets.PasswordInput)

    class Meta:
        fields = ['email', 'password']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        exclude = ['email','uid','password','bio','last_login','contacts','is_active','is_admin']
