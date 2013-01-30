from django.template import RequestContext
from django.shortcuts import render_to_response
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from nomr.models import Book, BookPart, Page
from nomr.serializers import BookSerializer, BookPartSerializer, PageSerializer

def home(request):
    '''
    Serve the home page
    '''

    return render_to_response('index.html', context_instance=RequestContext(request))

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'book-list': reverse('book-list', request=request, format=format),
        'book-part-list': reverse('book-part-list', request=request, format=format),
        'page-list': reverse('page-list', request=request, format=format)
    })

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

class BookPartList(generics.ListAPIView):
    '''
    Displays a list of all of the book parts entered into the database.
    '''

    model = BookPart
    serializer_class = BookPartSerializer

class BookPartDetail(generics.RetrieveAPIView):
    '''
    Retrieves information about a single book part.
    '''

    model = BookPart
    serializer_class = BookPartSerializer

class PageList(generics.ListAPIView):
    '''
    Displays a list of all of the book parts entered into the database.
    '''

    model = Page
    serializer_class = PageSerializer

class PageDetail(generics.RetrieveAPIView):
    '''
    Retrieves information about a single book part.
    '''

    model = Page
    serializer_class = PageSerializer
