import requests


# import json


class HH:
    """Класс для доступа к API HeadHunter"""
    employers_all = []
    employer_data = {}
    employers_dicts = []

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

    def get_vacancies(self):
        params = {
            'employer_id': self.employer_data['id'],
            'area': 113,
            'per_page': 100
        }
        response = requests.get('https://api.hh.ru/vacancies', params)
        vacancies = response.json()
        if vacancies is None:
            return "Данные не получены"
        elif 'errors' in vacancies:
            return vacancies['errors'][0]['value']
        return vacancies
        #
        # for page in range(20):
        #     vacancy =
        # for employer in range(20):
        #     self.employer.append(employer)
        #             if info['items'][vacancy]['salary'] is not None \
        #                     and info['items'][vacancy]['salary']['currency'] == "RUR"\
        #                     and info['items'][vacancy]['employer']['name'] == self.company:
        #                 self.vacancies.append([info['items'][vacancy]['employer']['name'],
        #                                        info['items'][vacancy]['name'],
        #                                        info['items'][vacancy]['apply_alternate_url'],
        #                                        info['items'][vacancy]['snippet']['requirement'],
        #                                        info['items'][vacancy]['salary']['from'],
        #                                        info['items'][vacancy]['salary']['to']])
        # for vacancy in self.vacancies:
        #     vacancy_dict = {'employer': vacancy[0], 'name': vacancy[1], 'url': vacancy[2], 'requirement': vacancy[3],
        #                     'salary_from': vacancy[4], 'salary_to': vacancy[5]}
        #     if vacancy_dict['salary_from'] is None:
        #         vacancy_dict['salary_from'] = 0
        #     elif vacancy_dict['salary_to'] is None:
        #         vacancy_dict['salary_to'] = vacancy_dict['salary_from']
        #     try:
        #         if "<highlighttext>" and "</highlighttext>" in vacancy_dict['requirement']:
        #             vacancy_dict['requirement'] = vacancy_dict['requirement'].replace("<highlighttext>", "")
        #             vacancy_dict['requirement'] = vacancy_dict['requirement'].replace("</highlighttext>", "")
        #     except TypeError:
        #         vacancy_dict['requirement'] = vacancy_dict['requirement']
        #
        #     self.vacancies_dicts.append(vacancy_dict)
        #
        # with open(f'{self.vacancy}_hh_ru.json', 'w', encoding='UTF-8') as file:
        #     json.dump(self.vacancies_dicts, file, indent=2, ensure_ascii=False)
        # print(f"Отбор осуществляется из {len(self.vacancies_all)} вакансий (проверка обращения к сервису)")


hh = HH('Skillbox')
hh_emp = hh.get_request()
hh_vac = hh.get_vacancies()
print(hh_emp)
print(hh_vac)
