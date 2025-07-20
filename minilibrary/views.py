from django.http import JsonResponse
from .models import Book

def get_books(request):
    author_id = request.GET.get("author")
    books = Book.objects.all()

    if author_id:
        books = books.filter(author__pk=author_id)

    books_data = list(books.values())  # <-- con list()

    return JsonResponse(books_data, safe=False)

    return render(request,"minilibrary/minilibrary.html",{"author":"brayan","books":books_data})
    # return JsonResponse(list(books_data), safe=False)
