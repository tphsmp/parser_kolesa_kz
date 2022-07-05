import requests
from bs4 import BeautifulSoup
import csv


URL = 'https://kolesa.kz/cars/mercedes-benz/karaganda/?year[from]=2019'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    'accept': '*/*'}
HOST = 'https://kolesa.kz/'
FILE = 'D:\cars.csv'


def get_html(url, params=None):
    r = requests.get(URL, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('div', class_='pager')

    if pagination:

        for page in pagination:
            page = str(page.find('ul').get_text(strip=True, separator=' '))
        page = (page.split())[-1]
        return int(page)

    else:
        page = 1
        return page


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='a-card__info')

    cars = []
    for item in items:
        cars.append({
            'title': item.find('a', class_='a-card__link').get_text(strip=True),
            'price': item.find('span', class_='a-card__price').get_text(strip=True),
            'description': str(item.find('p', class_='a-card__description').get_text(strip=True))[:6],
            'location': item.find('span', class_='a-card__param').get_text(strip=True),
            'link': HOST + item.find('a', class_='a-card__link').get('href')
        })
    return cars


def save_file(items, path):
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Модель', 'Цена', 'Год выпуска', 'Город', 'Ссылка'])
        for item in items:
            writer.writerow([item['title'], item['price'], item['description'], item['location'], item['link']])


def parse():
    html = get_html(URL)
    # print(html)
    if html.status_code == 200:
        cars = []
        # cars = get_content(html.text)
        # print(cars)
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Парсинг старницы {page} из {pages_count}...')
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text))
        # print(pages_count)
        # for value in cars:
        #     print(value.get('title') + ' ' + value.get('price') + ' ' + value.get('location') + ' ' + value.get('link'))
        save_file(cars, FILE)
        print(f'Получено {len(cars)} автомобилей')
    else:
        print('Error')


parse()
