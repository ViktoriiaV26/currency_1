from django import forms
from currency.models import Source


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = (
            'id',
            'name',
            'source_url',
        )
