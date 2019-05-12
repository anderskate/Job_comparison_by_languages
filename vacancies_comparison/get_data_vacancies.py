import requests
import os


def get_data_on_vacancies_hh(language):
    url = 'https://api.hh.ru/vacancies'

    vacancies = []
    page = 0
    pages_number = 1

    payload = {
        'text': 'Программист ' + language,
        'area': '1',
        'period': '30',
        'page': page,
    }

    while page < pages_number:
        page_data = requests.get(url, params=payload).json()
        pages_number = page_data['pages']
        page += 1
        for vacancy in page_data['items']:
            vacancies.append(vacancy)
        print('Скачали страницу hh.ru ' + str(page), 'Язык ' + language)

    return vacancies


def get_data_on_vacancies_sj(language):
    url = 'https://api.superjob.ru/2.0/vacancies'

    vacancies = []
    page = 0
    pages_number = 1

    headers = {"X-Api-App-Id": os.getenv("SECRET_KEY")}
    payload = {"keyword": "Программист " + language,
               "town": 4,
               'page': page}

    while page < pages_number:
        page_data = requests.get(url, headers=headers, params=payload).json()
        pages_number = page_data['total']
        page += 1
        for vacancy in page_data['objects']:
            vacancies.append(vacancy)
        print('Скачали страницу superjob.ru ' + str(page), 'Язык ' + language)

    return vacancies
    
