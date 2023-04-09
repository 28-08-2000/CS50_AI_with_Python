import os
import random
import re
import sys 
import copy  #for deep copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor)  :
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """ 
    """create a sample"""
    prob_dist = {} 
    no_of_pages = len(corpus)

    links = [] 
    for x in corpus[page]:
        links.append(x) 
    no_of_links = len(links) 

    #add the probability of choosing a link on current page is d/links 
    #add the probability of choosing a page randomly from whole corpus is 1-d/pages
    for x in corpus: 
        if x not in links:
           prob_dist[x] = (1 - damping_factor)/no_of_pages 
        else:
            prob_dist[x] = ((1 - damping_factor)/no_of_pages) + (damping_factor/no_of_links)
 

    #print("this is prob distribution")
    #print(prob_dist) 
    return prob_dist
    #raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """ 
    """find weight of each page using markov chain""" 
    #create container to store pages 
    pages_cont = [] 
    for x in corpus:
        pages_cont.append(x) 

    """choose a page  randomly in starting""" 
    rand_page = random.choice(pages_cont)
    curr_page = rand_page

    #create the dictionary for estimated pagerank values
    page_rank = {} 
    for x in pages_cont:
        page_rank[x] = 0  
    """create markov chain""" 
    #generate n samples 
    for i in range(n): 
        page_rank[curr_page] = page_rank[curr_page] + (1/n)  #no of appearances
        sample_dict = transition_model(corpus,curr_page,damping_factor)
        pages_prob_cont = [] 
        for x in sample_dict:
            pages_prob_cont.append(sample_dict[x]) 
        """ choose a page according to previous sample  probability distribution """
        rand_page= random.choices(pages_cont,pages_prob_cont) #return list 
        curr_page = rand_page[0] 
    #print(page_rank) 
    return page_rank
    #raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """ 
    """find weight of each page using iterative rule
       until it converges"""
    #create container to store pages
    pages_cont = []
    for x in corpus:
        pages_cont.append(x) 
    no_of_pages =  len(pages_cont) 

    #if any page has no links add links to every page
    for x in corpus:
        if len(corpus[x]) == 0:
            for i in pages_cont:
                corpus[x].add(i)

    # create a dictionary for incoming pages
    incoming_pages_dict = {}
    for y in pages_cont:
        incoming_pages_dict[y] = set()
    for x in corpus:
        for y in corpus[x]:
            incoming_pages_dict[y].add(x) 

    # create the dictionanry for pagerank values 
    page_rank = {} 
    for x in pages_cont:
        page_rank[x] = 1/no_of_pages # assume initial prob 

    """find probabilities using formula that is based on previous distribution""" 
    while True:  
        prev_page_rank = copy.deepcopy(page_rank) 
        # FIRST CONDITION I
        # probability of the surfer choose a page at random and ended up on page p
        for x in page_rank:
            page_rank[x] = (1-damping_factor)/no_of_pages 
        # SECOND CONDITION II 
        for p in pages_cont:
           summation = 0
           for i in incoming_pages_dict[p]: 
               # probability of the surfer followed a link from a page i to page p
               summation = summation + (prev_page_rank[i] / len(corpus[i]))
           summation = summation*damping_factor
           page_rank[p] = page_rank[p] + summation 
        no_of_changes = 0
        for x in pages_cont: 
            change = abs(page_rank[x] - prev_page_rank[x])
            if change > 0.001: 
                no_of_changes = no_of_changes + 1 
        if no_of_changes == 0:
            break 
    return page_rank
    #raise NotImplementedError


if __name__ == "__main__":
    main()
