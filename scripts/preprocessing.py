# Read raw .txt files right after conversion from PDFs.
# Organize into articles while ignoring unnecessary information. 

import os, sys, re
from fixlawname import FixLawName


"""
summary = Top section of the raw file where laws in the official gazette are listed. 
Headings = Names of laws in the summary. 
TOC = Table of Contents. Section outlining all chapters and/or articles in a given law.
"""

# make range for loop that goes through lines around the target line
loop_from_small = lambda n: [j for i in range(1,n) for j in [i, -i]]

def get_item(list_name, index):
  """check if list is long enough and return the element at the desired index"""
  if len(list_name) > index: return list_name[index]
  return '' # after applying split(), will result in empty list.

def str_between(doc_file, n_start, g_start, n_end, g_end):
  """ return string between token g_start in line n_start up to 
  token g_end in line n_end. Token at last index NOT included."""
  end_index = len(doc_file[n_start].split()) if n_start != n_end else g_end
  string_list = doc_file[n_start].split()[g_start:end_index]

  # stuff before the last line
  for n in range(n_start +1, n_end):
    string_list.append('\n')
    doc_line = doc_file[n].split()
    for token in doc_line:
      string_list.append(token)    
  
  # if n_start and n_end are equal, you should not add the same tokens twice. 
  if n_start != n_end: 
    string_list.append('\n')
    string_list.extend(doc_file[n_end].split()[:g_end])
  return ' '.join((' '.join(string_list)).split('\n')) #1 Join list 2 Split on '\n'. 3 Join again

def split_at_char(token, list_char):
  """If the token has any character in list_char, exclude the part after the char"""
  new_str = ''
  for char in token:
    new_str += char
    if char in list_char: return new_str   # return after adding ':'
  return token

def get_subdocs_indices(raw_file):
  """
  what does this mega function do? Should it become a class?
  """
  law_types = ['law','order','regulation', 'practice', 'commissioner']
  law_initials = ['law', 'presidential','organic','prime','ministerial','regulation', 
                  'practice', 'commissioner', 'presindential']
  law_no, law_no_symbols = ['no','n°','nº'], ['°','º']
  first_art_no = ['one', '1', 'one:', '1:']
  heading_end = ['…','.']
  heading_end = [x.lower() for x in heading_end]
  non_english = ['loi', 'itegeko', 'iteka', 'arrêté', 'règlement', 'amabwiriza', 'directives']
   
  print('\n',raw_file,'\n')
  
  def get_pub_name(current_line, n):
    """Get name of the publication / Official Gazette"""
    pub_name_found = False
    long_form, short_form = False, False
    pub_name, short_og, long_og = '', ['og', 'o.g.'], ['official', 'gazette']
   
    if current_line[0] in short_og: short_form = True
    elif current_line[:2] == long_og: long_form = True
    else: return pub_name_found, pub_name
 
    # if it's long_form, 'n°' is shifted to the right by 1. 
    index = 1 if short_form else 2
    if len(current_line[index]) >= 2 and current_line[index][:2] in law_no:
      pub_name_found = True
      pub_name = current_line
      
      """'If statements' below fix name (replace 'og' with long_form 
         and separate 'n°' and the og number if attached in one string."""
      if short_form: pub_name = long_og + pub_name[1:]
      if len(pub_name[2]) > 2: 
        pub_name = pub_name[:2] + [pub_name[2][:2]] + [pub_name[2][2:]] + pub_name[3:]

      return pub_name_found, ' '.join(pub_name)

    return pub_name_found, pub_name


  def check_summary_headings(n, current_line):
    """In the summary of OG, laws (etc) are introduced as
       N° <law_number> of <date> e.g. N° 19/01 of 21/03/2011  
       line below takes into account that sometimes 
       there is no whitespace between N° and <law_number> """
   
    if len(current_line) in [3,4] and post_summary== False and \
    ((current_line[0] in law_no and current_line[2] == 'of') or \
    (current_line[0][:2] in law_no and current_line[1] == 'of')):
      return True
    
    return False


  def get_heading_order(n):
    """Find order of the summary: heading by language or by law number?
       Technically, this function is not essential, though, it helps with organizing."""
    nonlocal heading_order
    eng_headings  = 0
    for y in loop_from_small(8): # Why 8? Hard-coding. Not effective.
      doc_line = get_item(doc_file, n + y).split()
      if len(doc_line) > 0:

        # if line starts with english word
        if doc_line[0] in law_initials:
          eng_headings += 1
          # if you see english word twice 
          # before seeing non-english, break
          if eng_headings == 2:
            heading_order = 'by_language'
            break
        # if line starts with kinya/french word
        if doc_line[0] in non_english:
          heading_order = 'by_law_number'
          break
    return heading_order

  def get_subname(start_index):
    """This function returns the name of a law.
       There can be multiple laws in one raw/file.
      
       start_index -- where the name starts"""
     
    line_i, token_i = start_index, 0
    name_found = False # Have you found the end of the name (or start of a new name)
    last_token = '' # last token with heading-end characters

    while not name_found:
      token, line_i, token_i = get_next_token(doc_file, line_i, token_i)
      for c in range(len(token)):
        last_token = token[:c] # I see. To avoid 'heading-end' stuff on the name.
        # Spotting law ending: we wanna find heading_end i.e. a sequence of dots.
        if token[c] in heading_end and len(token) > c + 1 and token[c] == token[c+1]:
          name_found = True
          break 
      # encountering a new heading
      if check_summary_headings(line_i, get_item(doc_file, line_i).split()):
        name_found = True
     
    return str_between(df_case_sensitive, start_index, 0, line_i, token_i)+' '+ last_token
  
  def get_law_numbers(initial_index):
    """After identifying that the current-line is a law title, 
       we must check if that title was seen in the summary, (as 
       opposed to another law just referenced in the document) 

    initial_index -- index of the line where the law title was seen"""
 
    digits_near_name = []
    # next three lines (lines are usually broken)
    for m in range(5):  #Why 5? Hard-coding. Not effective.
      next_line = get_item(doc_file, initial_index + m).split()
      for w in next_line:
        # word starts & ends with a digit, save it
        if w[0].isdigit(): 
          digits = w
          if len(w) > 2 and w[-2:] == 'of': digits = w[:-2]
          digits_near_name.append(w)
        
        # or word start with no..., save it
        if len(w) > 2 and w[:2] in law_no and w[2].isdigit(): 
          digits = w[2:]
          if len(w) > 4 and w[-2:] == 'of': digits = w[2:-2]
          digits_near_name.append(digits)
    
    return digits_near_name 

  def add_law_titles_indices(n, law_numbers):
    """So, we have identified all digits near the law name/title. 
       Here, we check if any of the digits is associated to a law 
       in the Summary, if so, we add the index to sub-docs."""
   
    nonlocal sub_docs
    match_found = False
    for digits in digits_near_name:
      for doc in sub_docs:
        no_of_law = doc[1]
        # if the law was seen/saved in Summary
        if digits == no_of_law:
          if 'toc_title' in sub_docs[doc]:
            sub_docs[doc]['body_title'] = n
        
          else:
            sub_docs[doc]['toc_title'] = n
           

  # Article One appears twice in a law: TOC &  body. 
  def find_article_one(current_line, n):
    """Appends index of 'article one' to first_articles, and
       return True if you found.
    """
    nonlocal first_articles

    # if article is already indexed, no need to do it again
    if n in first_articles: return True 

    art_str, article_found = "article", False
    match_str = current_line[0] # equal to token at 1st index of line.    

    # finds and fixes article headings spelled as 'a r t i c l e' with whitespaces. 
    if len(current_line) >= 7 and ''.join(current_line[:7]) == art_str:      
      match_str = art_str
      doc_file[n] = art_str + ' ' + ' '.join(current_line[7:]) # modifying doc_file

    if match_str != art_str: return article_found  # index zero should be 'article'
    # check if the next token is in ['1', '1:', 'one', 'one:']

    next_token, line_i, token_i = get_next_token(doc_file, n, 0) # token and its position
    # if there is no whitespace after first_art_no, fix it
    next_token = split_at_char(next_token, [':'])

    if next_token in first_art_no:
      first_articles.append(n)
      article_found = True
    
    # change next token to '1' in doc-file if it's something else
    if article_found and next_token not in ['1', '1:']:
      digit_one = '1' if next_token == 'one' else '1:'
      modified_line = doc_file[line_i].split()
      modified_line[token_i] = digit_one
      doc_file[line_i] = ' '.join(modified_line)
      df_case_sensitive[line_i] = ' '.join(modified_line)	# Save changes to case sensitive version 

    return article_found

  def check_ending(current_line, n):
    """find where a doc ends by targetting 'Commencement'
       e.g.1. 'Article 43: Commencement'
       e.g.2. 'Article 43 : Commencement'"""
 
    nonlocal law_endings
    kigali_words = ['kigali', 'kigali,', 'kigali.', 'kigali;']

    found_commencement, found_this, found_kigali = False, False, False
    # the exact number of tokens-until-'This' is 4. 'article' '#' ':' 'commen..' 'this'
    num_of_tokens, tokens_until_this = 0, 8  # Double for caution

    if not is_article_heading(doc_file, n, 0)[0]: return     
    
    line_i, token_i = n, 0
    while num_of_tokens < tokens_until_this: # loop from the next eight tokens.
      token, line_i, token_i = get_next_token(doc_file, line_i, token_i)
      if token == 'commencement': found_commencement = True
      if token_i == 0 and token in ['this', 'these']: found_this = True
      if found_commencement and found_this: break
      num_of_tokens += 1
   
    # if we could not identify 'this' (at index 0) and 'commencement' next to each other
    if not (found_commencement and found_this): return

    num_of_tokens = 0
    last_article_size = 100 # Arbitrary number. We should find 'Kigali' before 100 tokens
 
    # Find where the last article ends. Target keyword 'kigali..' 
    while num_of_tokens < last_article_size:
     token, line_i, token_i = get_next_token(doc_file, line_i, token_i)
     if token in kigali_words:
       law_endings.append(line_i)
       found_kigali = True
       break
     num_of_tokens += 1
    
    assert found_kigali, "Could not find law ending ('kigali...') at line " + str(n)
 
    return  

  #####################################################
  # IMPLEMENTATION OF THE PROGRAM'S LOGIC STARTS HERE #
  #####################################################

  doc_file, df_case_sensitive = [], []    # entire raw-file is put into doc-file line-by-line before manupilation
  """First, the entire file is stored in a list this is important. for any line, we can find the prev. 
       or next (or further) line as needed. We also keep a copy that is case sensitive. """
  f = open(raw_file,'r', encoding='utf-8')
 
  raw = f.read()

  fixln_obj = FixLawName(raw)     
  doc_file_raw = fixln_obj.fix_name()
  
  doc_file = doc_file_raw.lower().split('\n')

  df_case_sensitive = doc_file_raw.split('\n')	# case sensitive copy
   
  f.close()
  
  
  sub_docs = {}    #One document can contain multiple laws/legal docs
  first_articles  = []    # No 1 articles in each sub document
  law_endings = []  # The last article in each law/doc
  heading_order = 'unk'
  post_summary, pub_name_found = False, False
  pub_name = '' #name of the publication/official gazette
  unfound = "Could NOT find" # print if cannot find something 


  # Get the O.G. name and remove the recurring lines from both copies
  pub_name, found_once = '',  False
  for i in range(len(doc_file)):
    current_line = doc_file[i].split()

    if len(current_line) >= 3:

      og_name_status, line = get_pub_name(current_line, i)
      if og_name_status and not found_once:
        pub_name = line # will return pub_name at the end of this func
        found_once = True # found the publication's name
      elif og_name_status and found_once:
        doc_file[i] = '' # replacing the line with empty space
        df_case_sensitive[i] = ''

      else:
        pass

 
  for n in range(len(doc_file)):
    """IMPORTANT: n is the current index in doc-file. 
       line_number is the # of line in actual raw_file."""
    line_number = n+1
    current_line = doc_file[n]
    current_line = current_line.split()
     
    """
    # Find the name of the official gazette/ publication
    if len(current_line) >= 3 and not pub_name_found:
      name_search = get_pub_name(current_line, n)
      # if name was found, return name at index 1
      if name_search[0]: pub_name = name_search[1]
    """

    # check if the current line is a summary heading
    if check_summary_headings(n, current_line):
      # for each file, heading-order is checked only once
      if heading_order == 'unk':
         heading_order = get_heading_order(n)
 
      if heading_order in ['by_language', 'by_law_number']:
        # the 'if' below adds white space if absent
        subdoc_id = ' '.join(current_line) 
        if len(current_line) == 3:
          subdoc_id = (subdoc_id[:2] + ' ' + subdoc_id[2:])
    
        subdoc_id_upper = subdoc_id.split()
        subdoc_id_upper[0] = 'N°' # changing n to upper case N
        subdoc_id = tuple(subdoc_id.split()) # Tuple/immutable to be key in dictionary

        # This block is going to hunt the law's ENTIRE name (i.e. indices for start/end)
        if subdoc_id not in sub_docs:
          """The name of the law can be above or below the law number/date
             and it can be composed of multiple lines i.e. very long law name
             worse, same language laws can be subsequent
             first, let's figure out the case among the three possibilities."""

          bound_found = False
          for y in loop_from_small(6):
            doc_line = get_item(doc_file, n + y).split()
            if len(doc_line) > 0:
    	      # if line starts with keyword in law_initials
              if doc_line[0] in law_initials:
                name_start = n + y
                bound_found = True
                break

          # if the beg. of law's name was found
          if bound_found:
            sub_doc_name = get_subname(name_start) 
            law_type = get_law_type(sub_doc_name.lower()).split() # get_law_type returns str
            len_type = len(law_type) 
            sub_doc_name = ' '.join(sub_doc_name.split()[:len_type] + list(subdoc_id_upper) + sub_doc_name.split()[len_type:])
            
            
      assert heading_order != 'unk', '{0} HEADING ORDER for file {1} at line {2}\n'.format(unfound, raw_file, line_number)
      
      assert sub_doc_name != '', '{0} law name & bounds for file {1} at line {2} \n'.format(unfound, raw_file, line_number)
      
      sub_docs[subdoc_id] = {'heading_index':n, 'subdoc_name':sub_doc_name}


      ######################################################################
      # END OF THE SECOND IF STATEMENT THAT ANALYZES LAW HEADINGS/SUMMARY. #
      ######################################################################

    # finding where article 1 is. 
    if len(current_line) > 0:
      find_article_one(current_line, n)

    """After passing the Summary/TOC, we need to identify where 
       each law starts. Looks like: "Law No 120/02 of <date> ..."
       Then, we collect all digits near by and see if any of them
       corresponds to a law in the Summary."""
   
    if len(current_line) > 0 and current_line[0] in law_initials: 
       
      # check if we are still in the SUMMARY section
      next_token = get_next_token(doc_file, n, 0)[0]
      next_token = split_at_char(next_token, law_no_symbols)
      #print(post_summary, current_line, n)
      if post_summary == False and next_token in law_no:
        post_summary = True
      
      # if we're still in summary, we do NOT need to save toc_title and body_title 
      if post_summary:
       
        # save all the digits near the law initial 
        digits_near_name = get_law_numbers(n)            
        # for all tokens saved above
        # check if it's a # of law in summary
        add_law_titles_indices(n, digits_near_name)
          
    # Check if the <current-line> is the end of the law i.e. commencemnt article. 
    if current_line: check_ending(current_line, n) # if stat checks if not empty []
    
  # check if name of the publication was found:
  assert pub_name, "{0} publication name for {1} \n".format(unfound, raw_file)

  return (doc_file, sub_docs, first_articles, law_endings, pub_name, df_case_sensitive)

## Check what's missing
def find_skips(args):
    sub_docs, first_articles, law_endings = args[0], args[1], args[2]
    doc_sections = ['toc_title', 'body_title']
    for doc in sub_docs:
      print('\n', ' '.join(list(doc)),  ':')
      for section in doc_sections:
        if section in sub_docs[doc]: 
          print(section, "is available at", sub_docs[doc][section])
        else: 
          print(section, "IS MISSING! ***********", "heading index:", sub_docs[doc]['heading_index'])

    print("\nFirst articles (" + str(len(first_articles)) + "): \n", first_articles)
    print("\nLaw endings (" + str(len(law_endings)) + "): \n", law_endings, '\n')
    assert len(first_articles) == len(law_endings) * 2, '\n\n NOT all first articles and/or law endings were found.'
    print('\nAll first articles and law endings available')

    return 

def classify_sub_files(doc_file, args): 
  """Function below will extract indices for the new documents we are about to make.
     Each law within a publication/offical gazette will have its own text file""" 
  
  sub_docs, first_articles, law_endings, pub_name = args[0], args[1], args[2], args[3]
  
  heading_indices = sort_pairs('heading_index', sub_docs)   # law number/law ID
  toc_titles = sort_pairs('toc_title', sub_docs)    # title of 'law' in TOC
  body_titles = sort_pairs('body_title', sub_docs)    # title of 'law' in Body
  first_articles = sorted(first_articles)
  law_endings = sorted(law_endings)
  pub_date = pub_name.split()[-1]
    
   
  assert len(heading_indices) == len(toc_titles) == len(body_titles) == \
         len(law_endings), "Number of law Headings & Titles NOT consistent ****"
  assert len(law_endings) * 2 == len(first_articles), \
         "Number of law endings (commencements) and 'article one's NOT consistent"
 
  sub_files = {}
  
  def find_articles_one(m):
    """Returns article 1 in TOC and 'body' after making sure
    they belong in the same law

    m -- index of the sub-doc (law)
    """
    current_toc_title = toc_titles[m][1]
    current_body_title = body_titles[m][1]
    current_law_ending = law_endings[m]
 
    # 'article one' found. Two for each law (in toc and body)
    first_found = False
    toc_article_one, body_article_one = 0, 0
   
    for art_index in first_articles:
      # find where (toc_title) the next law starts
      if len(toc_titles) > m + 1: toc_title_next = toc_titles[m+1][1]
      else: toc_title_next = law_endings[-1] + 1
     
      # Here the order of the if statements below matters.
      if first_found and art_index < toc_title_next:
        body_article_one = art_index
        break # Found the position for law start. 
     
      """We check "article one" in Table of Contents (toc) first
         If this was done before the previous if stat, the prev if 
         statement would evaluate to true and save 'article one' in toc
         as the second 'article one' that we are targetting"""
     
      if current_toc_title < art_index < current_body_title:
        toc_article_one = art_index
        first_found = True          
 
    return toc_article_one, body_article_one, toc_title_next, current_body_title
 
  for m in range(len(heading_indices)):
    toc_article_one, body_article_one, toc_title_next, current_body_title = find_articles_one(m)
    
    assert body_article_one, "Could NOT find second 'article one' for file {0} \
           and sub-doc {1} \n".format(pub_name, heading_indices[m][0])
   
    sub_doc_ending = 0
    for ending in law_endings:  # ending between this range is unique. Look at the raw file.
      if body_article_one < ending < toc_title_next:  
        sub_doc_ending = ending        
        break # we have found the ending of the document. 

    assert sub_doc_ending, "Could NOT find 'law ending' for file {0} and sub-doc \
           {1}\n".format(pub_name, heading_indices[m][0])
    
    # Extract articles' headings from the law's Table of Contents
    article_headings = get_article_headings(doc_file, toc_article_one, current_body_title)
    
    # Extract content of each article from the law's body
    articles_content = get_articles_content(doc_file, body_article_one, sub_doc_ending, article_headings)

    # Extract referenced laws: laws between toc_title and article_one
    law_name = sub_docs[heading_indices[m][0]]['subdoc_name'] # Got revise the data structures to understand.
    referenced_laws = get_referenced_laws(doc_file, current_body_title, body_article_one, law_name)
    
    msg = "Number of articles in TOC NOT the same as found in law content prior to line " + str(sub_doc_ending) 
    assert len(article_headings) == len(articles_content), msg
    
    # Once we found everything we need, just store it.
    sub_files[m] = []
    law_name = sub_docs[heading_indices[m][0]]['subdoc_name']
    sub_files[m].append(law_name) 	# index 0
    sub_files[m].append(article_headings) # index 1
    sub_files[m].append(articles_content) # index 2
    sub_files[m].append(referenced_laws) # index 3
  # return classified sub_files
  return sub_files, pub_name, pub_date 
 

def sort_pairs(key, dictionary):
  # Take unsorted dictionary and return list sorted by pairs. (Nested dictionary)  

  unsorted_pairs = {int(dictionary[doc_id][key]): doc_id for doc_id in dictionary}
  sorted_keys = sorted(unsorted_pairs.keys())
  sorted_pairs = [(unsorted_pairs[index], index) for index in sorted_keys]
  return sorted_pairs

# remove excess whitespaces
def remove_spaces(string):
  if string:
    return ' '.join(string.split())
  return string
 
def remove_colon_if_any(string):
  """Remove colon ':' at the end or the beginning or in the middle"""
  if string:
    if string[-1] == ':': return string[:-1], True
    if string[0] == ':': return string[1:], False
    # [:-1] is used to remove colon in returned string. 
    if ':' in string: return split_at_char(string, [':'])[:-1], True
  return string, False 

def is_digits_colon(string):
  """Checks whether there is ONLY digits before the colon"""  
  for char in string:
    if not char.isdigit():   # char is not a digit
      if char == ':':
        return True      # digits followed by ':'
      return False     # digits NOT followed by ':'
  return False    # No 'colon' in the entire string


def line_exists(self, doc_file, line_i):
    # check if line exits in a list
    if len(doc_file) >= line_i + 1: return True
    return false


def get_next_token(doc_file, line_i, token_i):
  # FUnction has a bug. Consider using "line_exists() func" above
  """Get the next token in the doc_file (list)
  line_i -- current line index
  token_i -- current token index
  """
  if len(doc_file[line_i].split()) > token_i + 1:
    return doc_file[line_i].split()[token_i + 1], line_i, token_i + 1

  else:
    if len(doc_file) > line_i + 1:
      if len(doc_file[line_i + 1].split()) > 0:
        return doc_file[line_i + 1].split()[0], line_i + 1, 0
      else:
        # if the next line is empty, we run the function recursively. 
        return get_next_token(doc_file, line_i + 1, 0)
    # if we have reached the last token of the document.
    # THE RIGHT SIDE OF THE "AND" OPERATOR HAS A BUG. 
    # MAY BE TO THE ZERO in the recursive call.
    if len(doc_file) == line_i + 1 and len(doc_file[line_i].split()) == token_i + 1:
      return 

def get_referenced_laws(doc_file, body_title, body_article_one, law_name):
  """ This functions returns the text between the BODY Title and the BODY Article One

   body_title - Article of the 'law' that is after the Table of Contents (or in the body)
   body_article_one - First article in the body of the 'law'
   law_name - Name of the law as introduced in the body of the 'law'"""

  # position of last token of heading
  heading_ending = get_heading_ending(doc_file, body_title, law_name, 'Title') 
  # position of first token of references
  token, line_i, token_i = get_next_token(doc_file, heading_ending[0], heading_ending[1])

  return line_i, token_i, body_article_one - 1, len(doc_file[body_article_one -1])

def is_article_heading(doc_file, line_i, token_i = 0):
  """Given a token (and its location), say whether or not it starts a new article heading 
  line_i -- index of the current line number 
  token_i -- index of the current token in the line 

  outputs True, art-number, positions of '#:' or ':' if heading was found """
  art_number, end_w_colon = 0, False
  line_tokens = doc_file[line_i].split()
 
  # making sure line is not empty (made of whitespaces only)
  if len(line_tokens) > token_i and line_tokens[token_i] == 'article':
    next_token, line_i, token_i = get_next_token(doc_file, line_i, token_i) # eval right side 1st
    art_number, end_w_colon = remove_colon_if_any(next_token)
    # if the token is a digit and ends with a colon
    if art_number.isdigit() and end_w_colon:
      return True, int(art_number), line_i, token_i

    # if the token is a digit but doesn't end with a colon, check next token
    next_next_token, line_i, token_i = get_next_token(doc_file, line_i, token_i)

    if art_number.isdigit() and not end_w_colon and is_digits_colon(next_next_token):
      return  True, int(art_number), line_i, token_i
    else:
      return False, 0, line_i, token_i
  else:
    return False, 0, line_i, token_i

def get_article_headings(doc_file, first_head_art, last_head_art):
  """Returns headings/titles of all articles in the Table of Contents of a law.
  
  first_head_art -- index of the first article in the Table of Contents.
  last_head_art -- index of the last article ('commencement') in the TOC.
  """
  first_art_no = ['one', '1', 'one:', '1:']
  article_headings = {}
 
  def get_headings():
    """Returns dictionary of all article headings except the last one

       This nested function is EXTREMELY LONG. It needs to be shortened."""

    nonlocal article_headings
    prev_article = 0 # number of the previous article
    article_name = [] 	# Temp storage for name
    len_name = 0        # Number of token (length) of article-name
    is_higher_heading, higher_headings = False, ['title', 'chapter', 'part', 'section', 'o.g.']
    append_name = False   # if True, add token to article's name    
    line_i, token_i = len(doc_file), 1000000 #assuming that 10e6 is longer than any line  
    next_line_start, next_token_start = None, None # To save the start of article's heading
    roman_numerals = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']
  
    for n in range(first_head_art, last_head_art + 1):
      doc_line = doc_file[n].split()
      # As often, the order of the if statements below is very crucial.
      for g in range(len(doc_line)):
        token = doc_line[g]
        # Do not add chapter headings to articles' name
        if token in higher_headings:
          if token != 'part':
            is_higher_heading = True
          else:
            next_token, _ = remove_colon_if_any(get_next_token(doc_file, n, g)[0])
      
            if next_token in roman_numerals:
              is_higher_heading = True
            else:
             is_higher_heading = False        

        if append_name and not is_higher_heading:
          article_name.append(doc_line[g])

        new_article, article_number, line_i, token_i = is_article_heading(doc_file, n, g)
        if new_article:
          is_higher_heading = False # Because we know an article heading is starting
          if article_name: # for the first iteration (article 1), article_name is empty. 
            article_name = article_name[:len_name -1] if article_name[-1] == 'article' else article_name
            article_name = remove_colon_if_any(' '.join(article_name))[0]
            article_headings[int(prev_article)] = remove_spaces(article_name)
        
            # if this article was commencement, return article number (end)
            if get_next_token(doc_file, line_i, token_i)[0] == 'commencement': 
              return article_number 
            # otherwise initialize the variables
            article_name = []
          
          # the assignment below is crucial. The above one changes every iteration.
          next_line_start, next_token_start = line_i, token_i
          append_name = False # don't want to add article number and ':' stuff
          
          msg = "Skipped an article that follows article {0} at line {1}".format(prev_article, n)
          assert int(article_number)-int(prev_article) == 1, msg
          prev_article = article_number # number of current article. Its name is being appended.

        if n == next_line_start and g == next_token_start:
          append_name = True   
    
    return # Placeholder i.e. should NOT be used/needed 
    
  # the function below returns the number of the last article, BUT without adding it.
  # Add the last article 'commencement'
  last_article_number = get_headings() # Will append other articles while evaluating
  article_headings[int(last_article_number)] = 'commencement'
 
  assert len(article_headings) == int(last_article_number), 'Could NOT find all articles \
  in TOC starting at line ' + str(first_head_art)
  
  return article_headings

def next_art_heading(doc_file, line_initial, token_i, number_articles, sub_doc_ending):
    """This functions iterates through the article's content to find next heading"""
    is_heading, line_i = False, line_initial
    
    while is_heading != True and line_i <= sub_doc_ending:
      # the underscore below is intentional.
      is_heading, article_num, line_i, _ = is_article_heading(doc_file, line_i, token_i)

      if not is_heading:
        line_i, token_i = line_i + 1, 0

    if article_num < number_articles:
      assert is_heading, "Could not find next article heading at index " + str(line_i)

      return article_num, line_i, token_i
    elif article_num == number_articles:
      return article_num, line_i, token_i   # fucking bug
    else:
      assert False, "Should NOT evaluate to this point! (After last article) > Index: " + str(line_i)

def get_heading_ending(doc_file, start_index, heading, heading_type, prev_heading = 0):
  # get the coordinates where the headings ends. Start_index is where it starts.

  token, line_i, token_i = None, start_index, 0
  heading = heading.lower()
  if type(heading) != list: heading = heading.split()
  last_token = heading[-1]

  token_attempts = 0
  while token != last_token:  # we finish when we see the last token of the heading
    token, line_i, token_i = get_next_token(doc_file, line_i, token_i)
    token_attempts += 1
    msg = heading_type + " {}'s heading at index {} exceeds heading in TOC! (missing words)".format(prev_heading, line_i)
    # 3 is a margin error. That's a HUGE margin of error - 3 words difference.
    assert token_attempts <= len(heading) + 3, msg + "\n\nTOC Heading: "+ ' '.join(heading) + '\n'
 
  return line_i, token_i
 

def get_articles_content(doc_file, first_body_art, sub_doc_ending, article_headings):
  """Extracts the content of each article individually and returns 
     the dictionary containing all articles for a given law (sub-document)

     first_body_art -- index where 'article one' starts
     sub_doc_ending -- index where the last article ends
     article_headings -- dictionary of article numbers (integers) and their headings (strings)
     """
  all_articles_content = {}	# where all the content will be put
  # Get the "location" of the next token after "article". Ignoring 1st returned value.
  searched_art_num, line_i, token_i = is_article_heading(doc_file, first_body_art, 0)[1:] 
  actual_art_num = sorted(article_headings.keys())[0] # first article number ...
  number_articles = len(article_headings)

  while line_i <= sub_doc_ending and searched_art_num <= number_articles:
    token = None
    token_attempts = 0

    # Get_heading_end() gets where the article's heading ends.
    heading = article_headings[searched_art_num]
    line_i, token_i = get_heading_ending(doc_file, line_i, heading, 'article', searched_art_num)
    #get coordinates of the next token after article's heading
    token, line_i, token_i = get_next_token(doc_file, line_i, token_i)
    # Find where the NEXT article heading STARTS
    next_line_i, next_token_i = line_i, token_i # we are stuck with token_i because of str_between()
    next_art_num, next_line_i, next_token_i = next_art_heading(doc_file, next_line_i, \
                                              next_token_i, number_articles, sub_doc_ending)
    if next_art_num < number_articles:
      msg = "Skipped an article between {0} and {1} at line {2} ".format(searched_art_num, next_art_num, next_line_i)
      assert next_art_num == searched_art_num + 1, msg
    """
    Saving the content of the CURRENT article. '-1' because next_line_i is one index (at least) ahead

    article_content = str_between(doc_file, line_i, token_i, next_line_i - 1, len(doc_file[next_line_i -1].split()))

    instead of saving the content as shown above, we will save the arguments of str_between()
    and use them later."""
    content_coordinates = (line_i, token_i, next_line_i - 1, len(doc_file[next_line_i -1].split()))
    all_articles_content[int(searched_art_num)] = content_coordinates

    # Saving the last article. Notice that sub_doc_ending is used instead of next_line_i
    if next_art_num == number_articles: # + 1 to account for last's article heading: commenc. Hard-coding.
      all_articles_content[int(number_articles)] = (next_line_i + 1, token_i, sub_doc_ending, next_token_i)
      break
    # Initializing parameters
    searched_art_num = next_art_num
    line_i, token_i = next_line_i, next_token_i
  
  """
  for ar in all_articles_content:
    print("Article " + str(ar) + ':', article_headings[ar])
    print(all_articles_content[ar])
  """
  return all_articles_content
 
def get_law_type(law_name):
  # Identify the type of law from its name
  
  law_types = {'law': 'Law', 'prime':'Ministerial Order', 'ministerial':'Ministerial Order', \
               'presidential':'Presidential Order', 'Regulation':'Regulations',
               'Regulations':'Regulations', 'commissioner':'Commissioner General Rules',
               'practice':'Practices', 'practices':'Practices'}
  
  law_name = law_name.split()
  if law_name[0] in law_types: return law_types[law_name[0]]
  assert False,  "COULD NOT FIND LAW TYPE {0} !!!***".format(law_name)
 
def make_sub_files(df_case_sensitive, final_sorting):
  """Uses information (pub-name, pub-date, law-names) and indices in sub_file to 
     write new files. Find image illustration of the output format in the pwd"""
  sub_files, pub_name, pub_date = final_sorting
  pub_name = ' '.join(pub_name.split('\n'))

  for _file in sub_files:
    law_name = ' '.join(sub_files[_file][0].split('\n')) # turn name into one line
    law_type = get_law_type(law_name.lower())
    len_type = len(law_type.split())
    law_name_no_type = ' '.join(law_name.split()[len_type:]) # Starting with law No. Order matters.
    filename = '_'.join(law_name.split()[:len_type + 4]) # four for len(['NO', 'law#', 'of', 'lawDate']
    filename = filename.split('/')
    filename = '-'.join(filename)   

    # remove special symbols in filename. Otherwise things get complicated later on.
    final_filename = ''
    for char in filename:
      if char in ["°", "‟"]: char = "-"
      final_filename += char 
       
    final_filename = "ctructured_files/" + final_filename
    f = open(final_filename, 'w')
    f.write("### " + '\n')	# 1st line is empty for comments.
    f.write(law_type + '\n')    # type of the legal document
    f.write(law_name_no_type + '\n')	   # name of the law. Starting with law number. 
    f.write(pub_name + '\n')     # name of the official gazette
    f.write("Agency" + '\n')     # Agency name
    f.write("### " + '\n')  # any line for comments
    
    article_headings, articles_content, ref_laws_index= sub_files[_file][1], sub_files[_file][2], sub_files[_file][3]
    for article in article_headings:
      l_i, t_i, l_ii, t_ii = articles_content[article]  # arguments for line and token indices
      content = str_between(df_case_sensitive, l_i, t_i, l_ii, t_ii)
      f.write("Article " + str(article) + ' ' + article_headings[article] + '\n')
      f.write(content + '\n')
    f.close() # closing the file

    # Save referenced laws in a different text file
    ll_i, tt_i, ll_ii, tt_ii = ref_laws_index
    referenced_laws = str_between(df_case_sensitive, ll_i, tt_i, ll_ii, tt_ii)
    
    ff = open(final_filename+"_referencedLaws", 'w')
    ff.write("###" + '\n')   # 1st line is blank for comments
    ff.write(law_type + '\n')   # law type
    ff.write(law_name_no_type + '\n')  # law name without type (also starting with law #)
    ff.write(referenced_laws)
    ff.close() # closing the reference file
    
  return 



# run the whole program
def main():
  path = "devfiles_prepro/Official_Gazette_no_50_bis_of_14.12.2009.txt"
  path2 = "devfiles_prepro/Official_Gazette_no_19_of_11.05.2009.txt"  
  docs = get_subdocs_indices(path)
  find_skips(docs[1:4])
  final_sorting = classify_sub_files(docs[0], docs[1:-1])
  #make_sub_files(docs[-1], final_sorting)
 
main()
