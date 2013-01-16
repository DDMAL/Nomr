from django.template import RequestContext
from django.shortcuts import render_to_response
from rest_framework import generics

from gold.models import Book
from gold.serializers import BookSerializer

def home(request):
    '''
    Serve the home page
    '''

    return render_to_response('index.html', context_instance=RequestContext(request))

class BookList(generics.ListAPIView):
    '''
    Displays a list of all of the books entered into the database.
    '''

    model = Book
    serializer_class = BookSerializer

class BookDetail(generics.RetrieveAPIView):
    '''
    Retrieves information about a single book.
    '''

    model = Book
    serializer_class = BookSerializer
