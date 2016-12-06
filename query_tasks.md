# 1. Описание таблиц

База данных межпланетных экспедиций. Экспедиции (таблица Missions) отправляется к определенной планете. Перечень планет находится в таблице Planets. Для каждой экспедиции формируется экпипаж (таблица Crew). Экспедиция характеризуется также временами начала и окончания: атрибуты start и finish соответственно. Символом # отмечены атрибуты, являющиеся внешним ключом.

Описание таблиц:
Planets(id, name, type)
Humans(id, name, specialization, age)
Missions(id, #planet, description, finished, start, finish)
Crew(id, #mission, #human)

# 2. Задания

**1. Вывести общее количество миссий.**
```
SELECT COUNT(*)
FROM Missions;
```
**2. Вывести количество активных миссий.**
```
SELECT COUNT(*)
FROM Missions
WHERE finished = 0;
```
**3. Найти планеты (вывести id, имя) к которым не было отправлено ни одной миссии.**
```
SELECT id, name
FROM Planets
WHERE Planets.id NOT IN (
    SELECT planet
    FROM Missions);
```
**4. Найти планеты (вывести id, имя) к которым было отправлено больше всего миссий.**
```
SELECT Planets.id, Planets.name
COUNT(Missions.planet) AS NumberOfMissionsToPlanet
FROM Missions
JOIN Planets
ON Missions.planet = Planets.id
GROUP BY Planets.id;
ORDER BY NumberOfMissionsToPlanet DESC;
```
**5. Вывести перечень людей (id, имя, специализация), которые не участвуют ни в одной из миссий.**
```
SELECT id, name, specialization
FROM Humans
WHERE Humans.id NOT IN (
    SELECT human
    FROM Crew
    WHERE Crew.mission IN (
       SELECT id
       FROM Missions));
```
**6. Вывести перечень людей (id, имя, специализация), которые участвуют в одной из миссий.**
```
SELECT id, name, specialization
FROM Humans
WHERE Humans.id IN (
    SELECT human
    FROM Crew
    WHERE Crew.mission IN (
       SELECT id
       FROM Missions));
```
**7. Вывести экипажи миссий отправлявшихся к планете X.**
```
SELECT *
FROM Crew
JOIN Missions
ON Crew.mission = Missions.id
WHERE Missions.planet = (
    SELECT id
    FROM Planets
    WHERE Planets.name = "X");
```
**8. Вывести экипажи миссий, которые не летали по крайней мере 1 год.**
```
SELECT *
FROM Crew
JOIN Missions
ON Crew.mission = Missions.id
WHERE
    (Mission.finished = 1 AND (NOW - Mission.finish) > 1 YEAR)
    OR
    (Mission.finished = 0 AND (NOW - Mission.start) > 1 YEAR);
```
**9. Подсчитать количество людей участвовавших в каждой из миссиий (вывести id миссии, название миссии, кол-во человек).**
```
SELECT Missions.id, Missions.name
FROM Missions
JOIN Crew
ON Missions.id = Crew.mission
COUNT(Crew.human)
GROUP BY Missions.id;
```