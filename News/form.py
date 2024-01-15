from django import forms
from .models import News




class NewsUploadForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['author', 'title', 'description', 'video', "image", 'source', 'category', 'promotion']
         

    def __init__(self, *args, **kwargs):
        super(NewsUploadForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class":"input"})
         