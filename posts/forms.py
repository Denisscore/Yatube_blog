from django import forms
from .models import Post, Group, Comment
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms import ModelForm

class PostForm(forms.ModelForm):
    
    class Meta:   
        model = Post      
        fields = ("group", "text", "image")
        exclude = ("author", "pub_date")
        labels = {
            "group": "Группа",
            "text": "Текст",
            "image": "Изображение"
        }
        help_texts = {
            "group": "Выберите группу для Вашего поста, но это не обязательно :)",
            "text": "Введите текст поста",
        }
    
    def post_valid(self):
        data = self.cleaned_data["text"]
        if data == None:
            raise forms.ValidationError("Введите текст поста")
        return data


class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ("text",)
        exclude = ("post", "created")
        labels = {
            "author": "Автор",
            "text": "Текст",
        }
        help_texts = {
            "text": "Введите текст коментария",
        }
    