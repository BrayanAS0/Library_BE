from django.http import JsonResponse
from .models import Book,BookDetail,Review
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
def book_with_detail(request):
    id = request.GET.get("id")
    book = Book.objects.get(pk=id)
    recommendations = list(
        book.recommendation.all().values("user__username", "recommended_at", "note")
    )
    for r in recommendations:
        r["user"] = r.pop("user__username")

    reviews = list(
        book.reviews.all().values("user__username", "rating", "text", "created_at")
    )
    for r in reviews:
        r["user"] = r.pop("user__username")

    response = {
        "id": book.id,
        "author":book.author.name,
        "pages": book.pages,
        "title": book.title,
        "publication_date": book.publication_date,
        "recommendations": recommendations,
        "reviews": reviews
    }
    return JsonResponse(response)
@csrf_exempt
def loan_books(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_id = data.get("user_id")
            book_id = data.get("book_id")
            
            print(user_id, book_id)
            return JsonResponse({"user_id": user_id, "book_id": book_id})
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    else:
        return JsonResponse({"error": "Only POST method allowed"}, status=405)