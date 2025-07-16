from django.contrib import admin
from .models import Book,BookDetail,Author,Review,Genre,Loan
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
import datetime
from django.utils import timezone

User = get_user_model()
admin.site.site_header="Panel de prestamo de libros"


@admin.action(description="Marcar préstamos como devueltos")
def mark_as_returned(modeladmin, request, queryset):
    prestamos_no_devueltos = queryset.filter(is_returned=False)
    prestamos_no_devueltos.update(is_returned=True, return_date=timezone.now().date())
    for i in queryset:
        print(i.book)
    
class LoanInLine(admin.TabularInline):
    model=Loan
    extra=1


class ReviewInLine(admin.TabularInline):
    model =Review 
    extra =1
class BookDetailInLine(admin.TabularInline):
    model= BookDetail
    extra=1
    can_delete =False
    verbose_name_plural ="Detalle de libro"
class BookAdmin(admin.ModelAdmin):
    inlines = [ReviewInLine,BookDetailInLine]
    list_display= ("title","author","pages","publication_date")
    search_fields = ("title", "author__name")
    list_filter = ("author","genres","publication_date")
    ordering = ["publication_date"]
    date_hierarchy = "publication_date"
    autocomplete_fields = ["author"]
class GetUserModelAdmin(BaseUserAdmin):
    list_display=["username","email"]
    inlines=[LoanInLine]
class AuthorAdmin(admin.ModelAdmin):
    list_display=["name"]
    search_fields = ["name"]

class LoanAdmin(admin.ModelAdmin):
    list_display =["user","book","loan_date","return_date","is_returned"]
    readonly_fields =['loan_date']
    actions =[mark_as_returned]
    
    
    
admin.site.register(Book,BookAdmin)
admin.site.register(BookDetail)
admin.site.register(Author,AuthorAdmin)
admin.site.register(Review)
admin.site.register(Genre)
admin.site.register(Loan,LoanAdmin)

try:
    admin.site.unregister(User)
except admin.sites.NotRegistered :
    pass

admin.site.register(User,GetUserModelAdmin)