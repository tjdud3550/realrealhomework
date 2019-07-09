from django import forms
from .models import Blog, Comment

# 카테고리 추가
class NewBlog(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'body']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text',)