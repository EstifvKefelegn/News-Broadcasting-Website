# from typing import Any
from typing import Any
from django import forms
from .models import News, Promotion




class NewsUploadForm(forms.ModelForm):
    promotion_title = forms.CharField(max_length=100, required=False, label='Promotion Title')
    # promotion_description = forms.CharField(max_length=250, widget=forms.Textarea, required=False, label='Promotion Description')
    promotion_picture = forms.ImageField(required=False, label='Promotion Picture')
    promotion_video = forms.FileField(required=False, label='Promotion Video')



    class Meta:
        model = News
        fields = ['author','title', 'description', 'video', "image","small_image",'second_image', 'small_title','source', 'category', "promotion"]

    def save(self, commit=True):
        news_instance = super().save(commit=False)
        promotion_instance = Promotion(
            title = self.cleaned_data['promotion_title'],
            promo_picture =self.cleaned_data['promotion_picture'],
            promo_videos = self.cleaned_data['promotion_video']            

        ) 
        if commit:
            promotion_instance.save()
            news_instance.promotion = promotion_instance
            news_instance.save()
        return news_instance

    def clean(self):
        cleaned_data = super().clean()
        promotion_choice = cleaned_data.get('promotion_choice')

        # If the user selected a promotion, use it; otherwise, create a new one
        if promotion_choice:
            cleaned_data['promotion'] = promotion_choice
        else:
            # If no promotion selected, set promotion field to None
            cleaned_data['promotion'] = None

        return cleaned_data         

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
    

