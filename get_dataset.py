from FileAndQuery import File, Query
from json import load
import os

def get_dataset(name):
    current_dir = os.getcwd()
    docs_dir = current_dir + f"/datasets/{name}.ALL.json"
    query_dir = current_dir + f"/datasets/{name}.QRY.json"
    rel_dir = current_dir + f"/datasets/{name}.REL.json"

    with open(docs_dir, 'r') as f:
        json_docs = load(f)
        files = get_docs(json_docs)

    with open(query_dir, 'r') as f:
        json_querys = load(f)
        querys = get_querys(json_querys)

    return files, querys


def get_docs(json_docs):
    docs = []

    for key in json_docs.keys():
        id = int(json_docs[key]['id'])
        title = json_docs[key].get('title', 'empty')
        abstract = json_docs[key].get('abstract', 'empty')
        docs.append(File(id, title, abstract))

    return docs


def get_querys(json_querys):
    querys = []

    for key in json_querys.keys():
        id = int(json_querys[key]['id'])
        text = json_querys[key]['text']
        querys.append(Query(id, text))

    return querys
