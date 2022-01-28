# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import time
import urllib.request
import requests

if __name__ == '__main__':
    count = 0
    session = requests.Session()
    while count <= 5000:
        count += 1
        response = session.get('https://irs.thsrc.com.tw/IMINT/', cookies={'from-my': 'browser'})
        source = response.content.decode('utf-8')
        soup = BeautifulSoup(source, 'html.parser')
        img = soup.find('img')
        url = 'https://irs.thsrc.com.tw'+img.get('src')
        print(url)
        response = session.get(url, cookies={'from-my': 'browser'})
        with open('/image/'+str(count)+'.jpg', 'wb') as file:
            file.write(response.content)
            file.flush()
