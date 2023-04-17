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
        """Метод для получения информации по работодателю"""
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

    def __get_page_vacancies(self, employer_id, page):
        """Метод для получения всех вакансий исходя из id работодателя"""
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
        """Метод для обработки полученной информации по вакансиям
        range можно задать в любой, но я задал 2 чтобы было быстрее"""
        for page in range(2):
            vacancies_data = json.loads(self.__get_page_vacancies(employer_id, page))
            for vacancy_data in vacancies_data['items']:
                if vacancy_data['salary'] is None:
                    vacancy_data['salary'] = {}
                    vacancy_data['salary']['from'] = "не указано"
                    vacancy_data['salary']['to'] = "не указано"

                vacancy_dict = {'id': vacancy_data['id'], 'vacancy': vacancy_data['name'],
                                'url': vacancy_data['apply_alternate_url'],
                                'salary_from': vacancy_data['salary']['from'],
                                'salary_to': vacancy_data['salary']['to'],
                                'employer_id': self.employer_dict['id']}
                if vacancy_dict['salary_from'] is None:
                    vacancy_dict['salary_from'] = "не указано"
                elif vacancy_dict['salary_to'] is None:
                    vacancy_dict['salary_to'] = vacancy_dict['salary_from']
                self.vacancies_emp_dicts.append(vacancy_dict)
        return self.vacancies_emp_dicts


# hh = HH('Skyeng')
# emp = hh.get_employer()
# print(emp)
# vacancies = hh.get_vacancies(emp['id'])
# print(len(vacancies))
# for vacancy_hh in vacancies:
#     print(vacancy_hh)
