import sys, getopt
import os
import time
import re

from urllib.parse import urlparse

import requests  
from PIL import Image
from bs4 import BeautifulSoup  

def getdata(url):  
    r = requests.get(url)  
    return r.text  
    
def main(argv):
    url = ''

    opts, arg = getopt.getopt(argv,'u:r:',['url=','res='])
    for opt, arg in opts:
        if opt == '-u':
            url = arg

    if url != '':
        try:
            domain = urlparse(url).netloc
            http_version = url.split('/')[0]

            htmldata = getdata(url)
            soup = BeautifulSoup(htmldata, 'html.parser')   

            cleanString = re.sub(r'\W+', '', url)
        except Exception as e:
            print(e)
            return 

        if not os.path.exists(cleanString):
            os.makedirs(cleanString)

        for item in soup.find_all('img'):   
            try:
                file_ext = item.get('src', '').split('.')[-1]

                if file_ext == 'jpg' or file_ext == 'png' or file_ext == 'webp':
                    print('Downloading', item['src'])

                    if 'http' not in item['src']:
                        img = Image.open(requests.get(f'{http_version}//{domain}{item['src']}', stream = True).raw)
                    else:
                        img = Image.open(requests.get(item['src'], stream = True).raw)

                    img.save(f'{cleanString}/{item['src'].split('/')[-1]}')
            except Exception as e:
                print(e)
                continue

if __name__ == '__main__':
   main(sys.argv[1:])