# Python 2.7.3
import re
import os
import time
import math
import random
from collections import Counter
WORD = re.compile(r"\w+")

class index:
    stop_list = []
    def read_stop_list(self):
        with open(self.path + "/../stop-list.txt") as file:
            return file.read().split('\n') #read stop list file, split on new line char
            
            
    def __init__(self, path):
        self.path = path
        self.stop_list = self.read_stop_list()
        pass
    
    docIdDictionary = {}
    inverted_index = {}
    inv_index = {}
    tf_dict = {}
    idf_dict = {}
    tfidf_weighted_dictionary = {}
    normalized_tf_lengths = {}
    champion_list = {}
    group = {}
    def buildDocIdList(self, doc_files):
        for idx, each_file in enumerate(doc_files):
            #print(idx, each_file)
            self.docIdDictionary[each_file] = idx
        return self.docIdDictionary
        
    def buildIndex(self):
        start_time = time.time()
        doc_files = [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]
        docIdDictionary = self.buildDocIdList(doc_files)
        # Tokenization
        for each_file in doc_files:
            with open(self.path + "/" + each_file) as file:
                text = file.read() #we have the text of the document
            text_array = self.filter_words_with_stoplist(text) #filter out stop list words
            docId = docIdDictionary[each_file]
            self.tf_dict[docId] = self.build_tf_dict(text_array) #store tf values for each term on per document basis
            for idx, token in enumerate(text_array):
                if token not in self.inverted_index.keys():
                    self.inverted_index[token] = {}
                if docId not in self.inverted_index[token].keys():
                    self.inverted_index[token][docId] = []
                self.inverted_index[token][docId].append(idx)
        
        #build tf-idf weighted index
        self.build_idf_dict()
        #print("self.idf_dict", self.idf_dict)
        self.build_upgraded_inverted_index_to_contain_tfidf()
        print("Index built in " + str(time.time() - start_time) + " seconds")
        self.term_frequency_normalization_for_docIds()
        #print("self.normalized_tf_lengths", self.normalized_tf_lengths)
        
        self.build_leaders_and_followers()
#        print(self.inverted_index)
    
    def build_idf_dict(self):
        num_of_documents = len(self.docIdDictionary)
        for token, posting_list in self.inverted_index.items():
            #print(" token:", token, "| num_of_docs:", list(posting_list.keys()))
            self.idf_dict[token] = 1 + (math.log(num_of_documents / float(len(list(posting_list.keys())))))
    
    #    Term ID: [〖idf〗_t,(ID1,w_(t_1,d_1 ), [pos1,pos2,..]), (ID2, w_(t_2,d_2 ), [pos1,pos2,…]),….]
    #   { term : [ idf, (docId1, tf, [pos1,pos2]), (docId2, tf, [pos1,pos2]) ]
    def build_upgraded_inverted_index_to_contain_tfidf(self):
        tfidf_dict = {}
        for token, posting_list in self.inverted_index.items():
            tfidf_dict[token] = [self.idf_dict[token]]
            for docId in posting_list.keys(): #keys are document ids, values are positional indexes array
                tf = self.tf_dict[docId][token]
                if tf > 0:
                    weighted_tf = 1 + math.log(tf)
                else:
                    weighted_tf = 0
                positions = posting_list[docId]
                tfidf_dict[token].append((docId, weighted_tf, positions))
            list_of_tuples_to_sort_for_champion_list = tfidf_dict[token][1:]
            sorted_list = self.sort_docId_weighted_posIndex_tuples(list_of_tuples_to_sort_for_champion_list);
            if len(sorted_list) <= 3:
                r = len(sorted_list)
            else:    
                r = len(sorted_list) // 2 #half the sorted list for champions
            #print("sorted_list", sorted_list, "R", r)
            #print("sorted_list.reverse()", sorted_list.reverse())
            self.champion_list[token] = sorted_list[:r]
            #PUT THIS SORTED LIST BACK WJERE IT BELONGS!
            tfidf_dict[token] = [self.idf_dict[token]]
            for t in sorted_list:
                tfidf_dict[token].append(t)
            #now we have sorted docids with weighted tf's..now we can take top R for chamption list.
            
        self.tfidf_weighted_dictionary = tfidf_dict
    
        
    def sort_docId_weighted_posIndex_tuples(self, tup):
        lst = len(tup)
        for i in range(0, lst):
            for j in range(0, lst-i-1):
                if (tup[j][1] > tup[j + 1][1]):
                    temp = tup[j]
                    tup[j]= tup[j + 1]
                    tup[j + 1]= temp
        tup.reverse()
        return tup
    
        
    def build_tf_dict(self, text_array):
        word_count = {}
        for word in text_array:
            if word in word_count.keys():
                word_count[word] += 1
            else:
                word_count[word] = 0
        total_num_of_words = len(text_array)
        for w, count in word_count.items():
            word_count[w] = count / total_num_of_words
        #print("tf_dict", word_count)
        return word_count #this is the tf_dict structure: { 'word1' : 12.345, 'word2' : 11.123}
    
    def get_tf_for_term(self, term, docId):
        if docId in self.tf_dict:
            if term in self.tf_dict[docId]:
                return self.tf_dict[docId][term]
            else:
                return 0.0
        else:
            return 0.0
        
    def get_idf_for_term(self, term):
        if term in self.idf_dict.keys():
            return self.idf_dict[term]
        else:
            return 0.0
    
    
    def term_frequency_normalization_for_docIds(self):
        vocab = self.tfidf_weighted_dictionary.keys()
        print("Vocabulary Size:", len(vocab))
        for docId in self.docIdDictionary.values():
            l = 0
            for term in vocab:
                #print("self.get_tf_for_term(term, docId)", self.get_tf_for_term(term, docId))
                tf =self.get_tf_for_term(term, docId)
                if tf > 0:
                    #print("TF for term", term, "in docid", docId, " is", tf)
                    l += math.pow(1+math.log(tf), 2)
            self.normalized_tf_lengths[docId] = math.sqrt(l)


    def calc_cosine_similarity(self, query, docId):
        if self.normalized_tf_lengths[docId] == 0:
            #print("normalized tf zero for doc ", self.get_file_name_from_docIdDict(docId))
            return 0
        sim_score = 0
        vocab = list(self.tfidf_weighted_dictionary.keys())
        for term in query:
            term = term.lower()
            if term in vocab:
                sim_score += (self.get_tf_for_term(term, docId) * self.get_idf_for_term(term))
        sim_score = sim_score / self.normalized_tf_lengths[docId]
        #if sim_score > 1:
        #    print("Sim score", sim_score, "normalized", self.normalized_tf_lengths[docId])
        return sim_score

    def get_cosine(self, vec1, vec2):
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])
    
        sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
        sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)
    
        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator
    
    
    def text_to_vector(self, text):
        words = WORD.findall(text)
        return Counter(words)
    
   
    def post_process_exact_inexact_results(self, result, terms, K):
        print("Searching for '",self.join_txt_array_to_string(terms),"'...")
        if len(result) == 0:
            print('No results found!')
            return
        print('Total docs searched: ' + str(len(result)))
        if len(result) > K:
            print("Taking top", K, "results")
            result = result[:K]
        fileNames = list(self.docIdDictionary.keys())
        docIds = list(self.docIdDictionary.values())
        for r in result:
            score = r[0]
            docId = r[1]
            fileName = fileNames[docIds.index(docId)]
            print("File:",fileName, "Score:", score)
        

    def exact_query(self, query, K):
        start_time = time.time()
        results = []
        query = self.filter_words_with_stoplist(query) #input text sentence, outputs array
        for fileName, docId in self.docIdDictionary.items():
            score = self.calc_cosine_similarity(query, docId)
            #print("score", score, "query", query, "docId", docId)
            results.append((score, docId))
            # sort according to score then pick top K
        results = self.sort_cosine_leaders(results)
        print("exact_query searched in " + str(time.time() - start_time) + " seconds")
        self.post_process_exact_inexact_results(results, query, K)

    def inexact_query_champion(self, query, K):
        query_terms = self.filter_words_with_stoplist(query) #input text sentence, outputs array
        start_time = time.time()
        results = []
        unique_docIds = set()
        #print("self.champion_list", self.champion_list);
        for term in query_terms:
            term = term.lower()
            docIds = map(lambda x: x[0], self.champion_list[term])
            for docId in docIds:
                unique_docIds.add(docId)
        unique_docIds = list(unique_docIds)
        for docId in unique_docIds:
            score = self.calc_cosine_similarity(query_terms, docId)
            results.append((score, docId))
        results = self.sort_cosine_leaders(results)
        print("inexact_query_champion searched in " + str(time.time() - start_time) + " seconds")
        self.post_process_exact_inexact_results(results, query_terms, K)
    
    def inexact_query_index_elimination(self, query, k):
        query_terms = self.filter_words_with_stoplist(query) #input text sentence, outputs array
        start_time = time.time()
        term_idf_tuples = []
        for term in query_terms:
            term = term.lower()
            idf = self.tfidf_weighted_dictionary[term][0]
            term_idf_tuples.append((idf, term))
        term_idf_tuples = self.sort_term_idf_tuples(term_idf_tuples)
        num_to_pic = len(term_idf_tuples) // 2
        top_query_terms = term_idf_tuples[:num_to_pic]
        only_query_terms = list(map(lambda x: x[1], top_query_terms))
        print("inexact_query_index_elimination searched in " + str(time.time() - start_time) + " seconds")
        return self.exact_query(self.join_txt_array_to_string(only_query_terms), k)
        
    def inexact_query_cluster_pruning(self, query, K):
        query_terms = self.filter_words_with_stoplist(query) #input text sentence, outputs array
        start_time = time.time()
        leader_cosine_queries = []
        single_str = self.join_txt_array_to_string(query_terms)
        single_str = single_str.lower()
        for leader, followers in self.group.items():
            if leader is None:
                continue
            #print("leader!!!", leader)
            #print("docIdDictionary!!!", self.docIdDictionary)
            leader_txt = self.get_file_text(self.get_file_name_from_docIdDict(leader))
            leader_txt_filtered_array = self.filter_words_with_stoplist(leader_txt)
            leader_txt = self.join_txt_array_to_string(leader_txt_filtered_array)
            leader_vec = self.text_to_vector(leader_txt)
            q_vec = self.text_to_vector(single_str)
            cos = self.get_cosine(leader_vec, q_vec)
            leader_cosine_queries.append((cos,leader))
        leader_cosine_queries = self.sort_cosine_leaders(leader_cosine_queries)
        results = []
        for l in leader_cosine_queries:
            leader_docId = l[1]
            followers_docIds = self.group[leader_docId]
            cloned_docIds = followers_docIds.copy()
            cloned_docIds.append(leader_docId)
            for docId in cloned_docIds:
                score = self.calc_cosine_similarity(query_terms, docId)
                if score <= 0:
                    continue
                #print("score", score, "query", query, "docId", docId)
                results.append((score, docId))
            if len(results) < K:
                continue
            else:
                break
        results = self.sort_cosine_leaders(results)
        print("inexact_query_cluster_pruning searched in " + str(time.time() - start_time) + " seconds")
        self.post_process_exact_inexact_results(results, query_terms, K)
        
            
    def build_leaders_and_followers(self):
        leaders = []
        docIds = list(self.docIdDictionary.values())
        for i in range(int(math.sqrt(len(docIds)))):
            leaders.append(random.randint(0,len(docIds)-1))
        for lead in leaders:
            self.group[lead] = []
        if len(self.group) == 0:
            for lead in leaders:
                self.group[lead] = []
            for doc in docIds: # Iterate over all non-leader documents
                if doc in leaders: # ignore leaders, we are dealing with followers here
                    continue
                my_lead = []
                for lead in leaders: # Iterate over all leaders
                    lead_txt = self.get_file_text(self.get_file_name_from_docIdDict(lead))
                    followr_text = self.get_file_text(self.get_file_name_from_docIdDict(doc))
                    lead_txt = self.join_txt_array_to_string(self.filter_words_with_stoplist(lead_txt))
                    followr_text = self.join_txt_array_to_string(self.filter_words_with_stoplist(followr_text))
                    vector1 = self.text_to_vector(lead_txt)
                    vector2 = self.text_to_vector(followr_text)
                    cosine = self.get_cosine(vector1, vector2)
                    my_lead.append((lead, cosine))
                my_lead = sorted(my_lead, key=lambda tup: -tup[1])
                num_nearest = math.sqrt(len(my_lead))
                followers = my_lead[:num_nearest]
                self.group[lead] = followers
                

    #function for exact top K retrieval using cluster pruning (method 4)
    #Returns at the minimum the document names of the top K documents ordered in decreasing order of similarity score

    def sort_term_idf_tuples(self, tup):
        lst = len(tup)
        for i in range(0, lst):
            for j in range(0, lst-i-1):
                if (tup[j][1] > tup[j + 1][1]):
                    temp = tup[j]
                    tup[j]= tup[j + 1]
                    tup[j + 1]= temp
        tup.reverse()
        return tup
    
    def sort_cosine_leaders(self, tup):
        lst = len(tup)
        for i in range(0, lst):
            for j in range(0, lst-i-1):
                if (tup[j][0] > tup[j + 1][0]):
                    temp = tup[j]
                    tup[j]= tup[j + 1]
                    tup[j + 1]= temp
        tup.reverse()
        return tup

# function to print the terms and posting list in the index
    def print_dict(self):
        for word, posting_list in self.inverted_index.items():
            print(word, posting_list)

# function to print the documents and their document id
    def print_doc_list(self):
        for file, idx in self.docIdDictionary.items():
            print('Doc ID: ' + str(idx) + ' ==> ' + file)
    
    def get_file_name_from_docIdDict(self, docId):
        for file, did in self.docIdDictionary.items():
            if did == docId:
                return file
    
    def get_file_text(self, fileName):
        with open(self.path + "/" + fileName) as file:
            text = file.read().replace('\n',' ')
            return text
    
    def join_txt_array_to_string(self, arr):
        return ' '.join(word for word in arr)
    
    def filter_words_with_stoplist(self, text):
        text = text.replace('\n',' ')
        words = re.sub('[^a-zA-Z \n]', '', text).lower().split()
        word_array_cleaned = []
        for word in words:
            if word not in self.stop_list:
                word_array_cleaned.append(word)
        return word_array_cleaned
        
    def filter_query_text_return_text(self, query_text):
        query_array_cleaned = self.filter_words_with_stoplist(query_text)
        return self.join_txt_array_to_string(query_array_cleaned)
    
# function to get just the docIds for the term
    def getPostingListForTerm(self, term):
        if term in self.inverted_index:    
            posting_list = self.inverted_index[term] #{'woord' : {0: [0, 46], 54: [842], 59: [608]}}
            return list(posting_list.keys())
        return []
            

a = index("./collection")
a.buildIndex()


q1 = "with without yemen"
q2 = "french nuclear weapons president kennedy KHRUSHCHEV KAZAKHSTAN"
q3 = "greatest country asian"
q4 = "thousands more citizens"
q5 = "americans europe"
queries = [q1, q2, q3, q4, q5]
for q in queries:
    a.exact_query(q, 5)
    print("------------------------------------------------------------------------------------------------------------")
    a.inexact_query_champion(q, 5)
    print("------------------------------------------------------------------------------------------------------------")
    a.inexact_query_index_elimination(q, 5)
    print("------------------------------------------------------------------------------------------------------------")
    a.inexact_query_cluster_pruning(q, 5)
    print("============================================================================================================")
#a.and_query(query1)
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
