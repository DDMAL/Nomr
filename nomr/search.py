from django.conf import settings
from django.shortcuts import render
import solr

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
    sanitized_q = u""

    q = request.GET['q']
    if q == u"":
        sanitized_q = "*:*"
    else:
        sanitized_q = "text:%s" % q
    
    s_conn = solr.SolrConnection(settings.SOLR_SERVER)
    response = s_conn.select(sanitized_q)

    data = {
        'results': response.results
    }

    return render(request, 'results.html', data)
