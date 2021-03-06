'''
blog: http://aakashjapi.com/fuckin-search-engines-how-do-they-work/
https://github.com/logicx24/Text-Search-Engine

https://www.youtube.com/watch?v=o5uqBRt-akw&list=PL0ZVw5-GryEkGAQT7lX7oIHqyDPeUyOMQ&index=7
to implement and query

https://stackoverflow.com/questions/15173225/calculate-cosine-similarity-given-2-sentence-strings

http://www.sfs.uni-tuebingen.de/~ddekok/ir/lectures/tf-idf-dump.html

https://www.machinelearningplus.com/nlp/cosine-similarity/
'''

from index_search.index import InvertedIndex
import re

class Query:

    def __init__(self, filenames):
        self.filenames = filenames
        self.index = InvertedIndex(self.filenames)
        self.invertedIndex = self.index.totalIndex
        self.regularIndex = self.index.regularIndex

    def is_word_stopword(self, word):
        stopwords = open('../my_corpus/stopwords.txt').read()
        if word in stopwords:
            return True
        else:
            return False

    '''finding the score of each word in corpus'''
    def make_vectors(self, documents):
        vecs = {}
        for doc in documents:
            doc_vec = [0] * len(self.index.getUniques())  # array object with zero filled will be created.
            for ind, term in enumerate(self.index.getUniques()): #enumerating each term in indexed documents
                try:
                    doc_vec[ind] = self.index.generateScores(term, doc)  #storing earch term score => tf*idf
                except Exception:
                    pass
            vecs[doc] = doc_vec
        return vecs

    '''in given search query, finding the frequency of given words by comparing with indexed terms'''
    def query_freq(self, term, query):
        count = 0
        for word in query.split():
            if word == term:
                count += 1
        return count

    '''finding the all indexed terms frequency with the query terms, if term is having
    frequency means query terms exists in document(s).'''
    def term_freq(self, terms, query):
        temp = [0] * len(terms)   # array object with zero filled will be created.
        for i, term in enumerate(terms):
            temp[i] = self.query_freq(term, query)
        return temp

    def query_vec(self, query):
        pattern = re.compile('[\W_]+')
        query = pattern.sub(' ', query)
        query1s = query.split()
        queryVec = [0] * len(query1s)    # array object with zero filled will be created.
        index = 0
        final = []
        for ind, word in enumerate(query1s):
            queryVec[index] = self.query_freq(word, query)
            index += 1
        try:
            #getting the idf for each term in corpus
            queryidf = [self.index.idf[word] for word in self.index.getUniques()]
            # finding the magnitude of query terms,those are in
            # indexed documents.
            magnitude = pow(sum(map(lambda x: x**2, queryVec)), .5)
            # finding query terms in indexed document terms
            freq = self.term_freq(self.index.getUniques(), query)
            tf = [x/magnitude for x in freq]
            #score
            finalScore = [tf[i] * queryidf[i] for i in range(len(self.index.getUniques()))]
        except Exception:
            pass
        return finalScore


    def dotProduct(self, doc1, doc2):
        if len(doc1) != len(doc2):
            return 0
        return sum([x*y for x, y in zip(doc1, doc2)])


    '''gives the documenst(s) for matched term queries.'''
    def rankResults(self, resultDocs, query):
        vectors = self.make_vectors(resultDocs)
        queryVec = self.query_vec(query)
        results = [[self.dotProduct(vectors[result], queryVec), result] for result in resultDocs]
        results.sort(key=lambda x: x[0])
        results = [x[1] for x in results]
        return results

    '''This method gives the document(s) for matched term'''
    def one_word_query(self, word):
        pattern = re.compile('[\W_]+')
        word = pattern.sub(' ', word)
        flag = self.is_word_stopword(word)
        if flag:
            #print("User another word.")
            return ""

        if word in self.invertedIndex.keys():
            return self.rankResults([filename for filename in self.invertedIndex[word].keys()], word)
        else:
            return []

    '''This method gives the document(s) for matched terms'''
    def free_text_query(self, textQ):
        pattern = re.compile('[\W_]+')
        textQ = pattern.sub(' ', textQ)
        result = []
        for word in textQ.split():
            result += self.one_word_query(word)
        return self.rankResults(list(set(result)), textQ)

    '''This method gives the document(s) for matched terms which are in adjacent'''
    def phrase_query(self, textQ):
        pattern = re.compile('[\W_]+')
        textQ = pattern.sub(' ', textQ)
        listOfLists, result = [],[]
        for word in textQ.split():
            listOfLists.append(self.one_word_query(word))
        setted = set(listOfLists[0]).intersection(*listOfLists)  #means unpacks the listOfLists into intersection
        for filename in setted:
            temp = []
            for word in textQ.split():
                temp.append(self.invertedIndex[word][filename][:])
            for i in range(len(temp)):
                for ind in range(len(temp[i])):
                    temp[i][ind] -= i
            if set(temp[0]).intersection(*temp):
                result.append(filename)
        return self.rankResults(result, textQ)


if __name__ == '__main__':
    query = Query(['../my_corpus/doc01.txt', '../my_corpus/doc02.txt'])
    results = query.one_word_query('straight')
    print("One word query: ", results)

    results = query.phrase_query('great disappointment')
    print("Phrase Query: ", results)

    results = query.free_text_query('seemed quite natural flashed across')
    print("Free Text Query: ", results)
