from django.urls import path
from .views import create_book, upload_file, BookListAPIView

urlpatterns = [
    path("create-book/", create_book, name="create-book"),
    path("upload-file/", upload_file, name="upload-file"),
    path("books/", BookListAPIView.as_view(), name="books")
]