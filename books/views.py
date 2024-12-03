from django.http import JsonResponse
from .forms import BookForm
from azure.storage.blob import generate_blob_sas, BlobSasPermissions, BlobServiceClient
from datetime import datetime, timedelta
from django.conf import settings
import logging
from django.shortcuts import render


def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)

            # Retrieve the uploaded file URLs from the form data
            cover_image_url = form.cleaned_data.get('cover_image')
            file_url = form.cleaned_data.get('file')

            # Assign the URLs to the book instance
            book.cover_image = cover_image_url
            book.file = file_url

            # Save the book instance
            book.save()

            # Return a success response
            return JsonResponse({"message": "Book created successfully!"}, status=201)
        else:
            # If form is invalid, return the errors
            return JsonResponse({"errors": form.errors}, status=400)
    else:
        form = BookForm()
        return render(request, 'create_book.html', {'form': form})


def upload_file(request):
    if request.method == 'POST':
        try:
            blob_service_client = BlobServiceClient.from_connection_string(settings.AZURE_CONNECTION_STRING)
            file_type = request.POST.get('file_type')
            blob_name = request.POST.get('blob_name')

            if file_type == 'image':
                container_name = "mindcare-thumbnail"
            elif file_type == 'file':
                container_name = "mindcare-pdf"
            else:
                return JsonResponse({"error": "Invalid file type."}, status=400)

            # Generate SAS token
            sas_token = generate_blob_sas(
                account_name=blob_service_client.account_name,
                container_name=container_name,
                blob_name=blob_name,
                account_key=settings.AZURE_ACCOUNT_KEY,
                permission=BlobSasPermissions(write=True),
                expiry=datetime.utcnow() + timedelta(hours=1)  # Token valid for 1 hour
            )

            url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"

            return JsonResponse({"url": url}, status=200)
        except Exception as e:
            logging.exception("Failed to generate SAS token")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)
