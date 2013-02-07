from django.shortcuts import render
from nomr.models import Book, Printer, PrintingTechnology, Genre

def search(request):
    if 'q' not in request.GET:
        return _show_search(request)
    else:
        return _show_results(request)

def _show_search(request):
    # generate facet data
    data = {
        'printers': sorted([p.name for p in Printer.objects.all()]),
        'printing_technologies': sorted([pt.technology_type for pt in PrintingTechnology.objects.all()]),
        'locations': sorted([b.location for b in Book.objects.all()]),
        'genres': sorted([g.genre_name for g in Genre.objects.all()])
    }

    return render(request, 'search.html', data)

def _show_results(request):
    return render(request, 'results.html')
