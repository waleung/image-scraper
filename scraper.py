import sys, getopt
import os
import time
import re

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
            htmldata = getdata(url)
            soup = BeautifulSoup(htmldata, 'html.parser')   

            cleanString = re.sub(r'\W+', '', url)

            if (not os.path.exists(cleanString)):
                os.makedirs(cleanString)

            for item in soup.find_all('img'): 
                if (item['src'].split('.')[-1] == 'jpg' or item['src'].split('.')[-1] == 'png' or item['src'].split('.')[-1] == 'webp'):
                    print('Downloading', item['src'])

                    img = Image.open(requests.get(item['src'], stream = True).raw)
                    img.save(f'{cleanString}/{item['src'].split('/')[-1]}')
        except Exception as e:
            print(e)

if __name__ == '__main__':
   main(sys.argv[1:])