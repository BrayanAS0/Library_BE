from django.http import JsonResponse
from .models import Book

from django.contrib.auth import authenticate

def get_books(request):
    author_id = request.GET.get("author")
    books = Book.objects.all()

    if author_id:
        books = books.filter(author__pk=author_id)

    books_data = list(books.values())  # <-- con list()

    return JsonResponse(books_data, safe=False)
def verify_user(request):
    username = request.GET.get("user")
    password = request.GET.get("password")

    user = authenticate(username=username, password=password)
    if user is not None:
        return JsonResponse({"access": "granted"})
    else:
        return JsonResponse({"access": "denied"}, status=401)