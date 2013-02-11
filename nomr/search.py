from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import EmptyPage
import solr

from nomr.models import Book, Printer, PrintingTechnology, Genre
from nomr.resources.solrpaginate import SolrPaginator, SolrPage

def search(request):
    if 'q' not in request.GET:
        return _show_search(request)
    else:
        return _show_results(request)

def _show_search(request):
    pub_dates = [b.publication_date for b in Book.objects.all()]

    # generate facet data
    data = {
        'printers': sorted([p.name for p in Printer.objects.all()]),
        'printing_technologies': sorted([pt.technology_type for pt in PrintingTechnology.objects.all()]),
        'locations': sorted([b.location for b in Book.objects.all()]),
        'genres': sorted([g.genre_name for g in Genre.objects.all()]),
        'min_publication_date': min(pub_dates).isoformat(),
        'max_publication_date': max(pub_dates).isoformat()
    }

    return render_to_response('search.html', data, context_instance=RequestContext(request))

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


    start_date = request.GET.get('startdate')
    end_date = request.GET.get('enddate')
    if start_date and end_date:
        sanitized_q += (' AND publication_date:[%sT00:00:00.000Z TO %sT00:00:00.000Z]' % (start_date, end_date))

    s_conn = solr.SolrConnection(settings.SOLR_SERVER)
    response = s_conn.select(
        sanitized_q,
        fq=fq,
        facet='true',
        facet_field=['location', 'genres', 'printers', 'printing_technology'],
        facet_mincount=1,
        rows=settings.SOLR_PAGE_SIZE
    )

    try:
        # get page number
        page_num = int(request.GET.get('page', 1))
    except ValueError:
        page_num = 1

    # default page size is set to rows=settings.SOLR_PAGE_SIZE
    paginator = SolrPaginator(response)

    try:
        page = paginator.page(page_num)
    except EmptyPage:
        # generate an empty page, i.e., one with no results to display
        page = SolrPage([], 1, paginator)

    data = {
        'paged_results': page,
        'facets': response.facet_counts['facet_fields'],
    }

    return render_to_response('results.html', data, context_instance=RequestContext(request))
