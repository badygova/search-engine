from bs4 import BeautifulSoup
from bs4.element import Comment
import ssl
import re
import requests
import pymorphy2
morph = pymorphy2.MorphAnalyzer()


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return " ".join(t.strip() for t in visible_texts)


def get_data_from_urls():
    with open("1/list.txt") as file:
        array = [row.strip() for row in file]
    return array


def lemming(token):
    w_lemmas = []
    for p in morph.parse(token):
        w_lemmas.append(p.normal_form)

    return list(set(w_lemmas))


if __name__ == '__main__':
    ssl._create_default_https_context = ssl._create_unverified_context
    urls = get_data_from_urls()
    tokens_filename = '2/tokens.txt'
    lemmas_filename = '2/lemmas.txt'
    tokens_file = open(tokens_filename, 'w')
    lemmas_file = open(lemmas_filename, 'w')
    tokens = set()
    result = []

    for idx, url in enumerate(urls):
        response = requests.get('https://' + url, headers={'User-Agent': 'Mozilla/5.0'})

        html = response.text
        text = text_from_html(html)
        list_of_words = re.findall(r'[a-zA-ZА-Яа-яё]{3,}', text)

        for word in list_of_words:
            word = word.lower()
            if (word not in tokens) and (morph.parse(word)[0].tag.POS != ('CONJ' or 'PREP' or 'PRCL' or 'INTJ' or 'ADVB' or 'ADVB' or 'PRED')) and (word != ('еще' or 'ещё')):
                tokens.add(word)
                tokens_file.write(word + '\n')
                lemmas = lemming(word)
                for lem in lemmas:
                    lemmas_file.write(lem + ' ')
                lemmas_file.write('\n')

    tokens_file.close()
    lemmas_file.close()