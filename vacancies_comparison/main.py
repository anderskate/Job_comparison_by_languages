from dotenv import load_dotenv
from get_data_vacancies import (
    get_data_on_vacancies_hh,
    get_data_on_vacancies_sj
)
from calculate_salary import (
    get_predict_rub_salary_hh,
    get_predict_rub_salary_sj
)
from output_statistics import (
    get_language_statistics,
    output_of_data_table_by_language
)


def get_language_statistics_from_hh_and_sj(languages):
    language_statistics_data_hh = {}
    language_statistics_data_sj = {}

    for language in languages:
        vacancies_hh = get_data_on_vacancies_hh(language)
        vacancies_sj = get_data_on_vacancies_sj(language)

        vacancy_salaries_hh = []
        for vacancy in vacancies_hh:
            salary = get_predict_rub_salary_hh(vacancy)
            if salary is not None:
                vacancy_salaries_hh.append(salary)

        vacancy_salaries_sj = []
        for vacancy in vacancies_sj:
            salary = get_predict_rub_salary_sj(vacancy)
            if salary is not None:
                vacancy_salaries_sj.append(salary)

        language_statistics_data_hh[language] = get_language_statistics(
            vacancies_hh,
            vacancy_salaries_hh,
        )
        language_statistics_data_sj[language] = get_language_statistics(
            vacancies_sj,
            vacancy_salaries_sj,
        )

    output_of_data_table_by_language(
        language_statistics_data_hh,
        'HeadHunter Moscow',
    )
    output_of_data_table_by_language(
        language_statistics_data_sj,
        'SuperJob Moscow',
    )


def main():
    load_dotenv()
    languages = [
        'Python',
        'Java',
        'Javascript',
        'Ruby',
        'Swift',
        'Scala',
        'C#',
        'PHP',
    ]
    get_language_statistics_from_hh_and_sj(languages)


if __name__ == '__main__':
    main()
