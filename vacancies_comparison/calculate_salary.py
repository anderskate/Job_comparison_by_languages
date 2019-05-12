def get_predict_salary(salary_from, salary_to):
    if salary_to is None or salary_to == 0:
        return salary_from * 1.2
    elif salary_from is None or salary_from == 0:
        return salary_to * 0.8
    else:
        average_salary = (salary_from + salary_to) / 2
        return average_salary


def get_predict_rub_salary_hh(vacancy):
    if vacancy['salary'] is None:
        return None
    elif 'RUR' not in vacancy['salary']['currency']:
        return None
    else:
        salary_from = vacancy['salary']['from']
        salary_to = vacancy['salary']['to']
        return get_predict_salary(salary_from, salary_to)


def get_predict_rub_salary_sj(vacancy):
    if vacancy['payment_from'] == vacancy['payment_to'] == 0:
        return None
    elif 'rub' not in vacancy['currency']:
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
