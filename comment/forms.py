from django import forms
from .models import Comment



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
        widgets = {
            'content_type': forms.HiddenInput(attrs={'class':'form-control'}),
            'object_id': forms.HiddenInput(attrs={'class':'form-control'}),
            'parent': forms.HiddenInput(attrs={'class':'form-control'}),
            'content': forms.Textarea(attrs={'class':'form-control'}),
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.TextInput(attrs={'class':'form-control'}),
        }
