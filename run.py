from get_dataset import get_dataset
from text_proc import proc_doc, proc_query, proc_doc_noun_verb, proc_query_noun_verb
from vsm import calculate_docs_tfidf, calculate_querys_tfidf, calculate_query_tfidf, get_ranking, get_query_ranking
from evaluation import apply_r_f1, apply_r_recovered, apply_r_precision, apply_fallout

from json import dump, load
import os


def evaluate_system(dataset_name, proc_type, files, querys, rel, n):
    current_dir = os.getcwd()
    files_tfidf_dir = current_dir + f"/datasets/{dataset_name}.{proc_type}.files_tfidf.json"
    files_idf_dir = current_dir + f"/datasets/{dataset_name}.{proc_type}.files_idf.json"
    querys_tfidf_dir = current_dir + f"/datasets/{dataset_name}.{proc_type}.querys_tfidf.json"

    try:
        with open(files_tfidf_dir, 'r') as f:
            tfidf = load(f)

            files_tfidf = dict()
            for key in tfidf.keys():
                files_tfidf[int(key)] = tfidf[key]

        with open(querys_tfidf_dir, 'r') as f:
            tfidf = load(f)

            querys_tfidf = dict()
            for key in tfidf.keys():
                querys_tfidf[int(key)] = tfidf[key]

    except:
        if proc_type == 0:
            files_text = list(map(lambda x: proc_doc(x.title) + proc_doc(x.body), files))
            querys_text = list(map(lambda x: proc_query(x.body), querys))
        else:
            files_text = list(map(lambda x: proc_doc_noun_verb(x.title) + proc_doc(x.body), files))
            querys_text = list(map(lambda x: proc_query_noun_verb(x.body), querys))

        files_tfidf, files_idf = calculate_docs_tfidf(files_text)
        querys_tfidf = calculate_querys_tfidf(querys_text, files_idf, 0.4)

        with open(files_tfidf_dir, 'w') as f:
            dump(files_tfidf, f)

        with open(files_idf_dir, 'w') as f:
            dump(files_idf, f)

        with open(querys_tfidf_dir, 'w') as f:
            dump(querys_tfidf, f)


    ranking = get_ranking(files_tfidf, querys_tfidf, n)

    querys_eval = apply_r_f1(n, ranking, rel)
    # querys_eval = apply_r_recovered(n, ranking, rel)
    # querys_eval = apply_r_precision(n, ranking, rel)
    # querys_eval = apply_fallout(n, len(files), ranking, rel)

    for key in querys_eval.keys():
        print(querys_eval[key])


def personal_query(dataset_name, proc_type, files, n):
    current_dir = os.getcwd()
    files_tfidf_dir = current_dir + f"/datasets/{dataset_name}.{proc_type}.files_tfidf.json"
    files_idf_dir = current_dir + f"/datasets/{dataset_name}.{proc_type}.files_idf.json"
    
    try:
        with open(files_tfidf_dir, 'r') as f:
            tfidf = load(f)

            files_tfidf = dict()
            for key in tfidf.keys():
                files_tfidf[int(key)] = tfidf[key]

        with open(files_idf_dir, 'r') as f:
            files_idf = load(f)
    
    except:
        if proc_type == 0:
            files_text = list(map(lambda x: proc_doc(x.title) + proc_doc(x.body), files))
        else:
            files_text = list(map(lambda x: proc_doc_noun_verb(x.title) + proc_doc(x.body), files))

        files_tfidf, files_idf = calculate_docs_tfidf(files_text)

        with open(files_tfidf_dir, 'w') as f:
            dump(files_tfidf, f)

        with open(files_idf_dir, 'w') as f:
            dump(files_idf, f)

    query = input('Escriba su consulta: ')

    if proc_type == 0:
        query_text = proc_query(query)
    else:
        query_text = proc_query_noun_verb(query)

    querys_tfidf = calculate_query_tfidf(query_text, files_idf, 0.4)

    ranking = get_query_ranking(files_tfidf, querys_tfidf, n)
    
    for file_id in ranking:
        print(files[file_id-1])




if __name__ == "__main__":
    n = 10

    dataset_name = ''
    while dataset_name not in ['CISI', 'CRAN']:
        dataset_name = input('Escriba el nombre del dataset a utilizar (CISI o CRAN): ')

    files, querys, rel = get_dataset(dataset_name)
    
    proc_type = -1
    while proc_type not in [0, 1]:
        proc_type = int(input('Si desea solo tener en cuenta sustantivos y verbos en el procesamiento de la informacion escriba 1, en otro caso escriba 0: '))
    
    write_query = -1
    while write_query not in [0,1]:
        write_query = int(input('Si desea realizar una query escriba 1 y si desea realizar una evaluacion del sistema escriba 0: '))

    print('\n')
    
    if write_query == 0:
        evaluate_system(dataset_name, proc_type, files, querys, rel, n)
    else:
        personal_query(dataset_name, proc_type, files, n)

    