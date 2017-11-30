# class to standardize laws' names

class FixLawName:

  LAW_NO = ['no','n°','nº']
  NO_SYMBOLS = ['°','º']
  STD_NO = '°'

  def __init__(self, raw):
    self.raw = raw

  def copy_list(self):
    # get copy of the file as a lowercase list (of lists)
    self.copy_list = []

    for line in self.raw.split('\n'):
      line = line.lower().split()
      self.copy_list.append(line)
    
    return self.copy_list

  def original_list(self):
    # get original as list (still in case sensitive)
    self.original_list = []

    for line in self.raw.split('\n'):
      line = line.split()
      self.original_list.append(line)
   
    return self.original_list
  
  def line_exists(self, doc_file, line_i):
    # check if line exits in a list
    if len(doc_file) >= line_i + 1: return True
    return false
 
  def get_next_token(self, doc_file, line_i, token_i):
    """
    Get the next token in the doc_file (list)
    line_i -- current line index
    token_i -- current token index
    """
    doc_file = [' '.join(line) for line in doc_file]
    
    # check if next line in file exits. Not elegant implementation
    if not self.line_exists(doc_file, line_i):
      return "$$$END$$$", 0, 0 # indicating end of file.
    
    if len(doc_file[line_i].split()) > token_i + 1:
      return doc_file[line_i].split()[token_i + 1], line_i, token_i + 1
    
    else:
      if len(doc_file) > line_i + 1:
        if len(doc_file[line_i + 1].split()) > 0:
          return doc_file[line_i + 1].split()[0], line_i + 1, 0
        else:
          # if the next line is empty, we run the function recursively. 
          return self.get_next_token(doc_file, line_i + 1, 0)

      # if we have reached the last token of the document. 
      # There is a bug on the right side of the AND operator (because of Zero in recursive call).
      else:
        return "$$$END$$$", 0, 0

  def is_law_name(self, copy, i, j):
    """
    Check if the current token starts a law name
    HOW: see if token is in LAW_NO and followed
    by <num> "of" <date> in that order

    WORKING ASSUMPTION: ONLY TWO tokens are attached, AT MOST
    """
   
    is_name = False
    has_no, has_num, has_of, has_date = False, False, False, False

    token = copy[i][j]

    """Token is >= 2 and in LAW_NO"""
    if len(token) >= 2 and token[:2] in self.LAW_NO:
      has_no = True
      
      next_token, next_i, next_j = self.get_next_token(copy, i, j)
     
      """Token has a digit at the end - no whitespace"""
      if len(token) > 2 and token[2].isdigit():
        has_num = True
        # if there is no space, next_token should be 'of'
        if next_token == 'of':
          has_of = True
         
      """len = 2, i.e. len("nº"), then next_token is law_num"""
      if len(token) == 2 and next_token[0].isdigit():
        has_num = True
      
        """See if token ends with 'of' - no whitespace"""
        if not next_token[-1].isdigit():
          if len(next_token) > 3 and next_token[-2:] == 'of':
            has_of = True
      
      """Get next token - see if it stars with 'of' """
      next_token, next_i, next_j = self.get_next_token(copy, next_i, next_j)
    
      if next_token:
        if len(next_token) >= 2 and next_token[:2] == 'of':
          has_of = True

        """ if there was no space between no-num or num-of
        this next_token is the date"""
        if next_token[0].isdigit():
          has_date = True
        
        """see if 'of' is followed by a digit - date"""
        if len(next_token) > 2 and next_token[2].isdigit():
          has_date = True
          
      """Get next token - see if starts with a digit - date"""
      next_token, next_i, next_j = self.get_next_token(copy, next_i, next_j)

      if next_token and next_token[0].isdigit():
        has_date = True
      
    if has_no and has_num and has_of and has_date:
      return True

    return False
        
  def make_raw_file(self, nested_lists):
    # Take a nested list, and return a string
    # Just like a raw file after open()
    
    raw_file = ""
    len_file = len(nested_lists)

    for n in range(len_file):
      if n < len_file - 1:
        line = ' '.join(nested_lists[n]) + '\n'
      else:
        line = ' '.join(nested_lists[n])
      
      raw_file += line

    return raw_file 
    
 
  def fix_name(self):
    # locate law names and standardize them
    
    self.copy, self.original = self.copy_list(), self.original_list()
    """
    going through each line (lower case)
    Then go through each token in the line
    check if that token is part of law's name
    Then check if the format is correct
    that is: <Law> n° <num> of <date>"""

    for i in range(len(self.copy)):
      for j in range(len(self.copy[i])):
        if self.is_law_name(self.copy, i, j):
          
          did_no = False        

          token = self.copy[i][j]
          """Token is >= 2 and in LAW_NO"""
          if len(token) >= 2 and token[:2] in self.LAW_NO:
            
            """Token has a digit - law_num - at the end - no whitespace"""
            if len(token) > 2 and token[2].isdigit():
            
              # BIG IDEA: Add two tokens together with space in between
              self.original[i][j] = self.original[i][j][:1] + self.STD_NO + ' '+token[2:]
              did_no = True

            if not did_no:
              self.original[i][j] = self.original[i][j][:1] + self.STD_NO

            """Get next token. See if it starts with a digit - law_num"""
            next_token, next_i, next_j = self.get_next_token(self.copy, i, j)
            if len(token) == 2 and next_token[0].isdigit():

              """See if token ends with 'of' - no whitespace"""
              if not next_token[-1].isdigit():
                if len(next_token) > 3 and next_token[-2:] == 'of':
                  self.original[next_i][next_j] = self.original[next_i][next_j][:-2]+' '+\
                                                  self.original[next_i][next_j][-2:]
                  

            """Get next token - see if it stars with 'of' """
            next_token, next_i, next_j = self.get_next_token(self.copy, next_i, next_j)
            if len(next_token) >= 2:
              if next_token[:2] == 'of':
               
                """see if 'of' is followed by a digit - date"""
                if len(next_token) > 2 and next_token[2].isdigit():
                  self.original[next_i][next_j] = self.original[next_i][next_j][:2]+' '+\
                                                  self.original[next_i][next_j][2:]            
    
            """Get next token - see if starts with a digit - date"""
            next_token, next_i, next_j = self.get_next_token(self.copy, next_i, next_j)
            if next_token and next_token[0].isdigit():
              """If token does not end with a digit - separate"""
              if not next_token[-1].isdigit():
                n = 0
                for char in next_token:
                  if char.isalpha():
                    self.original[next_i][next_j] = self.original[next_i][next_j][:n]+' '+\
                                                  self.original[next_i][next_j][n:] 
                  n += 1 # n-1 is the index of the last digit
            
                             
    return self.make_raw_file(self.original)   
