# advanced_search.py
# Implementing Boolean retrieval model using Whoosh python module
# Group: Ctructure
# Date: Nov 25, 2017

import os, os.path
import datetime
import get_law_fields
from whoosh import index
from whoosh.fields import Schema, TEXT, ID, STORED, DATETIME 
from whoosh.analysis import StemmingAnalyzer


# import stopwords
with open("search_static/stopwords.txt", 'r') as f:
  stopwords = sorted(list(f.read().split('\n')))

lang_ana = StemmingAnalyzer(stoplist = stopwords)

# CREATE A SCHEMA
"""
The schema defines the fields that each document 
(i.e. law in most cases) may contain. 

law_name -- name of the document. Searchable and stored.
law_body -- the intro and articles of a law. Searchable only.
law_num_date -- the number of the law and the exact date. Searchable and stored.
pub_date -- the date of the Official Gazette publication.
article_one -- title and first few sentences of article one. Stored only for displaying in search results.

"""

schema = Schema(
                law_name = TEXT(analyzer=lang_ana, stored=True),
                law_body = TEXT(analyzer=lang_ana),
                law_num_date = ID(stored=True),
                # content type
                pud_date = DATETIME(sortable=True, stored=True),
                article_one = STORED
               )

# CREATE AN INDEX
"""
The documents will be stored according to the defined schema.
Fields that are indexed can be "searched." Some fields can be 
stored without being indexed... just to show up search results.
"""

# To create (or open existing) index directory
if os.path.exists("indexdir"):
  ix = index.open_dir("indexdir")

else:
  os.mkdir("indexdir")
  ix = index.create_in("indexdir", schema)

writer = ix.writer()





