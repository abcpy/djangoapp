from django import forms
from zanhu.articles.models import Article
from markdownx.fields import MarkdownxFormField


class ArticleForm(forms.ModelForm):
    content = MarkdownxFormField()


    class Meta:
        model = Article
        fields = ["title","image","content","tags","edited"]

