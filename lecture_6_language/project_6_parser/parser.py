import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to" | "until"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP  
S -> S Conj S | S Conj VP NP 

NP -> N | Det NP | Adj NP | N PP | Adv NP | N Adv
PP -> P NP | P NP VP
VP -> V | V NP | V PP | Adv V | V Adv
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)  


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    """word tokenize the sentence"""
    # print(sentence) 
    words = [] 
 
    sentence = sentence.lower() 
    sentence = nltk.word_tokenize(sentence) # tokenize words & all punctuations
   
    for word in sentence:  # for each word check if contain alphabet 
        if word.islower():
            words.append(word) 
     
    return words
    # raise NotImplementedError


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    """list of noun phrases""" 
    leaves = [] # list of NP chunks 

    for s in tree.subtrees(): 
        if s.label() == 'NP' :
        
           # check for its sub-sub-trees for NP
           NP_subtree = False 
           for ss in s.subtrees(): 
               if ss.label() == 'NP' and ss != s:
                   NP_subtree = True

           # if no sub tree contains NP 
           if NP_subtree == False:
               leaves.append(s) 

    return(leaves)
    # raise NotImplementedError


if __name__ == "__main__":
    main()
