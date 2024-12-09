from django.contrib import admin
from .models import Book,BorrowRequest
# Register your models here.
admin.site.register(Book)
admin.site.register(BorrowRequest)