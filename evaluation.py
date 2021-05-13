

def apply_r_f1(n, querys_rec, querys_rel):
    query_f1 = dict()

    for key in querys_rel.keys():
        query_f1[key] = r_f1(n, querys_rec[key], querys_rel[key])
    
    return query_f1


def apply_r_precision(n, querys_rec, querys_rel):
    query_precision = dict()

    for key in querys_rel.keys():
        query_precision[key] = r_precision(n, querys_rec[key], querys_rel[key])
    
    return query_precision


def apply_r_recovered(n, querys_rec, querys_rel):
    query_recovered = dict()

    for key in querys_rel.keys():
        query_recovered[key] = r_recovered(n, querys_rec[key], querys_rel[key])
    
    return query_recovered


def apply_fallout(n, cant_doc, querys_rec, querys_rel):
    query_fallout = dict()

    for key in querys_rel.keys():
        query_fallout[key] = fallout(n, cant_doc, querys_rec[key], querys_rel[key])

    return query_fallout


def r_f1(n, query_rec, query_rel):
    try:
        return 2 / (1/r_precision(n, query_rec, query_rel) + 1/r_recovered(n, query_rec, query_rel))
    except:
        return 'indefinido'


def r_precision(n, query_rec, query_rel):
    relevant = 0

    for doc in query_rec:
        if doc in query_rel:
            relevant += 1
    
    return relevant/n

def r_recovered(n, query_rec, query_rel):
    recovered = 0

    for doc in query_rec:
        if doc in query_rel:
            recovered += 1

    return recovered/len(query_rel)


def fallout(n, cant_doc, query_rec, query_rel):
    irrelevant = 0

    for doc in query_rec:
        if doc not in query_rel:
            irrelevant += 1

    return irrelevant/(cant_doc - len(query_rel))
