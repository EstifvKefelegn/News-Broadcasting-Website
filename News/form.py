# forms.py

from typing import Any
from django import forms
from .models import News, Promotion, NewsCategory  # Add the import statement
from django.contrib.auth.decorators import login_required

class NewsUploadForm(forms.ModelForm):

    class Meta:
        model = News
        fields =['author',
                 'title',
                 'description',
                 'video',
                 'image',
                 'small_image',
                 'second_image',
                 'small_title',
                 'source',
                 'category']

    def __init__(self, *args, **kwargs):
        # Accept 'request' as a keyword argument
        self.request = kwargs.pop('request', None)
        super(NewsUploadForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(NewsUploadForm, self).save(commit=False)
        if self.request:
            instance.author = self.request.user.username  # Set the author to the currently logged-in user
        if commit:
            instance.save()
        return instance
