import json
import requests


class HH:
    """Класс для доступа к API HeadHunter"""
    employer_dict = {}
    employers_data = []
    vacancies_emp = []
    vacancies_emp_dicts = []

    def __init__(self, employer):
        self.employer = employer

    def get_employer(self):
        url = 'https://api.hh.ru/employers'
        params = {'text': {self.employer}, "areas": 113, 'per_page': 20}
        response = requests.get(url, params=params)
        employer = response.json()
        if employer is None:
            return "Данные не получены"
        elif 'items' not in employer:
            return "Нет указанных работодателей"
        else:
            employer_dict = {'id': employer['items'][0]['id'], 'name': employer['items'][0]['name'],
                             'alternate_url': employer['items'][0]['alternate_url']}
            self.employer_dict = employer_dict
            self.employers_data.append(employer_dict)
            return self.employer_dict

        # for num in range(
        #         50):
        #     url = 'https://api.hh.ru/employers'
        #     params = {'text': {self.employer}, "areas": 113, 'per_page': 20}
        #     response = requests.get(url, params=params)
        #     employer = response.json()
        #     if employer is None:
        #         return "Данные не получены"
        #     elif 'items' not in employer:
        #         return "Нет указанных работодателей"
        #     else:
        #         self.employer_data['id'] = employer['items'][0]['id']
        #         self.employer_data['name'] = employer['items'][0]['name']
        #         self.employer_data['alternate_url'] = employer['items'][0]['alternate_url']
        #     return self.employer_data

    def __get_page_vacancies(self, employer_id, page):
        self.employer_id = employer_id
        params = {
            'employer_id': employer_id,
            'area': 113,
            'per_page': 100,
            'page': page
        }
        response = requests.get('https://api.hh.ru/vacancies', params)
        data = response.content.decode()
        response.close()
        return data

    def get_vacancies(self, employer_id):
        for page in range(2):
            vacancies = json.loads(self.__get_page_vacancies(employer_id, page))
            for vacancy in vacancies['items']:
                if vacancy['salary'] is None:
                    vacancy['salary'] = {}
                    vacancy['salary']['from'] = "не указано"
                    vacancy['salary']['to'] = "не указано"
                self.vacancies_emp.append(
                    [vacancy['id'], vacancy['name'], vacancy['apply_alternate_url'],
                     vacancy['salary']['from'], vacancy['salary']['to']])

        for vacancy in self.vacancies_emp:
            vacancy_dict = {'id': vacancy[0], 'vacancy': vacancy[1], 'url': vacancy[2],
                            'salary_from': vacancy[3], 'salary_to': vacancy[4],
                            'employer': self.employer_dict['id']}
            if vacancy_dict['salary_from'] is None:
                vacancy_dict['salary_from'] = 0
            elif vacancy_dict['salary_to'] is None:
                vacancy_dict['salary_to'] = vacancy_dict['salary_from']
            self.vacancies_emp_dicts.append(vacancy_dict)
        return self.vacancies_emp_dicts

#
# hh = HH('Skyeng')
# emp = hh.get_employer()
# print(emp)
# vacancies = hh.get_vacancies(emp['id'])
# for vacancy in vacancies:
#     print(vacancy)
