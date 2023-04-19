from fill_DB.fill_database import FillDB


def main():
    employers = ['skyeng', 'skillbox', 'лаборатория касперского', 'lesta games', 'Вконтакте', 'LG Electronics Inc.',
                 'SberTech', 'YADRO', 'Доктор Веб', 'GeekBrains']
    fill_db = FillDB(employers)
    fill_db.fill_db_employers()
    fill_db.fill_db_vacancies()


if __name__ == "__main__":
    main()
