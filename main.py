import requests
from terminaltables import AsciiTable
from dotenv import load_dotenv
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
    'page': page
    }

    while page < pages_number:
        page_data = requests.get(url, params=payload).json()
        pages_number = page_data['pages']
        page += 1
        for vacancy in page_data['items']:
            vacancies.append(vacancy)
        print('Скачали страницу hh.ru' + str(page), 'Язык ' + language)

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
        print('Скачали страницу superjob.ru' + str(page), 'Язык ' + language)

    return vacancies

def get_language_statistics(vacancies, vacancy_salaries):

    average_salary_by_language = calculate_average_salary_by_language(vacancy_salaries)
    vacancies_found = len(vacancies)
    vacancies_processed = len(vacancy_salaries)

    language_statistics = {"vacancies_found":vacancies_found,
                        "vacancies_processed": vacancies_processed,
                        "average_salary": average_salary_by_language}

    return language_statistics

def get_predict_salary(salary_from, salary_to):
    if salary_to == None or salary_to == 0:
        return salary_from * 1.2
    elif salary_from == None or salary_from == 0:
        return salary_to * 0.8
    else:
        average_salary = (salary_from + salary_to) / 2

def get_predict_rub_salary_hh(vacancy):
    if vacancy['salary'] == None:
        return None
    elif not 'RUR' in vacancy['salary']['currency']:
        return None
    else:
        salary_from = vacancy['salary']['from']
        salary_to = vacancy['salary']['to']
        return get_predict_salary(salary_from, salary_to)

def get_predict_rub_salary_sj(vacancy):
    if vacancy['payment_from'] == vacancy['payment_to'] == 0:
        return None
    elif not 'rub' in vacancy['currency']:
        return None
    else:
        salary_from = vacancy['payment_from']
        salary_to = vacancy['payment_to']
        return get_predict_salary(salary_from, salary_to)

def calculate_average_salary_by_language(vacancy_salaries):
    if vacancy_salaries == []:
        return None
    summa = 0
    for salary in vacancy_salaries:
        summa += salary
    average_salary_by_language = summa / len(vacancy_salaries)
    return int(average_salary_by_language)  

def output_of_data_table_by_language(languages_data, title):
    table_data = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата'],
        
    ]

    for language, language_values in languages_data.items():
        language_data = []
        language_data.append(language)
        for key, value in language_values.items():
            language_data.append(value)
        table_data.append(language_data)

    table = AsciiTable(table_data, title)
    print(table.table)

def main():
    load_dotenv()
    languages = ['Python', 'Java', 'Javascript', 'Ruby', 'Swift', 'Scala', 'C#', 'PHP']
    language_statistics_data_hh = {}
    language_statistics_data_sj = {}

    for language in languages:
        vacancies_hh = get_data_on_vacancies_hh(language)
        vacancies_sj = get_data_on_vacancies_sj(language)

        vacancy_salaries_hh = []
        for vacancy in vacancies_hh:
            salary = get_predict_rub_salary_hh(vacancy)
            if salary != None:
                vacancy_salaries_hh.append(salary)

        vacancy_salaries_sj = []
        for vacancy in vacancies_sj:
            salary = get_predict_rub_salary_sj(vacancy)
            if salary != None:
                vacancy_salaries_sj.append(salary)

        language_statistics_data_hh[language] = get_language_statistics(vacancies_hh, vacancy_salaries_hh)
        language_statistics_data_sj[language] = get_language_statistics(vacancies_sj, vacancy_salaries_sj)

    output_of_data_table_by_language(language_statistics_data_hh, 'HeadHunter Moscow')
    output_of_data_table_by_language(language_statistics_data_sj, 'SuperJob Moscow')

if __name__ == '__main__':
    main()





