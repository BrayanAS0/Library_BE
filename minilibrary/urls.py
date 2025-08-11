from django.http import JsonResponse,HttpResponse
from django.urls import path
from . import views
urlpatterns = [
    path("get_books",views.get_books),
    path("login",views.login),
    path("sign_up",views.signup),
    path("get_book_index",views.Book_index),
    path("Book_with_detail",views.book_with_detail),
    path("loan_books",views.loan_books),
    path("get_loans_by_user_id",views.get_loans_by_user_id)
]