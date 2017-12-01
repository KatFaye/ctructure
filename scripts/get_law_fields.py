# Function that takes a law file 
# AND returns all the fields for 
# Whoosh schema

import datetime


def list_from_file(filename):
  """ Simply returns a file as a list of lines
     filename -- path of a file
  """

  with open(filename, 'r') as f:
    raw_data = f.read()
  
  return raw_data.split('\n')


def get_fields(file_lines):
  """ Get fields from file_lines 
      file_lines - list of lines in the file
  """
  fields = {}  
 
  fields["content_type_tag"] = file_lines[1]
  law_name = file_lines[2]
  fields["law_name"] = law_name

  # Get law number & exact date from the name
  law_num = law_name.split()[1]
  law_exact_date = law_name.split()[3]
  law_num_date = law_num + '_' + law_exact_date
  fields["law_num_date"] = law_num_date 
 
  # Get Official Gazette from 4th line (4rd index)
  pub_date_raw = file_lines[3].split()[-1]
  day, month, year = [int(i) for i in pub_date_raw.split('/')]
  pub_date = datetime.datetime(year, month, day)
  fields["pub_date"] = pub_date
  
  fields["agency_tag"] = file_lines[4]

  # Get first few lines of article-one
  """ The lines below save the title of article-one
      Then get the first 50 words of article one or all
      words (whichever has the lower count
  """
  article_one_title = ' '.join(file_lines[6].split()[2:])
  article_one_words = file_lines[7].split()
  article_one_len = len(article_one_words)
  word_count = article_one_len if article_one_len < 50 else 50
  article_one_str =  ' '.join(article_one_words[:word_count])
  
  fields["article_one_title"] = article_one_title
  fields["article_one_str"] = article_one_str

  # Get the body of the law
  """ From article-one and everything below.
      Intentionally skipping 'intro' - may add later
  """
  law_body = ' '.join(file_lines[6:])
  fields["law_body"] = law_body

  return fields

# test script
"""
file_path = "demo_laws/Law_N-_20-2009_of_29-07-2009"
file_list = list_from_file(file_path)
file_fields = get_fields(file_list)

for field in file_fields:
  print field, file_fields[field], '\n'

"""
  
  
  
