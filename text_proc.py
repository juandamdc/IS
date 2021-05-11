import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def proc_doc(data):
    data = data.lower()  # lowercasing the text
    data = re.sub(r'http\S+|www\S+', '', data)  #  remove the urls
    data = remove_punctuation(data)  # remove the symbols
    data = re.sub(r' +', ' ', data)  # remove the extra empty spaces
    data = data.split(' ')
    data = lemmatize(data)
    data = remove_stopwords(data)
    return data


def proc_query(data):
    data = data.lower()  # lowercasing the text
    data = re.sub(r'http\S+|www\S+', '', data)  #  remove the urls
    data = remove_punctuation(data)  # remove the symbols
    data = re.sub(r' +', ' ', data)  # remove the extra empty spaces
    data = data.split(' ')
    return data


def remove_punctuation(data):
    punctuation = r'[!"#$%-./:;<=>@|?*+()^_`{}~\[\]\\\n]'
    return re.sub(punctuation, ' ', data)


def remove_stopwords(data):
    return [w for w in data if w not in stopwords.words('english')]


def lemmatize(data):
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(w) for w in data]