#pending readme so nothing gets deleted accidentallyl
# exact-and-inexact-retrieval

## buildDocIdList()

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

## get_tf_for_term()
Returns the term frequency for a specific term in a specific document

## get_idf_for_term()
Gets the term idf for cosing scoring

## term_frequency_normalization_for_docIds(self)
Normalizes the documents term frequency by taking the square root of the frequencies log + 1 squared

## calc_cosine_similarity()
returns the cosine similarty by comparing the term frequency lists to see how much terms have similar frequency within their respective documents

## get_cosine(self, vec1, vec2)
Calculates the cosine of two documents for later use in the inexact retrieval methods

## text_to_vector(self, text)
returns the list of words as a vector

## post_process_exact_inexact_results()
Does the post processing of the results from each search to display relevant information like the number of documents searched and the search results

## exact_query()
Takes the exact qeury, sorts the resulting list based on relevance and takes input on how many results are wanted and post processes the results

## inexact_query_champion()







## inexact_query_index_elimination()
Does an inexact query by taking the most relevant k queries according to the weighted tf-idf dictionary and processes those results

## inexact_query_cluster_pruning(self, query, K)
Uses cosine simlarity, a leader and follower status is assigned to each document and then, rather than search every document while querying, the leader is queried and if the results do not appear to be very relevant then the followers of the branch are also ignored

## build_leaders_and_followers()
Randomly assigns a number of documents as leaders according to the square root of the total number of documents. The document list is then processed , ignoring the leader documents, to calculate the similarity between remaining documents and assign each document as a follower to the most relevant leader.

## sort_term_idf_tuples()
Takes in a list of tuples as a query and returns the list of tuples relevant to the inverted document frequency

## sort_cosine_leaders()

## print_dict()
prints the terms and posting list in the index

## print_doc_list()
prints the documents and their document id

## get_file_name_from_docIdDict()
gets the file name from the document Id dictionary

## get_file_text()
returns the text of a document by inputting a file name

## join_txt_array_to_string()
returns text with an inputted array appended to the end

## filter_words_with_stoplist()

## filter_query_text_return_text()

## getPostingListForTerm(self, term)
returns the list of document ids without positions


## and_query()
The and merge function first checks the edge cases where 0 query terms are used, giving a warning that a query term is needed, and 1 query term where the posting list is returned as normal for the single term. The function first grabs the posting list for the first query term and then loops through the rest of the query terms, finding the intersections in the posting list values and keeping the result. The total time is posted after the final result is formed.

## getPostingListForTerm()
Loops through the document list and add the docId to list 

## intersect()
Takes two posting lists and returns a list of values that are contained in both posting lists by incrementing through each value

## post_process_results()
Takes the resulting posting list and prints it with the option to include the positions of the search terms in each document

## exact_query()
function for exact top K retrieval (method 1)
Returns at the minimum the document names of the top K documents ordered in decreasing order of similarity score

## inexact_query_champion()
function for exact top K retrieval using champion list (method 2)
Returns at the minimum the document names of the top K documents ordered in decreasing order of similarity score

## inexact_query_index_elimination()
function for exact top K retrieval using index elimination (method 3)
Returns at the minimum the document names of the top K documents ordered in decreasing order of similarity score

## inexact_query_cluster_pruning()

## print_dict()
Iterate through the words and posting list in inverted index then print

## print_doc_list()
Iterate through docID dictionary and print index, which is the docId and file name that is stored as key of the dictionary
