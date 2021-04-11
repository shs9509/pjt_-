from django import forms
from .models import Book, Comment


class Book_Form(forms.ModelForm):

    class Meta:
        model = Book
        fields = '__all__'
    
class Comment_Form(forms.ModelForm):

    class Meta:
        model = Comment
        fields = '__all__'