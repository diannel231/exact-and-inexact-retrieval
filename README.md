#pending readme so nothing gets deleted accidentallyl
# exact-and-inexact-retrieval

## buildDocIdList()

## buildIndexOptimized()
Implemented in two parts because direct converson to inverted indes was having issues
First creates token dictionary and builds a dictionary of docID value as key and token dictionary as value
Iterates through that list and add them to an inverted index to create the working list

## buildIndex()


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
