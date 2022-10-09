# Python 2.7.3
import re
import os
import collections
import time


class index:
    def __init__(self, path):
        self.path = path
        pass

    docIdDictionary = {}
    inverted_index = {}
    inv_index = {}
    def buildDocIdList(self, doc_files):
        for idx, each_file in enumerate(doc_files):
            #print(idx, each_file)
            self.docIdDictionary[each_file] = idx
        return self.docIdDictionary

    def buildIndexOptimized(self):
        start_time = time.time()
        doc_files = [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]
        docIdDictionary = self.buildDocIdList(doc_files)
        # Tokenization
        for each_file in doc_files:
            with open(self.path + "/" + each_file) as file:
                text = file.read().replace('\n',' ')
            text_array = re.sub('[^a-zA-Z \n]', '', text).lower().split()
            for idx, token in enumerate(text_array):
                if token not in self.inverted_index.keys():
                    self.inverted_index[token] = {}
                docId = docIdDictionary[each_file]
                if docId not in self.inverted_index[token].keys():
                    self.inverted_index[token][docId] = []
                self.inverted_index[token][docId].append(idx)

        print("Index built in " + str(time.time() - start_time) + " seconds")
#        print(self.inverted_index)

    def buildIndex(self):
        start_time = time.time()
        doc_files = [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]
        docIdDictionary = self.buildDocIdList(doc_files)

        #build top down index first with dicId as key
        index = {}
        for each_file in doc_files:
            # Tokenization
            with open(self.path + "/" + each_file) as file:
                text = file.read().replace('\n',' ')
            text_array = re.sub('[^a-zA-Z \n]', '', text).lower().split()
            token_dictionary = {}
            for idx, token in enumerate(text_array):
                if token not in token_dictionary.keys():
                    token_dictionary[token] = [idx]
                else:
                    token_dictionary[token].append(idx)
            index[docIdDictionary[each_file]] = token_dictionary
        #print(index[0])

        #build inverted index
        for key, value in index.items():
            doc_id = key
            position_word_index = value
            for word, position in position_word_index.items():
                if word not in self.inverted_index:
                    self.inverted_index[word] = []
                self.inverted_index[word].append({doc_id: position})

        #sort the posting list
        for key, value in index.items():
            self.inverted_index[key] = collections.OrderedDict(sorted(value.items()))

        print("Index built in " + str(time.time() - start_time) + " seconds")
        #print(self.inverted_index)

# function for identifying relevant docs using the index
    def and_query(self, query_terms):
        start_time = time.time()
        if len(query_terms) == 0:
            print("Enter at least one search query!")
            return
        if len(query_terms) == 1:
            return self.getPostingListForTerm(query_terms[0])

        #more than one search term entered, do AND by intersection
        result = self.getPostingListForTerm(query_terms[0])
        for term in query_terms[1:]:
            result = self.intersect(result, self.getPostingListForTerm(term))
        self.post_process_results(result, query_terms, False)

        print("Retrieved in " + str(time.time() - start_time) + " seconds")

        return result

    def intersect(self, p1, p2):
        result = []
        i = 0
        j = 0
        while i < len(p1) and j < len(p2):
            if p1[i] == p2[j]:
                result.append(p1[i])
                i = i + 1
                j = j + 1
            elif p1[i] < p2[j]:
                i = i + 1
            else:
                j = j + 1
        return result

# function to process result from AND operation. we get bunch of docIds.
    def post_process_results(self, result, terms, print_positions):
        if len(result) == 0:
            print('No results found!')
            return
        print('Total docs retrieved: ' + str(len(result)))
        fileNames = list(self.docIdDictionary.keys())
        docIds = list(self.docIdDictionary.values())
        for docId in result:
            fileName = fileNames[docIds.index(docId)]
            print(fileName)
            if print_positions == True:
                for term in terms:
                    docIdsAndPositions = self.inverted_index[term]
                    for docIdPosDict in docIdsAndPositions:
                        docIdInKey = list(docIdPosDict.keys())[0]
                        if docIdInKey == docId:
                            positions = docIdPosDict[docIdInKey]
                            print('Term: "'+term+'" found in file "'+fileName+'" at positions: '+str(positions))

    def exact_query(self, query_terms, k):
	#function for exact top K retrieval (method 1)
	#Returns at the minimum the document names of the top K documents ordered in decreasing order of similarity score

    def inexact_query_champion(self, query_terms, k):
	#function for exact top K retrieval using champion list (method 2)
	#Returns at the minimum the document names of the top K documents ordered in decreasing order of similarity score

    def inexact_query_index_elimination(self, query_terms, k):
	#function for exact top K retrieval using index elimination (method 3)
	#Returns at the minimum the document names of the top K documents ordered in decreasing order of similarity score

    def inexact_query_cluster_pruning(self, query_terms, k):
	#function for exact top K retrieval using cluster pruning (method 4)
	#Returns at the minimum the document names of the top K documents ordered in decreasing order of similarity score

# function to print the terms and posting list in the index
    def print_dict(self):
        for word, posting_list in self.inverted_index.items():
            print(word, posting_list)

# function to print the documents and their document id
    def print_doc_list(self):
        for file, idx in self.docIdDictionary.items():
            print('Doc ID: ' + str(idx) + ' ==> ' + file)

# function to get just the docIds for the term
    def getPostingListForTerm(self, term):
        if term in self.inverted_index:
            posting_list = self.inverted_index[term] #{'woord' : {0: [0, 46], 54: [842], 59: [608]}}
            return list(posting_list.keys())
        return []


a = index("./collection")
a.buildIndexOptimized()


query1 = ['with', 'without', 'yemen']
print("Querying dictionary with key words: " + str(query1))
a.and_query(query1)
"""
print("------------------------------------------------------------------------------------------------------------")
query2 = ['americans', 'europe']
print("Querying dictionary with key words: " + str(query2))
a.and_query(query2)
print("------------------------------------------------------------------------------------------------------------")
query3 = ['greatest', 'country', 'asian']
print("Querying dictionary with key words: " + str(query3))
a.and_query(query3)
print("------------------------------------------------------------------------------------------------------------")
query4 = ['thousands', 'more', 'citizens']
print("Querying dictionary with key words: " + str(query4))
a.and_query(query4)
print("------------------------------------------------------------------------------------------------------------")
query5 = ['socialist', 'administration', 'industry']
print("Querying dictionary with key words: " + str(query5))
a.and_query(query5)
"""


#print(a.getPostingListForTerm('jordan'))
#a.print_dict()
#a.print_doc_list()
