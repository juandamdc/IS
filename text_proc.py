import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def proc_doc(data):
    data = basic_proc(data)
    data = data.split(' ')
    data = lemmatize(data)
    data = remove_stopwords(data)
    return data


def proc_query(data):
    data = basic_proc(data)
    data = data.split(' ')
    data = lemmatize(data)
    data = remove_stopwords(data)
    return data


def proc_doc_noun_verb(data):
    data = basic_proc(data)
    data = nltk.word_tokenize(data)
    tagged_data = nltk.pos_tag(data)
    data = list(map(lambda x: x[0], filter(lambda x: x[1]=='NN' or x[1]=='VB', tagged_data)))
    data = lemmatize(data)
    return data


def proc_query_noun_verb(data):
    data = basic_proc(data)
    data = nltk.word_tokenize(data)
    tagged_data = nltk.pos_tag(data)
    data = list(map(lambda x: x[0], filter(lambda x: x[1] in ['NN', 'NNS', 'NNP', 'NNPS', 'VB', 'VBG', 'VBD', 'VBN', 'VBP', 'VBZ'], tagged_data)))
    data = lemmatize(data)
    return data


def basic_proc(data):
    data = data.lower()  # lowercasing the text
    data = re.sub(r'http\S+|www\S+', '', data)  #  remove the urls
    data = remove_punctuation(data)  # remove the symbols
    data = re.sub(r' +', ' ', data)  # remove the extra empty spaces
    return data


def remove_punctuation(data):
    punctuation = r'[!"#$%-./:;<=>@|?*+()^_`{}~\[\]\\\n]'
    return re.sub(punctuation, ' ', data)


def remove_stopwords(data):
    return [w for w in data if w not in stopwords.words('english')]


def lemmatize(data):
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(w) for w in data]
