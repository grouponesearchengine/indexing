
from bs4 import BeautifulSoup
import json
import re
import os
import pprint


def tag_to_text(tag):
    # TODO figure out how to replace tag with space
    try:
        return tag.get_text()
    except AttributeError as err:
        return ''


def list_to_text(tags):
    return [t.get_text() for t in tags]


def fpath_to_url(path):
    ext = path.split('srep')[-1].split('.')[0]
    return 'https://www.nature.com/articles/srep'+ext


def parse(fpath, html):

    tree = BeautifulSoup(html, 'html.parser')
    title = tree.find('h1', {'itemprop': 'name headline'})
    abstract = tree.find('div', {'id': 'abstract-content'})
    introduction = tree.find('div', {'id': 'introduction-content'})
    results = tree.find('div', {'id': [
        'results-content',
        'results-and-discussion-content'
        ]})
    discussion = tree.find('div', {'id': [
        'discussion-content',
        'conclusions']})
    methods = tree.find('div', {'id': [
        'methods-content',
        'materials-and-methods-content',
        'experimental-content']})
    info = tree.find('div', {'id': 'additional-information-content'})
    subjects = tree \
        .find('div', {'data-component': 'article-subject-links'}) \
        .find_all('li')
    authors = tree \
        .find('li', {'itemprop': 'author'}) \
        .find_all('span', {'itemprop': 'name'})

    try:
        references = tree \
            .find('div', {'id': 'references-content'}) \
            .find('li', {'itemprop': 'citation'}) \
            .find_all('p')
    except AttributeError:
        references = ''

    data = {
        'url': fpath_to_url(fpath),
        'title': tag_to_text(title),
        'abstract': tag_to_text(abstract),
        'introduction': tag_to_text(introduction),
        'results': tag_to_text(results),
        'discussion': tag_to_text(discussion),
        'methods': tag_to_text(methods),
        'info': tag_to_text(info),
        'authors': list_to_text(authors),
        'references': list_to_text(references),
        'subjects': list_to_text(subjects),
    }
    return data


def indexing():
    bpath = 'repository/'
    paths = sorted(os.listdir(bpath))
    articles = []
    max_art = len(paths)-1
    for i, fpath in enumerate(paths):
        html = open(bpath+fpath)
        data = parse(fpath, html)
        articles.append(data)
        if i % 1000 == 999 or i == max_art:
            outpath = 'index'+str(i//1000).zfill(3)+'.json'
            with open(outpath, 'w') as fobj:
                json.dump(articles, fobj)
            articles = []
        print('article', i, 'of', max_art)


if __name__ == '__main__':
    indexing()

