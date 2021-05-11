from get_dataset import get_dataset
from vsm import calculate_docs_tfidf, calculate_querys_tfidf, get_ranking

if __name__ == "__main__":
    files, querys = get_dataset('CRAN')

    files_text = list(map(lambda x: x.proc, files))
    querys_text = list(map(lambda x: x.proc, querys))

    files_tfidf = calculate_docs_tfidf(files_text)
    querys_tfidf = calculate_querys_tfidf(querys_text, 0.4)

    ranking = get_ranking(files_tfidf, querys_tfidf, 10)

    print(ranking[1])