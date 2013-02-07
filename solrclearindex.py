#!/usr/bin/env python
import solr
import sys
import os

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nomr.settings")
    from django.conf import settings

    print 'Connecting to Solr Server ...'

    try:
        s_conn = solr.SolrConnection(settings.SOLR_SERVER)
    except Exception:
        print 'Failed to open connection'
    else:
        print 'Success'

    print "Clearing Solr index ..."

    s_conn.delete_query("*:*")
    s_conn.commit()
    
    print "Done"

    sys.exit()
