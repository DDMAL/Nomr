from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
import solr
import os
import uuid

from nomr.models import Book, BookPart, Page
from nomr.resources.generateglyphs import GlyphGen

def glyphs(request):
    sanitized_q = u""

    q = request.GET.get('q')
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
    response = s_conn.select(sanitized_q, fq=fq)

    # create a folder in the media root for the glyphs to be generated
    # folder name will be a generated UUID for now
    glyph_folder_name = 'glyphs/%s' % uuid.uuid4()
    glyph_collection_path = os.path.join(settings.MEDIA_ROOT, glyph_folder_name)
    glyph_collection_url = os.path.join(settings.MEDIA_URL, glyph_folder_name)

    try:
        os.makedirs(glyph_collection_path)
    except OSError:
        # uuids are unique, so this should never be thrown
        err_msg = 'There was an error generating the glyphs for the given search query. Please try again.'
        return render_to_response('error.html', {'msg': err_msg}, context_instance=RequestContext(request))

    # for each book, get the pages
    for b in response.results:
        # get page image links
        book_part = BookPart.objects.get(book=b['uuid'])
        pages = Page.objects.filter(book_part=book_part.uuid)
        
        image_paths = [str(os.path.join(settings.MEDIA_ROOT, p.image.name)) for p in pages]
        mei_paths = [str(os.path.join(settings.MEDIA_ROOT, p.mei.name)) for p in pages]
        for image_path, mei_path in zip(image_paths, mei_paths):
            # for each image and mei pair
            gg = GlyphGen(image_path, mei_path)
            gg.gen_glyphs(glyph_collection_path)

    # get list of relative urls to the generated glyphs
    glyph_urls = []
    for glyph_file in os.listdir(glyph_collection_path):
        glyph_urls.append(os.path.join(glyph_collection_url, glyph_file))

    return render_to_response('glyphs.html', {'glyphs': glyph_urls}, context_instance=RequestContext(request))
