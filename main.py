from classes.engine_HH import HH


def main():
    employers = ['skyeng', 'skillbox', 'лаборатория касперского', 'lesta games', 'VK', 'LG Electronics Inc.',
                 'SberTech', 'YADRO', 'Доктор Веб', 'GeekBrains']
    for employer in employers:
        employer_info = HH(employer)
        employer_info.get_employer()
        for vacancy_dict in HH.employers_data:
            vacancies = employer_info.get_vacancies(vacancy_dict['id'])
            for vacancy in vacancies:
                print(vacancy)
        break


if __name__ == "__main__":
    main()
