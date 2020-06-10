from __future__ import unicode_literals
from django import forms
from .models import User, Region

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('name', 'age', 'region', 'location', 'holiday_tp_nm', 'min_sal')

    def __init__(self, *args, **kwargs):

        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['region'].queryset = Region.objects.all().values("region")

        