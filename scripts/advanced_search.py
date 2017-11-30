# advanced_indexing.py
# Implementing Boolean retrieval model using Whoosh python module
# Group: Ctructure
# Date: Nov 25, 2017

import os, os.path
import datetime
from whoosh import index
from whoosh.fields import Schema, TEXT, ID, STORED, DATETIME 
from whoosh.analysis import StemmingAnalyzer
from get_law_fields import list_from_file, get_fields
from whoosh.qparser import QueryParser

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
                # content type & agency
                pub_date = DATETIME(sortable=True, stored=True),
                article_one_title = STORED,
                article_one_str = STORED
               )

# CREATE AN INDEX
"""
The documents will be stored according to the defined schema.
Fields that are indexed can be "searched." Some fields can be 
stored without being indexed... just to show up search results.
"""  

# To create (or open existing) index directory
if os.path.exists("indexdir"):
  index = index.open_dir("indexdir")

else:
  os.mkdir("indexdir")
  index = index.create_in("indexdir", schema)

# start indexing documents
file_list = os.listdir("demo_laws")

writer = index.writer()

def get_unicode(string):
  return unicode(string, 'utf-8')

for doc in file_list:
  if os.path.isfile("demo_laws/" + doc):
    file_lines = list_from_file("demo_laws/"+doc)
    file_fields = get_fields(file_lines)
  
    law_name = file_fields["law_name"]
    law_body = file_fields["law_body"]
    law_num_date = file_fields["law_num_date"]
  
    pub_date = file_fields["pub_date"]
    article_one_title = file_fields["article_one_title"]
    article_one_str = file_fields["article_one_str"]  
    
    writer.add_document(law_name = get_unicode(law_name),
                        law_body = get_unicode(law_body),
                        law_num_date = get_unicode(law_num_date),
  
                        pub_date = pub_date,
                        article_one_title = article_one_title,
                        article_one_str = article_one_str
                       )
writer.commit()

# define fields to search
qp = QueryParser("law_body", schema=index.schema)  

with index.searcher() as searcher:
  query = qp.parse("law")
  results = searcher.search(query)
  print(len(results))



