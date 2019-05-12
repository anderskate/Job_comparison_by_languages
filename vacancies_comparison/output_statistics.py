from terminaltables import AsciiTable
from calculate_salary import calculate_average_salary_by_language


def get_language_statistics(vacancies, vacancy_salaries):
    average_salary_by_language = calculate_average_salary_by_language(
        vacancy_salaries
    )
    vacancies_found = len(vacancies)
    vacancies_processed = len(vacancy_salaries)

    language_statistics = {
        "vacancies_found": vacancies_found,
        "vacancies_processed": vacancies_processed,
        "average_salary": average_salary_by_language,
    }

    return language_statistics


def output_of_data_table_by_language(languages_data, title):
    table_data = [
        [
            'Язык программирования',
            'Вакансий найдено',
            'Вакансий обработано',
            'Средняя зарплата',
        ],
    ]

    for language, language_values in languages_data.items():
        language_data = []
        language_data.append(language)
        for key, value in language_values.items():
            language_data.append(value)
        table_data.append(language_data)

    table = AsciiTable(table_data, title)
    print(table.table)
