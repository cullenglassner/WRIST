from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.admin.widgets import AdminDateWidget

class AddContactForm(forms.Form):
    
    uid = forms.CharField(label=_("UID"), max_length=16)
    address = forms.CharField(label=_("Address"), max_length=256)


    error_messages = {
        'invalid_uid': _("The UID %(uid) is not associated with an active user."),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(AddContactForm, self).__init__(*args, **kwargs)


    def clean(self):
        uid = self.cleaned_data.get('uid')
        address = self.cleaned_data.get('address')

        if uid:
            self.user_cache = get_user_model().objects.get(uid=uid)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_uid'],
                    code='invalid_uid',
                    params={'uid': uid},
                )
        return self.cleaned_data

class RemoveContactForm(forms.Form):
    
    uid = forms.CharField(label=_("UID"), max_length=16)

    error_messages = {
        'invalid_uid': _("The UID %(uid) is not associated with an active user."),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(RemoveContactForm, self).__init__(*args, **kwargs)


    def clean(self):
        uid = self.cleaned_data.get('uid')

        if uid:
            self.user_cache = get_user_model().objects.get(uid=uid)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_uid'],
                    code='invalid_uid',
                    params={'uid': uid},
                )
        return self.cleaned_data
