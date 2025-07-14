from django.contrib import admin


from .models import Book,BookDetail,Author,Review,Genre,Loan

class BookAdmin(admin.ModelAdmin):
    list_display= ("title","author","pages","publication_date")
    search_fields = ("title", "author__name")


admin.site.register(Book,BookAdmin)
admin.site.register(BookDetail)
admin.site.register(Author)
admin.site.register(Review)
admin.site.register(Genre)
admin.site.register(Loan)
