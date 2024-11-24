from django import forms
from .models import Board, Category, Post
from ckeditor.widgets import CKEditorWidget


class BoardCreateForm(forms.ModelForm):
    title = forms.CharField(
        label='Title',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
    )
    text = forms.CharField(
        label='Text',
        widget=CKEditorWidget()
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Category',
    )
    image = forms.ImageField(
        label='Image',
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Board
        fields = ['title', 'text', 'category', 'image']

    def save(self, commit=True, user=None):
        board = super().save(commit=False)
        if user:
            board.author = user  # add author in board
        if commit:
            board.save()
        return board
  

class PostCreateForm(forms.ModelForm):
    title = forms.CharField(
        label='Title',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
    )
    text = forms.CharField(
        label='Text',
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    image = forms.ImageField(
        label='Image',
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Post
        fields = ['title', 'text', 'image']

    def save(self, commit=True, user=None):
        post = super().save(commit=False)
        if user:
            post.author = user  # add author in board
        if commit:
            post.save()
        return post