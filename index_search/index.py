'''
blog: http://aakashjapi.com/fuckin-search-engines-how-do-they-work/
https://github.com/logicx24/Text-Search-Engin
'''

#input = [file1, file2, .....]
#output = {filename: [word1, word2]}

import re
import math
import nltk

stemmer = nltk.PorterStemmer()

class InvertedIndex:

    def __init__(self, files):
        self.tf = {}
        self.df = {}
        self.idf = {}
        self.filenames = files
        self.file_to_terms = self.process_files()
        self.regularIndex = self.regIndex()
        self.totalIndex = self.fullIndex()
        self.vectors = self.vectorize()
        self.magni = self.magnitudes(self.filenames)
        self.populateScores()


    def process_files(self):
        file_to_terms = {}
        stopwords = open('../my_corpus/stopwords.txt').read()
        for file in self.filenames:
            pattern = re.compile('[\W_]+')
            file_to_terms[file] = open(file, 'r').read().lower()
            file_to_terms[file] = pattern.sub(' ', file_to_terms[file])
            re.sub(r'[\W_]+', '', file_to_terms[file])
            file_to_terms[file] = file_to_terms[file].split()
            file_to_terms[file] = [w for w in file_to_terms[file] if w not in stopwords]
            #file_to_terms[file] = [stemmer.stem(w) for w in file_to_terms[file]]
        return file_to_terms

    def index_one_file(self, term_list):
        #input = [word1, word2, ....]
        #output = {word1: [pos1, pos2], word2: [pos2, pos3],...}
        fileIndex = {}
        for index, word in enumerate(term_list):
            if word in fileIndex.keys():
                fileIndex[word].append(index)
            else:
                fileIndex[word] = [index]
        return fileIndex

    def make_indices(self, term_lists):
        #input = {filename: [word1, word2,...], ...}
        #output = {filename: {word:[pos1, pos2, ....}, ...}
        total = {}
        for filename in term_lists.keys():
            total[filename] = self.index_one_file(term_lists[filename])
        return total

    #regular index, which is indexed like {filename: {word:[pos1, pos2, ...}, ...}
    def regIndex(self):
        return self.make_indices(self.file_to_terms)

    #index across all the documents for a word(s), which is the inverted index
    def fullIndex(self):
        #input = {filename: {word:[pos1, pos2, ...}, ...}
        #output = {word: {filename: [pos1, pos2]}, ...}
        total_index = {}
        indices = self.regularIndex
        for filename in indices.keys():
            self.tf[filename] = {}
            for word in indices[filename].keys():
                self.tf[filename][word] = len(indices[filename][word]) #term frequency is term count in a document
                if word in self.df.keys():
                    self.df[word] += 1   #document frequency word/term count across all the documents
                else:
                    self.df[word] = 1
                if word in total_index.keys():
                    if filename in total_index[word].keys():
                        total_index[word][filename].append(indices[filename][word][:])
                    else:
                        total_index[word][filename] = indices[filename][word]
                else:
                    total_index[word] = {filename: indices[filename][word]}
        return total_index

    def vectorize(self):
        vectors = {}
        for filename in self.filenames:
            vectors[filename] = [len(self.regularIndex[filename][word]) for word in self.regularIndex[filename].keys()]
        return vectors

    def magnitudes(self, documents):
        mags = {}
        for doc in documents:
            mags[doc] = pow(sum(map(lambda x: x**2, self.vectors[doc])), .5)
        return mags

    def term_frequency(self, term, document):
        return self.tf[document][term]/self.magni[document] if term in self.tf[document].keys() else 0

    #the number of documents the term t shows up in
    def document_frequency(self, term):
        if term in self.totalIndex.keys():
            return len(self.totalIndex[term].keys())
        else:
            return 0

    #total number of documents
    def collection_size(self):
        return len(self.filenames)

    #the total number of documents divided by the number of documents the term t shows up in
    def inverse_doc_frequency(self, N, N_t):
        if N_t != 0:
            return math.log(N/N_t)
        else:
            return 0

    def getUniques(self):
        return self.totalIndex.keys()

    def populateScores(self):
        for filename in self.filenames:
            for term in self.getUniques():
                self.tf[filename][term] = self.term_frequency(term, filename)
                if term in self.df.keys():
                    self.idf[term] = self.inverse_doc_frequency(self.collection_size(), self.df[term])
                else:
                    self.idf[term] = 0
        return self.df, self.tf, self.idf

    #score
    def generateScores(self, term, document):
        return self.tf[document][term] * self.idf[term]



if __name__ == '__main__':
    invertedIndex = InvertedIndex(['../my_corpus/doc01.txt', '../my_corpus/doc02.txt'])
    terms = invertedIndex.file_to_terms
    #print(terms)
    total = invertedIndex.make_indices(terms)
    #print(total)
    total_index = invertedIndex.fullIndex()
    print(total_index)
    vectors = invertedIndex.vectorize()
    #print(vectors)





