import requests
from bs4 import BeautifulSoup
from time import sleep

headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:106.0) Gecko/20100101 Firefox/106.0"}

def download(url):
    '''
    Код для скачивания файлов по ссылке
    '''
    resp = requests.get(url, stream=True)
    r = open("C:\\Users\\Egor\\Downloads\\Parsing_folder\\images\\" + url.split("/")[-1], "wb")
    for value in resp.iter_content(1024*1024):
        r.write(value)
    r.close()

def get_url():
    '''
    Сбор ссылок с карточками товара
    '''
    for count in range(1, 8):
        print(f'Сбор данных со страницы {count} выполняется')
        url = f'https://scrapingclub.com/exercise/list_basic/?page={count}'

        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, 'lxml') #html.parser

        data = soup.find_all("div", class_="col-lg-4 col-md-6 mb-4")

        for i in data: 
            card_url = 'https://scrapingclub.com' + i.find('a').get('href')
            yield card_url


def array():
    '''
    Сбор данных, а именно названия, стоимости, описания и ссылки товаров
    '''
    for card_url in get_url():
        response = requests.get(card_url, headers=headers)

        sleep(3)
        soup = BeautifulSoup(response.text, 'lxml') #html.parser

        data = soup.find("div", class_="card mt-4 my-4")

        name = data.find('h3', class_='card-title').text.replace("\n", "")
        price = data.find('h4').text
        text = data.find('p', class_='card-text').text
        url_img = 'https://scrapingclub.com' + data.find('img', class_="card-img-top img-fluid").get('src')
        
        download(url_img)

        yield name, price, text, url_img