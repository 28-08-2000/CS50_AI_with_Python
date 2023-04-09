import nltk
import sys 
import os 
import operator 
import string 
import numpy as np

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """ 
    """dictionary  key(file name) --> value(string of content)""" 
    files = os.listdir(directory)
    txt_dict = dict()

    for file in files:     # for each text file 
        content = ""       # initialize empty string

        with open(os.path.join(directory, file), encoding="utf-8") as f:
            content += f.read()    #.replace("\n", " ") 
             
        txt_dict[file] = content 

    return txt_dict
    # raise NotImplementedError


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """ 
    words = [] 

    document = document.lower() 
    document = nltk.word_tokenize(document) 

    for word in document:
        if word not in string.punctuation and word not in nltk.corpus.stopwords.words("english"):
            words.append(word) 
     
    return words
    # raise NotImplementedError


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """ 
    """idf value of each word"""
    total_docs = len(documents)  
    words_idf = dict() 

    for document in documents:    # for all documents
        for word in documents[document]: 

            # already not calculated 
            if word not in words_idf: 

                # how many document contain this word
                present_in = 1
                for doc in documents:
                    if doc != document and word in documents[doc]:
                        present_in += 1 

                # idf value using log e 
                words_idf[word] = np.log(total_docs / present_in)  
    
    return words_idf
    # raise NotImplementedError


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """ 
    """best match file"""
    files_rank = dict() 

    for file in files:    # for each file calc file score 
        file_score = 0  
        # for each word in query  
        for word in query:
            TF = files[file].count(word)  
            idf = idfs[word] 
            file_score += TF * idf 

        files_rank[file] = file_score 

    # list of top n files
    best_files = [k for k, v in sorted(files_rank.items(), key = operator.itemgetter(1), reverse= True)[:n]] 

    return best_files 
    # raise NotImplementedError


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """ 
    """best match passage""" 
    """matching word measure""" 
    sentence_rank = dict()

    for sentence in sentences:   # for each sentence
        sentence_score = 0

        # matching word measure
        for word in query:
            if word in sentences[sentence]:
                sentence_score += idfs[word] 
        
        sentence_rank[sentence] = sentence_score
    
    # top n sentences acc matching word measure
    best_sentences = [k for k, v in sorted(sentence_rank.items(), key = operator.itemgetter(1), reverse= True)[:n]]  
    
    """query term density"""
    query_density = dict() 
    for sentence in sentences:  # for each sentece
       QTDensity = 0 
       # calc query term density
       for word in query:
           if word in sentences[sentence]:
               QTDensity += 1
       QTDensity /= len(sentences[sentence]) 

       query_density[sentence] = QTDensity 

    
    # if equal word measure and less term density swap
    for j in range(n):
        for i in range(n - 1):
            if sentence_rank[best_sentences[i]] == sentence_rank[best_sentences[i + 1]] and query_density[best_sentences[i]] < query_density[best_sentences[i + 1]]:
                best_sentences[i], best_sentences[i + 1] = best_sentences[i + 1], best_sentences[i] 

    return best_sentences 
    # raise NotImplementedError


if __name__ == "__main__":
    main()
