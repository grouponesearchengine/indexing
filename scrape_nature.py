import shutil
import urllib.request
import time
import re
import os


def init_dir():
    repdir = 'repository/'
    if os.path.exists(repdir):
        shutil.rmtree(repdir)
    os.mkdir(repdir)


def repository_fpath(url):
    fpath = re.sub('\W+', '', url)
    fpath = fpath[:100]
    return 'repository/'+fpath+'.html'


def scrape():
    init_dir()
    host = 'https://www.nature.com/articles/srep'
    for i in range(45784, 1, -1):
        url = host+str(i).zfill(5)
        html = ''
        try:
            res = urllib.request.urlopen(url)
            if res.getcode() == 200:
                html = res.read()
                print('writing', url)
                with open(repository_fpath(url), 'wb') as fobj:
                    fobj.write(html)
        except Exception as err:
            print(err)


if __name__ == '__main__':
    scrape()



