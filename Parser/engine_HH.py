import requests
import json


class HH:
    """Класс для доступа к API HeadHunter"""
    vacancies_all = []
    vacancies = []
    vacancies_dicts = []

    def __init__(self, vacancy):
        self.vacancy = vacancy

    def get_request(self):
        """Метод для отправки запроса на HeadHunter проводит необходимые проверки,
        записывает полученную информацию в .json файл,
        возвращает словари для последующей работы с ними.
        """

        for num in range(
                50):  # при значении 50 выбирает из 1000 вакансий те в которых есть информация о З/П и она в RUR
            url = 'https://api.hh.ru/vacancies'
            params = {'text': {self.vacancy}, "areas": 113, 'per_page': 20, 'page': num}
            response = requests.get(url, params=params)
            info = response.json()
            if info is None:
                return "Данные не получены"
            elif 'errors' in info:
                return info['errors'][0]['value']
            elif 'items' not in info:
                return "Нет вакансий"
            else:
                for vacancy in range(20):
                    self.vacancies_all.append(
                        vacancy)  # добавлено для проверки количества полученных вакансий до отбора
                    if info['items'][vacancy]['salary'] is not None \
                            and info['items'][vacancy]['salary']['currency'] == "RUR":
                        self.vacancies.append([info['items'][vacancy]['employer']['name'],
                                               info['items'][vacancy]['name'],
                                               info['items'][vacancy]['apply_alternate_url'],
                                               info['items'][vacancy]['snippet']['requirement'],
                                               info['items'][vacancy]['salary']['from'],
                                               info['items'][vacancy]['salary']['to']])
        for vacancy in self.vacancies:
            vacancy_dict = {'employer': vacancy[0], 'name': vacancy[1], 'url': vacancy[2], 'requirement': vacancy[3],
                            'salary_from': vacancy[4], 'salary_to': vacancy[5]}
            if vacancy_dict['salary_from'] is None:
                vacancy_dict['salary_from'] = 0
            elif vacancy_dict['salary_to'] is None:
                vacancy_dict['salary_to'] = vacancy_dict['salary_from']
            self.vacancies_dicts.append(vacancy_dict)

        with open(f'{self.vacancy}_hh_ru.json', 'w', encoding='UTF-8') as file:
            json.dump(self.vacancies_dicts, file, indent=2, ensure_ascii=False)
        print(f"Отбор осуществляется из {len(self.vacancies_all)} вакансий (проверка обращения к сервису)")
        return self.vacancies_dicts
