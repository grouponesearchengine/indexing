from bs4 import BeautifulSoup
import pprint
import shutil
import json
import re
import os


def init_dir():
    repdir = 'index/'
    if os.path.exists(repdir):
        shutil.rmtree(repdir)
    os.mkdir(repdir)


def tag_to_text(tag):
    # TODO figure out how to replace tag with space
    try:
        return tag.get_text().strip()
    except AttributeError:
        return ''


def list_to_text(tags):
    try:
        return [t.get_text().strip() for t in tags]
    except AttributeError:
        return []


def fpath_to_url(path):
    ext = path.split('srep')[-1].split('.')[0]
    return 'https://www.nature.com/articles/srep'+ext


def trans_re(text):
    trans = {'<': ' <', '/>': ' />'}
    regex = re.compile("(%s)" % "|".join(map(re.escape, trans.keys())))
    text_n = regex.sub(lambda mo: trans[mo.string[mo.start():mo.end()]], text)
    return re.sub(' +', ' ', text_n)


def parse(fpath, html):

    html = trans_re(html.read())

    tree = BeautifulSoup(html, 'lxml')
    title = tree.find('h1', {'itemprop': 'name headline'})
    abstract = tree.find('div', {'id': 'abstract-content'})
    introduction = tree.find('div', {'id': 'introduction-content'})
    results = tree.find('div', {'id': [
        'results-content',
        'results-and-discussion-content']})
    discussion = tree.find('div', {'id': [
        'discussion-content',
        'conclusions']})
    methods = tree.find('div', {'id': [
        'methods-content',
        'materials-and-methods-content',
        'experimental-content']})
    date = tree.find('time')
    volume = tree.find('div', {'data-container-section': 'info'})
    cited = tree.find('p', {'data-test': 'citation-count'})
    info = tree.find('div', {'id': 'additional-information-content'})
    
    try:
        subjects = tree \
            .find('div', {'data-component': 'article-subject-links'}) \
            .find_all('li')
    except AttributeError:
        subjects = []

    try:
        authors = tree \
            .find('li', {'itemprop': 'author'}) \
            .find_all('span', {'itemprop': 'name'})
    except AttributeError:
        authors = []

    try:
        references = tree \
            .find('div', {'id': 'references-content'}) \
            .find('li', {'itemprop': 'citation'}) \
            .find_all('p')
    except AttributeError:
        references = []

    data = {
        'url': fpath_to_url(fpath),
        'title': tag_to_text(title),
        'abstract': tag_to_text(abstract),
        'introduction': tag_to_text(introduction),
        'results': tag_to_text(results),
        'discussion': tag_to_text(discussion),
        'methods': tag_to_text(methods),
        'date': tag_to_text(date),
        'volume': tag_to_text(volume),
        'cited': tag_to_text(cited),
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
            outpath = 'index/index'+str(i//1000).zfill(3)+'.json'
            with open(outpath, 'w') as fobj:
                json.dump(articles, fobj)
            articles = []
        print('article', i, 'of', max_art)


if __name__ == '__main__':
    indexing()

