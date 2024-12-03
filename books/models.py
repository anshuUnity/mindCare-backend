from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class Book(models.Model):
    # Basic Details
    title = models.CharField(max_length=255, help_text="Title of the book")
    author = models.CharField(max_length=255, help_text="Author of the book")
    description = models.TextField(blank=True, null=True, help_text="A brief summary or description of the book")
    published_date = models.DateField(blank=True, null=True, help_text="Publication date of the book")
    
    # Metadata
    isbn = models.CharField(
        max_length=13,
        unique=True,
        blank=True,
        null=True,
        help_text="International Standard Book Number (ISBN)",
    )
    language = models.CharField(max_length=100, default="English", help_text="Language of the book")
    pages = models.PositiveIntegerField(
        blank=True, 
        null=True, 
        validators=[MinValueValidator(1, message="Number of pages must be at least 1")],
        help_text="Total number of pages in the book"
    )

    # File Storage
    cover_image = models.URLField(blank=True, null=True, help_text="URL of the book's cover image")
    file = models.URLField(blank=True, null=True, help_text="URL of the book file (PDF, ePub, etc.)")

    # Single Tag
    tag = models.CharField(
        max_length=100,
        help_text="Tag to categorize the book (e.g., fiction, self-help, etc.)"
    )

    # Status and Timestamps
    is_available = models.BooleanField(default=True, help_text="Indicates if the book is available for reading")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the book record was created")
    updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp when the book record was last updated")

    class Meta:
        ordering = ['title']
        verbose_name = "Book"
        verbose_name_plural = "Books"

    def __str__(self):
        return self.title

    def clean(self):
        """
        Custom validation for ISBN length.
        """
        if self.isbn:
            isbn_str = str(self.isbn)  # Convert ISBN to a string
            print(len(isbn_str))
            if not (10 <= len(isbn_str) <= 13):
                raise ValidationError("ISBN must be between 10 and 13 characters long.")

