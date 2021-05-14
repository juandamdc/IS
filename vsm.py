from math import log, sqrt


def calculate_docs_tfidf(files):
    n_i = dict()

    # calculate tf
    files_tf = [] 
    for file in files:
        files_tf.append(calculate_tf(file, n_i))

    # calculate idf
    N = len(files)
    files_idf = dict()

    for key in n_i.keys():
        files_idf[key] = log(N/n_i[key], 10)

    # calculate tfidf
    files_tfidf = dict()
    for i in range(len(files)):
        files_tfidf[i+1] = dict()
        for key in files_tf[i]:
            files_tfidf[i+1][key] = files_tf[i][key] * files_idf[key] 

    return files_tfidf, files_idf


def calculate_querys_tfidf(querys, files_idf, alpha):
    querys_tfidf = dict()
    
    for i in range(len(querys)):
        querys_tfidf[i+1] = calculate_query_tfidf(querys[i], files_idf, alpha)

    return querys_tfidf


def calculate_query_tfidf(query, files_idf, alpha):
    # calculate tf
    query_tf = calculate_tf(query, dict())

    # calculate tfidf    
    query_tfidf = dict()
    for key in query_tf:
            query_tfidf[key] = (alpha + (1 - alpha) * query_tf[key]) * files_idf.get(key, 0)

    return query_tfidf


def calculate_tf(text, n_i):
    word_count = dict()

    for word in text:
        if word in word_count.keys():
            word_count[word] = word_count[word] + 1
        elif word in n_i.keys():
            word_count[word] = 1
            n_i[word] = n_i[word] + 1
        else:
            word_count[word] = 1
            n_i[word] = 1

    max_f = max(word_count.values())

    for key in word_count.keys():
        word_count[key] = word_count[key] / max_f

    return word_count


def get_ranking(docs, querys, n):
    ranking = dict()

    for key in querys.keys():
        ranking[key] = get_query_ranking(docs, querys[key], n)

    return ranking


def get_query_ranking(docs, query, n):
    query_ranking = dict()

    for key in docs.keys():
        query_ranking[key] = ranking_function(docs[key], query)

    return get_tops(query_ranking, n)


def get_tops(ranking, n):
    return list(map(lambda x: x[0], sorted(ranking.items(), key=(lambda x: x[1]), reverse=True)))[:n]


def ranking_function(doc, query):
    return sum([doc.get(key, 0) * query[key] for key in query.keys()]) / (mod_vector(doc) * mod_vector(query))


def mod_vector(vector):
    return sqrt(sum(map(lambda x: x**2, vector.values())))


def query_feedback(query_tfidf, relevant_docs, irrelevant_docs, files_tfidf):
    words = set(query_tfidf.keys())

    for doc in relevant_docs:
        words = words.union(files_tfidf[doc].keys())

    for doc in irrelevant_docs:
        words = words.union(files_tfidf[doc].keys())

    for word in words:
        query_tfidf[word] = query_tfidf.get(word, 0) + 0.75 * 1/max(len(relevant_docs), 1) * sum([files_tfidf[doc].get(word, 0) for doc in relevant_docs]) + 0.15 * 1/max(len(irrelevant_docs), 1) * sum([files_tfidf[doc].get(word, 0) for doc in irrelevant_docs])

    return query_tfidf