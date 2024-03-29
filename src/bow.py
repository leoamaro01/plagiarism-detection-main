from math import log, sqrt

def bow(text1: str, text2: str, pgphs1: list[str], pgphs2: list[str]) -> list[float]:    
    # gets the unique terms in the whole "corpus"
    terms = get_terms(text1 + ' ' + text2)
    
    # now we create a frequency matrix, where each row is 
    # a frequency vector for a paragraph
    t1feqs = list(map(lambda p: get_terms_frequencies(p, terms), pgphs1))
    t2feqs = list(map(lambda p: get_terms_frequencies(p, terms), pgphs2))

    bow1 = list(map(lambda f: get_doc_tf_idf(f, t1feqs), t1feqs))
    bow2 = list(map(lambda f: get_doc_tf_idf(f, t2feqs), t2feqs))
    
    def get_best_similarity(v: list[float]) -> float:
        return max(map(lambda p: cosine_similarity(v, p)
                       , bow2))
    
    return list(map(get_best_similarity, bow1))
    

# returns how similar two vectors are in terms of the angle between them
def cosine_similarity(v1: list[float], v2: list[float]):
    dot_product = sum(map(lambda x, y: x * y, v1, v2))
    norm1 = sqrt(sum(map(lambda x: x*x, v1)))
    norm2 = sqrt(sum(map(lambda x: x*x, v2)))
    
    return dot_product / (norm1 * norm2)


# retrieves a list of the unique terms in a text.
# e.g. "love is love, always love yourself" -> ["love", "is", "always", "yourself"]
def get_terms(text: str) -> list[str]:
    words = text.split()
    
    unique_words = []
    
    for w in words:
        if w not in unique_words:
            unique_words.append(w)
            
    return unique_words




# calculates the tf_idf vector for a document frequencies vector
def get_doc_tf_idf(doc_freqs: list[int], corpus: list[list[int]]) -> list[float]:
    max_freq = max(doc_freqs)
    if max_freq == 0:
        return list(map(lambda _: 0, range(len(doc_freqs))))
    corpus_len = len(corpus)
    
    def get_tf(t_idx: int) -> float:           
        return doc_freqs[t_idx] / max_freq
    
    def get_idf(t_idx: int) -> float:
        docs_with_t: float = 0 # type float to avoid integer division
        for d in corpus:
            if d[t_idx] > 0:
                docs_with_t += 1
        
        return log(corpus_len / docs_with_t)
    
    def get_tfidf(t_idx: int) -> float:
        tf = get_tf(t_idx)
        if tf > 0:         
            return tf * get_idf(t_idx)
        else:
            return 0
    
    return list(map(get_tfidf, range(len(doc_freqs))))
    

# returns a list with the frequency of each term in `terms` found in `text`
def get_terms_frequencies(text: str, terms: list[str]) -> list[int]:
    freqs = []
    
    words = text.split()
    
    for t in terms:
        count = 0
        for w in words:
            if w == t:
                count += 1
        freqs.append(count)
    
    return freqs

