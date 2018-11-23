from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json
import time
import os


def fpath_to_url(path):
    ext = path.split('srep')[-1].split('.')[0]
    return 'https://www.nature.com/articles/srep'+ext


def load_json(path):
    if path.endswith('.json'):
        with open(path, 'r') as open_file:
            return json.load(open_file)


def bulk_load():
    bpath = 'index/'
    fpaths = sorted(os.listdir(bpath))
    es = Elasticsearch()
    for fpath in fpaths:
        helpers.bulk(
            es, load_json(bpath+fpath),
            index='science', doc_type='article')
        print(bpath+fpath+' loaded into database...')
        # time.sleep(30)


if __name__ == '__main__':
    bulk_load()

