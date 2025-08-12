from django.http import JsonResponse
from .models import Book,BookDetail,Review,Loan
import json
from django.contrib.auth import authenticate,get_user_model,get_user
from django.views.decorators.csrf import csrf_exempt
def get_books(request):
    author_id = request.GET.get("author")
    books = Book.objects.all()

    if author_id:
        books = books.filter(author__pk=author_id)

    books_data = list(books.values()) 

    return JsonResponse(books_data, safe=False)
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
def loan_books(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method allowed"}, status=405)

    try:
        data = json.loads(request.body)
        user_id = data.get("user_id")
        book_id = data.get("book_id")

        if not user_id or not book_id:
            return JsonResponse({"error": "Missing user_id or book_id"}, status=400)

        is_taken = Loan.objects.filter(book_id=book_id, is_returned=False).exists()
        if is_taken:
            return JsonResponse({"error": "Book is already loaned"}, status=409)

        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return JsonResponse({"error": "Book does not exist"}, status=404)

        try:
            user = get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return JsonResponse({"error": "User does not exist"}, status=404)

        loan = Loan.objects.create(book=book, user=user)
        return JsonResponse({
            "user_id": user_id,
            "book_id": book_id,
            "loan_id": loan.id
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
def get_loans_by_user_id(request):
    try:
        user_id =request.GET.get("user_id")
        loans= list(Loan.objects.filter(user__id=user_id).values())
        return JsonResponse(loans,safe=False)
    except:
        return JsonResponse("somethings is wrong")