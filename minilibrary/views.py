from django.http import JsonResponse
from .models import Book
import json
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
def get_books(request):
    author_id = request.GET.get("author")
    books = Book.objects.all()

    if author_id:
        books = books.filter(author__pk=author_id)

    books_data = list(books.values()) 

    return JsonResponse(books_data, safe=False)
@csrf_exempt
def login(request):
    if request.method == "POST":
            try:
                data = json.loads(request.body)
                username = data.get("username")
                password = data.get("password")
            except (json.JSONDecodeError, TypeError):
                return JsonResponse({"error": "Invalid JSON"}, status=400)
            
            if not username or not password:
                return JsonResponse({"error": "Missing username or password"}, status=400)

            user = authenticate(username=username, password=password)
            if user is not None:
                return JsonResponse({"access": "granted"})
            else:
                return JsonResponse({"access": "denied"}, status=401)
    else:
            return JsonResponse({"error": "POST required"}, status=405)
@csrf_exempt
def signup(request):
    if request.method == "POST":
            try:
                data = json.loads(request.body)
                username = data.get("username")
                password = data.get("password")
            except (json.JSONDecodeError, TypeError):
                return JsonResponse({"error": "Invalid JSON"}, status=400)
            
            if not username or not password:
                return JsonResponse({"error": "Missing username or password"}, status=400)

            user = authenticate(username=username, password=password)
            if user is not None:
                return JsonResponse({"access": "granted"})
            else:
                return JsonResponse({"access": "denied"}, status=401)
    else:
            return JsonResponse({"error": "POST required"}, status=405)

def Books(request):
    books = Book.objects.all()
    return JsonResponse(books.values())
def Book_index(request):
    books = Book.objects.prefetch_related("loans").all()
    
    result = []
    for b in books:
        data = {
            "id": b.id,
            "title": b.title,
            "publication_date": b.publication_date,
            "pages":b.pages,
            "has_active_loan": b.loans.filter(is_returned=False).exists(),
        }
        result.append(data)
    return JsonResponse(result, safe=False)