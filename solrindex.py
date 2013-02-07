#!/usr/bin/env python

import solr
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nomr.settings")

    from django.conf import settings
    from nomr.models import Book

    print 'Connecting to Solr Server ...'

    try:
        s_conn = solr.SolrConnection(settings.SOLR_SERVER)
    except Exception:
        print 'Failed to open connection'
    else:
        print 'Success'

    print 'Indexing Books ...'

    books = Book.objects.all()
    books_data = []
    for b in books:
        data = {
            'uuid': b.uuid,
            'title': b.title,
            'description': b.description,
            'is_manuscript': b.is_manuscript,
            'printers': [p.name for p in b.printers.all()],
            'publication_date': b.publication_date,
            'location': b.location,
            'printing_technology': b.printing_technology.technology_type,
            'genre': [g.genre_name for g in b.genre.all()],
            'is_sacred': b.is_sacred,
        }

        if b.alternate_id:
            data['alternate_id'] = b.alternate_id.id

        books_data.append(data)

    s_conn.add_many(books_data)
    s_conn.commit()

    print 'Done'

    sys.exit()
