# Organize laws and repeals in a list

law_repeals = [] # where the data will be stored

file_path = "repeals_mod.txt"

def get_repeals(filename):

  with open(filename, 'r') as f:
    raw_data = f.read().split('\n') # split by newline
    
    # put the data in the law_repeals list
    # each element is (<law_name>, <repeal_article>) 
    # where law_name and repeal_article are both strings
  
    for n in range(0, len(raw_data), 3):
      law_name = raw_data[n]
      repeal_article = raw_data[n+1]
     
      law_repeals.append((law_name, repeal_article))

  return law_repeals

    
get_repeals(file_path)
