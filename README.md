# exact-and-inexact-retrieval

## How to execute code
  - Download anaconda
  - run conda install -c anaconda spyder 
  - open spyder
  - Copy the index.py, stoplist.txt, and collections files into spyder
  - Hit the run button in Spyder

## buildDocIdList()
Returns the Id dictionary

## buildIndex()
The primary function for constructing the inverted index using the list of documents. It first tokenizes the documents then converts to the inverted index form.

## build_idf_dict()
Creates the term frequenxy-inverse document frequency list

## build_upgraded_inverted_index_to_contain_tfidf()
Uses both the invesrted index list and tfidf list to creade a weighted inverted index that contains the tfidf information for the champions lst.

## sort_docId_weighted_posIndex_tuples()
Takes in a list of tuples as a query and returns a list of the most relevant tuples in the list for inexact search methods

## build_tf_dict()
Takes in a list of words in a document as a query and returns a list with information on how frequent each term in the list is compared to every other term as a percentage

## term_frequency_normalization_for_docIds(self)
Normalizes the documents term frequency by taking the square root of the frequencies log + 1 squared

## calc_cosine_similarity()
returns the cosine similarty by comparing the term frequency lists to see how much terms have similar frequency within their respective documents

## exact_query()
Takes the exact query, sorts the resulting list based on relevance and takes input on how many results are wanted and post processes the results

## inexact_query_champion()
Takes the top single query word documents for each query term and only does the cosine similarity to calculate the score for those top documents

## inexact_query_index_elimination()
Does an inexact query by taking the most relevant k queries according to the weighted tf-idf dictionary and processes those results

## inexact_query_cluster_pruning(self, query, K)
Uses cosine simlarity, a leader and follower status is assigned to each document and then, rather than search every document while querying, the leader is queried and if the results do not appear to be very relevant then the followers of the branch are also ignored

## build_leaders_and_followers()
Randomly assigns a number of documents as leaders according to the square root of the total number of documents. The document list is then processed , ignoring the leader documents, to calculate the similarity between remaining documents and assign each document as a follower to the most relevant leader.

### get_cosine(self, vec1, vec2)
Calculates the cosine of two documents for later use in the inexact retrieval methods

### text_to_vector(self, text)
returns the list of words as a vector

### post_process_exact_inexact_results()
Does the post processing of the results from each search to display relevant information like the number of documents searched and the search results

### sort_term_idf_tuples()
Takes in a list of tuples as a query and returns the list of tuples relevant to the inverted document frequency

### sort_cosine_leaders()

### get_tf_for_term()
Returns the term frequency for a specific term in a specific document

### get_idf_for_term()
Gets the term idf for cosing scoring

### print_dict()
prints the terms and posting list in the index

### print_doc_list()
prints the documents and their document id

### get_file_name_from_docIdDict()
gets the file name from the document Id dictionary

### get_file_text()
returns the text of a document by inputting a file name

### join_txt_array_to_string()
returns text with an inputted array appended to the end

### filter_words_with_stoplist()
filters the most common words out of the text so that the effect of the low impact words are lower

### filter_query_text_return_text()
filters the most common words out of the query so that the effect of the low impact words are lower

### getPostingListForTerm(self, term)
returns the list of document ids without positions
