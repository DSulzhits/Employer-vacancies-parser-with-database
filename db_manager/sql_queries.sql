SELECT employer_name, COUNT(vacancies) AS vacancy_count
FROM employers
INNER JOIN vacancies
USING(employer_id)
GROUP BY employer_name
ORDER BY vacancy_count DESC

SELECT employer_name, vacancy_name, vacancy_salary_from, vacancy_salary_to, vacancy_url
FROM employers
INNER JOIN vacancies
USING(employer_id)
WHERE vacancy_salary_from IS NOT null
ORDER BY vacancy_salary_from DESC



select * from vacancies

CREATE TABLE vacancies
(
	vacancy_id int PRIMARY KEY,
	vacancy_name varchar(100),
	vacancy_url varchar(200),
	vacancy_salary_from int,
	vacancy_salary_to int,
	employer_id int REFERENCES employers(employer_id)
);

SELECT * FROM vacancies
WHERE vacancy_salary_from IS NOT null

SELECT * FROM vacancies
WHERE vacancy_name LIKE '%Python%'

SELECT vacancy_name, vacancy_salary_from
FROM vacancies
WHERE vacancy_salary_from > (SELECT AVG(vacancy_salary_from) FROM vacancies)

SELECT ROUND(min(vacancy_salary_from))
FROM vacancies
WHERE vacancy_salary_from IS NOT null
