from .models import Comment
from django import forms

class CommentForm(forms.ModelForm) :
    class Meta :
        model = Comment
        fields = ('content',)
        # fields 대신에 exclude도 가능
        # exclude = ('post', 'author', 'create_at', 'modified_at')