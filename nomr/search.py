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
    if not q:
        sanitized_q = "*:*"
    else:
        # perform search on general text field (concatenation of all fields)
        sanitized_q = "text:%s" % q
    
    # get facet queries
    fq = request.GET.getlist('fq')

    s_conn = solr.SolrConnection(settings.SOLR_SERVER)
    response = s_conn.select(
        sanitized_q,
        fq=fq,
        facet='true',
        facet_field=['location', 'genres', 'printers', 'printing_technology'],
        facet_mincount=1
    )

    data = {
        'results': response.results,
        'facets': response.facet_counts['facet_fields']
    }

    return render(request, 'results.html', data)
