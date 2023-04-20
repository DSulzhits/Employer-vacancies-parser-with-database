from fill_DB.fill_database import FillDB
from db_manager.db_manager import DBManager


def main():
    """Код для проверки работоспособности программы"""
    employers = ['skyeng', 'skillbox', 'лаборатория касперского', 'lesta games', 'Вконтакте', 'LG Electronics Inc.',
                 'SberTech', 'YADRO', 'Доктор Веб', 'GeekBrains']
    fill_db = FillDB(employers)
    fill_db.fill_db_employers()
    fill_db.fill_db_vacancies()

    db_manager = DBManager
    data = db_manager.get_companies_and_vacancies_count()
    for d in data:
        print(d)
    all_info = db_manager.get_all_vacancies()
    for info in all_info:
        print(info)
    salary = db_manager.get_avg_salary()
    print(salary)
    top_salary = db_manager.get_vacancies_with_higher_salary()
    for top in top_salary:
        print(top)
    vacancies = db_manager.get_vacancies_with_keyword("Python")
    for vac in vacancies:
        print(vac)


if __name__ == "__main__":
    main()
