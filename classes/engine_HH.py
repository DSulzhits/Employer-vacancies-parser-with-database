import json
import requests


class HH:
    """Класс для доступа к API HeadHunter"""
    employer_data = {}
    vacancies_emp = []
    vacancies_emp_dicts = []

    def __init__(self, employer):
        self.employer = employer

    def get_request(self):
        """Метод для отправки запроса на HeadHunter проводит необходимые проверки,
        записывает полученную информацию в .json файл,
        возвращает словари для последующей работы с ними.
        """

        for num in range(
                50):  # при значении 50 выбирает из 1000 вакансий те в которых есть информация о З/П и она в RUR
            url = 'https://api.hh.ru/employers'
            params = {'text': {self.employer}, "areas": 113, 'per_page': 20}
            response = requests.get(url, params=params)
            employer = response.json()
            if employer is None:
                return "Данные не получены"
            elif 'items' not in employer:
                return "Нет указанных работодателей"
            else:
                self.employer_data['id'] = employer['items'][0]['id']
                self.employer_data['name'] = employer['items'][0]['name']
                self.employer_data['alternate_url'] = employer['items'][0]['alternate_url']
            return self.employer_data

    def get_page_vacancies(self, page):
        employer_id = self.employer_data['id']
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

    def get_vacancies(self):
        for page in range(2):
            vacancies = json.loads(self.get_page_vacancies(page))
            for vacancy in vacancies['items']:
                if vacancy['salary'] is None:
                    vacancy['salary'] = {}
                    vacancy['salary']['from'] = "не указано"
                    vacancy['salary']['to'] = "не указано"
                self.vacancies_emp.append(
                    [vacancy['name'], vacancy['apply_alternate_url'], vacancy['snippet']['requirement'],
                     vacancy['salary']['from'], vacancy['salary']['to']])

        for vacancy in self.vacancies_emp:
            vacancy_dict = {'name': vacancy[0], 'url': vacancy[1], 'requirement': vacancy[2],
                            'salary_from': vacancy[3], 'salary_to': vacancy[4]}
            if vacancy_dict['salary_from'] is None:
                vacancy_dict['salary_from'] = 0
            elif vacancy_dict['salary_to'] is None:
                vacancy_dict['salary_to'] = vacancy_dict['salary_from']
                try:
                    if "<highlighttext>" and "</highlighttext>" in vacancy_dict['requirement']:
                        vacancy_dict['requirement'] = vacancy_dict['requirement'].replace("<highlighttext>", "")
                        vacancy_dict['requirement'] = vacancy_dict['requirement'].replace("</highlighttext>", "")
                except TypeError:
                    vacancy_dict['requirement'] = vacancy_dict['requirement']
            self.vacancies_emp_dicts.append(vacancy_dict)
        return self.vacancies_emp_dicts
