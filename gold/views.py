from django.template import RequestContext
from django.shortcuts import render_to_response
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from gold.models import Book
from gold.serializers import BookSerializer

def home(request):
    '''
    Serve the home page
    '''

    return render_to_response('index.html', context_instance=RequestContext(request))

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'book-list': reverse('book-list', request=request, format=format),
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
