from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=50,unique=True)


class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_date = models.DateField(null=True, blank=True)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='books')
    pages = models.IntegerField()
    isbn = models.CharField(max_length=50)
    genre =models.ManyToManyField(Genre,related_name='books')

    def __str__(self):
        return self.title
class BookDetail(models.Model):
    summary = models.TextField()
    cover_url= models.CharField()
    language = models.CharField()
    book= models.OneToOneField(Book,related_name="detail",on_delete=models.CASCADE)

class Review(models.Model):
    user= models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    book=models.ForeignKey(Book,on_delete=models.CASCADE,related_name="reviews")
    rating = models.PositiveIntegerField()
    text = models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} -> {self.book.title} ({self.rating/5})" 

class Loan(models.Model):
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    book= models.ForeignKey(Book,models.CASCADE,related_name="loans")
    loan_date= models.DateTimeField(auto_now_add=True)
    return_date= models.DateTimeField(blank=True,null=True)
    is_returned =models.BooleanField(default=False)
    
    def __str__(self):
        return f"/n{self.user} -> {self.book.title} -> {"Devuelto"if self.is_returned else "No Devuelto"}"
    