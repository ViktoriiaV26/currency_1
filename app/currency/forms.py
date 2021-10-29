from django import forms
from currency.models import Source
from currency.models import Rate


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = (
            'id',
            'name',
            'source_url',
        )


class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = (
            'buy',
            'sale',
            'source',
            'type',
        )