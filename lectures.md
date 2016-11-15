# Базы данных

## Содержание
* [13.09.2016<br>Проектирование БД](#13092016Проектирование-бд)
* [15.11.2016<br>Работа с таблицами SQL](#15112016Работа-с-таблицами-sql)

## 13.09.2016<br>Проектирование БД

* анализ предметной области
    * текстовое описание
* создание модели предметной области
    * как сущности связаны между собой
* создание модели БД
* создание БД

## 15.11.2016<br>Работа с таблицами SQL

### Пример БД студентов
Students(id, name, group)<br>
Grades(student, grade)<br>
Groups(id, number)<br>

#### Запросы
Найти максимальную оценку:
```
SELECT GRADE
FROM GRADES
ORDER BY GRADE DESC
LIMIT 1;
```
или то же самое другим способом:
```
SELECT MAX(GRADE)
FROM GRADES;
```

```
SELECT *
FROM GRADES
JOIN STUDENTS
ON student = STUDENTS.id;
```
Результат -- R(#student, grade, name, group)

```
SELECT MAX(GRADE) group
FROM GRADES
JOIN STUDENTS
ON student = STUDENTS.id
GROUP BY group;
```
Выбрать пары студент -- название группы
```
SELECT NAME, Number
FROM STUDENTS
JOIN GROUPS
ON group = groups.id;
```
Выбрать студентов, у которых оченки ниже средней
```
SELECT *
FROM STUDENTS
JOIN GRADES
ON id = student;
WHERE grade >
    ( SELECT AVG(grade)
       FROM GRADES );
```
Найти студентов с заданным именем
```
SELECT *
FROM GRADES
WHERE name LIKE '%Николай%';
```