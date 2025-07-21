from django.http import JsonResponse,HttpResponse
from django.urls import path
from . import views
urlpatterns = [
    path("get_books/",views.get_books),
    path("verify_user/",views.verify_user)
]