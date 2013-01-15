from gold.models import Book, BookPart, Page
from gold.models import Printer, PrintingTechnology, Genre, AlternateBookID
from django.contrib import admin

admin.site.register(Book)
admin.site.register(BookPart)
admin.site.register(Page)
admin.site.register(Printer)
admin.site.register(PrintingTechnology)
admin.site.register(Genre)
admin.site.register(AlternateBookID)
