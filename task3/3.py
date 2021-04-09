import re
import zipfile
from functools import cmp_to_key
from main import text_from_html
import pymorphy2
morph = pymorphy2.MorphAnalyzer()


def read_lemmatization():
    f = open("../task2/lemmas.txt", "r")
    lines = f.readlines()
    map = dict()
    for line in lines:
        key = None
        words = re.split('\s+', line)
        for i in range(len(words) - 1):
            if i == 0:
                key = words[i]
                map[key] = []
            else:
                map[key].append(words[i])
    return map


def sort_index(index):
    def comparator(x, y):
        return x[1].general_count - y[1].general_count

    return dict(sorted(index.items(), key=cmp_to_key(comparator), reverse=True))


def get_lemma(word):
    p = morph.parse(word)[0]
    if p.normalized.is_known:
        normal_form = p.normal_form
    else:
        normal_form = word.lower()
    return normal_form


def find_words_in_html_files(map):
    archive = zipfile.ZipFile('../task1/files.zip', 'r')
    index = dict()

    urls_list_file = open("../task1/list.txt", "r")
    lines = urls_list_file.readlines()
    urls_list = []
    for line in lines:
        urls_list.append(line.rstrip())
    for idx, file in enumerate(archive.filelist):
        html = archive.open(file.filename)
        text = text_from_html(html)
        html_word_list = re.findall(r'[А-Яа-яё]{task3,}', text)
        print(idx)
        tokens = set()
        for word in html_word_list:
            if (morph.parse(word)[0].tag.POS != ('CONJ' or 'PREP' or 'PRCL' or 'INTJ' or 'ADVB' or 'ADVB' or 'PRED')) and (word != ('еще' or 'ещё')):
                lemma = get_lemma(word)
                word = word.lower()
                if (lemma in map.keys()) and (word not in tokens):
                    tokens.add(lemma)
                    similar_words = map[lemma]
                    count = 0
                    for similar_word in similar_words:
                        count += html_word_list.count(similar_word)
                    if lemma not in index.keys():
                        index[lemma] = WordWithDocInfo()
                    numbers = re.findall(r'\d+', file.filename)
                    index[lemma].append_document_info(int(numbers[0])-1, count)
        print(file.filename + " проанализирован")
    return dict(sorted(index.items()))


def write_index_result_to_file(index):
    file = open("index.txt", "w")
    for word, doc_info in index.items():
        file_string = word + " "
        for doc in doc_info.documents:
            file_string += " " + str(doc)
        file_string += "\n"
        file.write(file_string)
    file.close()


def create_index():
    map = read_lemmatization()
    index = find_words_in_html_files(map)
    sorted_index = sort_index(index)
    write_index_result_to_file(sorted_index)


def read_index():
    f = open("index.txt", "r")
    lines = f.readlines()
    map = dict()
    for line in lines:
        words = re.split('\s+', line)
        key = words[0]
        if not key in map.keys():
            map[key] = set()
        for i in range(1, len(words) - 1):
            map[key].add(words[i])
    return map


def boolean_search(query, index):
    query_words = re.split('\s+', query)
    page_crossing = set()
    token_query = set(map(lambda x: get_lemma(x), query_words))
    for word in token_query:
        page_crossing = page_crossing | index[word]
    print(page_crossing)


class WordWithDocInfo:
    def __init__(self):
        self.documents = []
        self.general_count = 0

    def append_document_info(self, document_number, document_word_count):
        self.documents.append(document_number)
        self.general_count += document_word_count

if __name__ == '__main__':
    create_index()
    # boolean_search("чашка", read_index())