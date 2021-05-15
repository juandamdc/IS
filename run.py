from get_dataset import get_dataset
from text_proc import proc_doc, proc_query, proc_doc_noun_verb, proc_query_noun_verb
from vsm import calculate_docs_tfidf, calculate_querys_tfidf, calculate_query_tfidf, get_ranking, get_query_ranking, query_feedback
from evaluation import apply_r_f1, apply_r_recovered, apply_r_precision, apply_fallout

import statistics
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

    querys_eval_r_f1 = apply_r_f1(n, ranking, rel)
    querys_eval_r_recovered = apply_r_recovered(n, ranking, rel)
    querys_eval_r_precision = apply_r_precision(n, ranking, rel)
    querys_eval_fallout = apply_fallout(n, len(files), ranking, rel)

    print('Evaluacion del sistema')
    print(f'promedio {n}-Recobrado: ', statistics.mean(querys_eval_r_recovered.values()))
    print(f'promedio {n}-Precision: ', statistics.mean(querys_eval_r_precision.values()))
    print(f'promedio {n}-F1: ', statistics.mean(filter(lambda x: x != 'indefinido', querys_eval_r_f1.values())))
    print(f'promedio {n}-Fallout: ', statistics.mean(querys_eval_fallout.values()))


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

    querys_num = 0
    querys_text_id = dict()
    querys_id_relevant = dict()
    querys_id_irrelevant = dict()
    
    print('''    Para escribir una consulta use el comando: query <query text>
    Para adicionar un documento al conjunto de documentos relevantes para una consulta use el comando: relevant <query_id> <document_id>
    Para adicionar un documento al conjunto de documentos no relevantes para una consulta use el comando: irrelevant <query_id> <document_id> 
    Para salir presione Enter''')

    while True:
        input_str = input('>>: ')

        if input_str == '':
            break

        input_str = input_str.split(' ', 1)
        if input_str[0] == 'query':
            querys_num = input_query(proc_type, input_str[1], querys_num, querys_text_id, querys_id_relevant, querys_id_irrelevant, files, files_tfidf, files_idf, n)
        elif input_str[0] == 'relevant':
            input_relevant(input_str[1], querys_id_relevant, querys_num, len(files))
        elif input_str[0] == 'irrelevant':
            input_irrelevant(input_str[1], querys_id_irrelevant, querys_num, len(files))
        else:
            print('Escriba un comendo valido\n')


def input_query(proc_type, query, querys_num, querys_text_id, querys_id_relevant, querys_id_irrelevant, files, files_tfidf, files_idf, n):
    if querys_text_id.get(query, 0) == 0:
        querys_num += 1
        querys_text_id[query] = querys_num
    
    query_id = querys_text_id[query]
    print(f'Query id: {query_id}')
    print(querys_id_relevant.get(query_id, []))
    print(querys_id_irrelevant.get(query_id, []))

    if proc_type == 0:
        query_text = proc_query(query)
    else:
        query_text = proc_query_noun_verb(query)

    query_tfidf = calculate_query_tfidf(query_text, files_idf, 0.4)
    query_tfidf = query_feedback(query_tfidf, querys_id_relevant.get(query_id, []), querys_id_irrelevant.get(query_id, []), files_tfidf) 

    ranking = get_query_ranking(files_tfidf, query_tfidf, n)
        
    for file_id in ranking:
        print(files[file_id-1])

    return querys_num


def input_relevant(input_str, querys_id_relevant, querys_num, files_num):
    input_str = input_str.split(' ')

    if len(input_str) > 2:
        print('Escriba un comendo valido\n')
        return
    
    query_id = int(input_str[0])
    file_id = int(input_str[1])
    
    if query_id <= 0 or query_id > querys_num:
        print(f'No existe una query con dicho id({query_id})')
        return

    if file_id <= 0 or file_id > files_num:
        print(f'No existe un documento con dicho id({file_id})')
        return

    if querys_id_relevant.get(query_id, []) == []:
        querys_id_relevant[query_id] = []
    
    querys_id_relevant[query_id].append(file_id)
    

def input_irrelevant(input_str, querys_id_irrelevant, querys_num, files_num):
    input_str = input_str.split(' ')

    if len(input_str) > 2:
        print('Escriba un comendo valido\n')
        return

    query_id = int(input_str[0])
    file_id = int(input_str[1])

    if query_id <= 0 or query_id > querys_num:
        print(f'No existe una query con dicho id({query_id})')
        return

    if file_id <= 0 or file_id > files_num:
        print(f'No existe un documento con dicho id({file_id})')
        return

    if querys_id_irrelevant.get(query_id, []) == []:
        querys_id_irrelevant[query_id] = []
    
    querys_id_irrelevant[query_id].append(file_id)





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

    