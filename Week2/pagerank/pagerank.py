import os
import random
import re
import sys

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


def transition_model(corpus, page, damping_factor):
    """
    Return a probabilitiesy distribution over which page to visit next,
    given a current page.

    With probabilitiesy `damping_factor`, choose a link at random
    linked to by `page`. With probabilitiesy `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    model = {}
    links = corpus[page]
    if links == set():
        prob = 1/len(corpus)
        for key in corpus:
            model[key] = prob
    else:
        prob_of_links = damping_factor/len(links)
        page_prob = (1 - damping_factor)/(len(corpus)) 
        for key in corpus:
            if key in links:
                model[key] = (prob_of_links + page_prob)
            else:
                model[key] = round(page_prob,5)
    return model



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # To get the list of pages in the corpus.
    pages = list(corpus.keys())
    # the dictionary of all posibilties 
    generated_pages = {}
    # picking a random page
    first_page = random.choice(pages)
    # Intilaizing that every page should at first have prob of zero.
    for page in pages:
        generated_pages[page] = 0
    # Updating the value of the first page to be equal 1/n.
    generated_pages[first_page] = 1/n
    # Getting a transition model using the random page we have gotten.
    possiblities = transition_model(corpus, first_page, damping_factor)
    for i in range(0, n-1):
        # Getting a new page but with a weighted random choice we ..
        # the possiblity of each page as a weight.
        new_page = random.choices(list(possiblities.keys()),list(possiblities.values()),k=1)
        # updating the probabilitiesotion of the choosen page.
        generated_pages[new_page[0]] =  generated_pages[new_page[0]] + 1/n
        # Getting a new transition with the new page.
        possiblities = transition_model(corpus, new_page[0],damping_factor)
    return  generated_pages

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
        
    N = len(corpus)
    probabilities = {}
    new_dict = {}

    # assigning each page a rank of 1/n, where n is total number of pages in the corpus
    for page in corpus:
        probabilities[page] = 1 / N

    # repeatedly calculating new rank values basing on all of the current rank values
    while True:
        for page in corpus:
            temp = 0
            for linking_page in corpus:
                # check if page links to our page
                if page in corpus[linking_page]:
                    temp += (probabilities[linking_page] / len(corpus[linking_page]))
                # if page has no links, interpret it as having one link for every other page
                if len(corpus[linking_page]) == 0:
                    temp += (probabilities[linking_page]) / len(corpus)
            temp *= damping_factor
            temp += (1 - damping_factor) / N

            new_dict[page] = temp

        difference = max([abs(new_dict[x] - probabilities[x]) for x in probabilities])
        if difference < 0.001:
            break
        else:
            probabilities = new_dict.copy()

    return probabilities


if __name__ == "__main__":  
    main()