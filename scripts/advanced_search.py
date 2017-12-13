# advanced_indexing.py
# Implementing Boolean retrieval model using Whoosh python module
# Group: Ctructure
# Date: Nov 25, 2017

import os
import os.path
import datetime
from whoosh import index
from whoosh import query
from whoosh.fields import Schema, TEXT, ID, STORED, DATETIME, KEYWORD, NUMERIC
from whoosh.analysis import StemmingAnalyzer
from get_law_fields import list_from_file, get_fields
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh.query import Query, Term, And


# import stopwords
with open("scripts/search_static/stopwords.txt", 'r') as f:
  stopwords = sorted(list(f.read().split('\n')))

lang_ana = StemmingAnalyzer(stoplist=stopwords)

# CREATE A SCHEMA
"""
The schema defines the fields that each document 
(i.e. law in most cases) may contain. 

law_name -- name of the document. Searchable and stored.
law_body -- the intro and articles of a law. Searchable only.
law_num_date -- the number of the law and the exact date. Searchable and stored.
pub_year -- the date of the Official Gazette publication.
article_one -- title and first few sentences of article one. Stored only for displaying in search results.

"""

schema = Schema(
    law_name=TEXT(analyzer=lang_ana, stored=True),
    law_body=TEXT(analyzer=lang_ana),
    law_num_date=ID(stored=True),

    # A doc can have multiple
    agency_tag=KEYWORD(stored=True),
    content_type_tag=KEYWORD(stored=True),

    pub_year=NUMERIC(sortable=True, stored=True),
    article_one_title=STORED,
    article_one_str=STORED
)

# CREATE AN INDEX
"""
The documents will be stored according to the defined schema.
Fields that are indexed can be "searched." Some fields can be 
stored without being indexed... just to show up search results.
"""

# To create (or open existing) index directory
if os.path.exists("scripts/indexdir"):
  index = index.open_dir("scripts/indexdir")

else:
  os.mkdir("scripts/indexdir")
  index = index.create_in("scripts/indexdir", schema)

# start indexing documents
file_list = os.listdir("scripts/demo_laws")


def get_unicode(string):
  return unicode(string, 'utf-8')

# MAIN_WRITELOCK file gets created after initiating the writer object (below)
# it's a simple way to know that we have already indexed documents


if not os.path.exists("scripts/indexdir/MAIN_WRITELOCK"):

  writer = index.writer()

  for doc in file_list:
    if doc[0] == '.':
      continue  # skip hidden files
    if os.path.isfile("scripts/demo_laws/" + doc):
      """
      The list_from_file function returns the raw file as 
      a list of lines. 
      The get_fields func returns a dictionary with field values
      """
      file_lines = list_from_file("scripts/demo_laws/" + doc)
      file_fields = get_fields(file_lines)

      law_name = file_fields["law_name"]
      law_body = file_fields["law_body"]
      law_num_date = file_fields["law_num_date"]

      agency_tag = file_fields["agency_tag"]
      content_type_tag = file_fields["content_type_tag"]

      pub_year = file_fields["pub_year"]
      article_one_title = file_fields["article_one_title"]
      article_one_str = file_fields["article_one_str"]

      writer.add_document(law_name=get_unicode(law_name),
                          law_body=get_unicode(law_body),
                          law_num_date=get_unicode(law_num_date),

                          agency_tag=get_unicode(agency_tag),
                          content_type_tag=get_unicode(content_type_tag),

                          pub_year=pub_year,
                          article_one_title=article_one_title,
                          article_one_str=article_one_str
                          )
  writer.commit()

else:
  pass  # No need to index documents again (i.e. duplicates)


# define fields to search
qp = MultifieldParser(["law_body", "law_name"], schema=index.schema)


def build_filters(agency_in=None, content_type_in=None, pub_year_in=None):
  # build the search query given user selections
  agency = content_type = pub_year = None
  user_filter = None

  # if there is an agency filter
  if agency_in:
    agency = agency_in
  # if there is a content_type filter
  if content_type_in:
    content_type = content_type_in
  # if there is a publication date filter
  if pub_year_in:
    pub_year = pub_year_in

  # Do all combinations of the filters
  # 1. No filters selected
  if not agency and not content_type and not pub_year:
    user_filter = None
  # 2. All filters are selected.
  if agency and content_type and pub_year:
    user_filter = And([Term("agency_tag", get_unicode(agency)),
                       Term("content_type_tag", get_unicode(content_type)),
                       Term("pub_year", pub_year)])

  # 3. agency and content_type
  if agency and content_type and not pub_year:
    user_filter = And([Term("agency_tag", get_unicode(agency)),
                       Term("content_type_tag", get_unicode(content_type))])
  # 4. agency and pub_year
  if agency and pub_year and not content_type:
    user_filter = And([Term("agency_tag", get_unicode(agency)),
                       Term("pub_year", pub_year)])
  # 5. content_type and pub_year
  if content_type and pub_year and not agency:
    user_filter = And([Term("content_type_tag", get_unicode(content_type)),
                       Term("pub_year", pub_year)])

  # 6. Agency alone
  if agency and not pub_year and not content_type:
    user_filter = And([Term("agency_tag", get_unicode(agency))])
  # 7. Content_type alone
  if content_type and not pub_year and not agency:
    user_filter = And([Term("content_type_tag", get_unicode(content_type))])
  # 8. pub_year alone
  if pub_year and not agency and content_type:
    user_filter = And([Term("pub_year", pub_year)])

  return user_filter


def get_results(_agency, _year, _content_type, user_query):
  global index
  with index.searcher() as searcher:
    agency_in = _agency
    pub_year_in = _year
    content_type_in = _content_type

    user_filter = build_filters(agency_in=agency_in,
                                content_type_in=content_type_in,
                                pub_year_in=pub_year_in)

    query = qp.parse(user_query)
    results = searcher.search(query, filter=user_filter)
    new_list = []
    for r in results:
      new_list.append(r)
      print(r)

    return new_list
