from get_dataset import get_dataset
from text_proc import proc_doc, proc_query, proc_doc_noun_verb, proc_query_noun_verb
from vsm import calculate_docs_tfidf, calculate_querys_tfidf, get_ranking
from evaluation import apply_r_f1, apply_r_recovered, apply_r_precision, apply_fallout

if __name__ == "__main__":
    n = 10

    dataset_name = ''
    while dataset_name not in ['CISI', 'CRAN']:
        dataset_name = input('Escriba el nombre del dataset a utilizar (CISI o CRAN): ')

    files, querys, rel = get_dataset(dataset_name)
    
    proc_type = -1
    while proc_type not in [0, 1]:
        proc_type = int(input('Si desea solo tener en cuenta sustantivos y verbos en el procesamiento de la informacion escriba 1, en otro caso escriba 0: '))

    if proc_type == 0:
        files_text = list(map(lambda x: proc_doc(x.title) + proc_doc(x.body), files))
        querys_text = list(map(lambda x: proc_doc(x.body), querys))
    else:
        files_text = list(map(lambda x: proc_doc_noun_verb(x.title) + proc_doc(x.body), files))
        querys_text = list(map(lambda x: proc_doc_noun_verb(x.body), querys))

    files_tfidf, files_idf = calculate_docs_tfidf(files_text)
    querys_tfidf = calculate_querys_tfidf(querys_text, files_idf, 0.4)

    ranking = get_ranking(files_tfidf, querys_tfidf, n)

    querys_eval = apply_r_f1(n, ranking, rel)
    # querys_eval = apply_r_recovered(n, ranking, rel)
    # querys_eval = apply_r_precision(n, ranking, rel)
    # querys_eval = apply_fallout(n, ranking, rel)

    for key in querys_eval.keys():
        print(querys_eval[key])