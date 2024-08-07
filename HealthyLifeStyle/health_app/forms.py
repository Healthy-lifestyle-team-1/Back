from django import forms

from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Article


class ArticleForm(forms.ModelForm):

      def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          self.fields["text"].required = False

      class Meta:
          model = Article
          fields = ("author", "text")
          widgets = {
              "text": CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}
              )
          }