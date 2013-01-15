from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from gold.models import Book
from gold.serializers import BookSerializer

def home(request):
    '''
    Serve the home page
    '''

    return render_to_response('index.html', context_instance=RequestContext(request))

@api_view(['GET'])
def book_list(request):
    '''
    Displays a list of all of the books entered into the database.
    '''

    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books)

        return Response(serializer.data)

@api_view(['GET'])
def book_detail(request, uuid):
    '''
    Retrieves information about a single book.
    '''

    book = get_object_or_404(Book, pk=uuid)

    if request.method == 'GET':
        serializer = BookSerializer(book)

        return Response(serializer.data)
