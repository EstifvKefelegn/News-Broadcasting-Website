# from typing import Any
from django import forms
from .models import News




class NewsUploadForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['author','title', 'description', 'video', "image", 'source', 'category', 'promotion']
         

    # def __init__(self, *args, **kwargs):
    #     super(NewsUploadForm, self).__init__(*args, **kwargs)

    #     for name, field in self.fields.items():
    #         field.widget.attrs.update({"class":"input"})

    # def save(self, commit=True) -> Any:
    #     newsinstance = super(NewsUploadForm, self).save(commit=False)
    #     newsinstance.author = self.request.user

        # if commit:
        #     newsinstance.save()
        # return newsinstance         
    

