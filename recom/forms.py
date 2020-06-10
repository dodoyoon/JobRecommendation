from __future__ import unicode_literals
from django import forms
from .models import User, Region, UserCareer

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('name', 'age', 'region', 'location', 'holiday_tp_nm', 'min_sal')

    def __init__(self, *args, **kwargs):

        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['region'].queryset = Region.objects.all().values("region")

class UserCareerForm(forms.ModelForm):
    class Meta:
        model = UserCareer
        fields = ('career', )

        