CREATE TABLE employers
(
	employer_id int PRIMARY KEY,
	employer_name varchar(100),
	eployer_url varchar(200)
);

CREATE TABLE vacancies
(
	vacancy_id int PRIMARY KEY,
	vacancy_name varchar(100),
	vacancy_url varchar(200),
	vacancy_salary_from varchar(50),
	vacancy_salary_to varchar(50),
	employer_id int REFERENCES employers(employer_id)
);