from django import forms

from main.models import Form26


class Form26Form(forms.ModelForm):

    creation_date = forms.DateField()
    creation_date.widget.attrs.update({'id': 'datepicker'})

    class Meta:
        model = Form26
        fields = ('inspection', 'recommendation', 'creation_date')