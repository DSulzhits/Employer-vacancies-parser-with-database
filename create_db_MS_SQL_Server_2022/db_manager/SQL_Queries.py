def fill_employers(table_name, data_to_fill):
    QUERY = fr'''INSERT INTO {table_name} (employer_id, employer_name, employer_url)
                        VALUES 
                        ('{data_to_fill['id']}',
                         '{data_to_fill['name']}',
                         '{data_to_fill['alternate_url']}');'''

    return QUERY


def fill_vacancies(table_name, data_to_fill):
    QUERY = fr'''INSERT INTO {table_name} (vacancy_id, vacancy_name, vacancy_url, vacancy_salary_from, vacancy_salary_to, employer_id)
                        VALUES 
                        ('{data_to_fill['id']}',
                         '{data_to_fill['vacancy']}',
                         '{data_to_fill['url']}',
                         '{data_to_fill['salary_from']}',
                         '{data_to_fill['salary_to']}',
                         '{data_to_fill['employer_id']}');'''

    return QUERY
