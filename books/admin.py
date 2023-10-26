from django.contrib import admin
from books.models import *


# Register your models here.

admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Category)
admin.site.register(Book)