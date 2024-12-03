from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    cover_image = forms.URLField(widget=forms.HiddenInput(), required=False)
    file = forms.URLField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'description',
            'published_date',
            'isbn',
            'language',
            'pages',
            'tag',
            'cover_image',
            'file',
            'is_available',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = None  # Remove help text
