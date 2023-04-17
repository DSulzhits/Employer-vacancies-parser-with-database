from fill_DB.fill_database import fill_employers_db


def main():
    employers = ['skyeng', 'skillbox', 'лаборатория касперского', 'lesta games', 'VK', 'LG Electronics Inc.',
                 'SberTech', 'YADRO', 'Доктор Веб', 'GeekBrains']
    fill_employers_db(employers)


if __name__ == "__main__":
    main()
