from django import forms
from .models import Link

class NewLinkForm(forms.ModelForm):
    long_url = forms.URLField(required=True)
    
    class Meta:
        model = Link
        fields = (
            "long_url",
        )

    widgets = {
        "long_url": forms.URLInput(attrs={"required": "required"}),
    }
