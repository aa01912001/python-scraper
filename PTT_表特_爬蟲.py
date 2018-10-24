import requests
import os
import csv
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
def main():

    req = requests.get('https://www.ptt.cc/bbs/Beauty/index.html')

    image_counter = 0
    image_url = []
    for i in range(1):
        ''' get imgur url  '''
        bsObj = BeautifulSoup(req.text, 'html.parser')
        title_data = bsObj.find('div', {'class':'btn-group btn-group-paging'}).find_all('a', {'class':'wide'})
        last_url = title_data[1]['href']  # last url

        last_req = requests.get('https://www.ptt.cc' + last_url)
        bsObj = BeautifulSoup(last_req.text, 'html.parser')
        last_title_data = bsObj.find_all('div', {'class':'title'})
        last_title_data

        def get_image_from_this_page(title_url, image_number):
            title_req = requests.get('https://www.ptt.cc' + title_url)
            bsObj = BeautifulSoup(title_req.text, 'html.parser')
            file_url = bsObj.find('div', {'id':'main-content'}).find('a')['href']
            if file_url[:5] == 'https' and file_url[-3:] == 'jpg':
                print(file_url)
                image_url.append(file_url)

        #urlretrieve(file_url, filename=r'C:\Users\aa019\Desktop\PTT表特爬蟲\image\image' + str(image_number) + '.jpg')
        for title_url in last_title_data:
            image_counter += 1
            try:
                get_image_from_this_page(title_url.find('a')['href'], image_counter)
            except:
                image_counter -= 1

        req = last_req

    with open('image_url.csv', 'w', newline='') as f:
        writer = csv.writer(f)

        for url in image_url[:len(image_url)-1]:
            writer.writerow([url])

if __name__ == "__main__":
    main()
