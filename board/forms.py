from django import forms
from .models import Board, Category
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