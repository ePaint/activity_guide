from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList

from .models import Ad

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['image_url']
        widgets = {
            'image_url': forms.URLInput(attrs={'placeholder': ''})
        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['image_url'].required = False