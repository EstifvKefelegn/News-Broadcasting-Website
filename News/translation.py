from modeltranslation.translator import register, TranslationOptions

from .models import NewsCategory

@register(NewsCategory)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)  # Add a comma to make it a tuple
