use db;

insert into person 
    (person_id, login, first_name, last_name, email, password) values
    (1, 'taya', 'Taya', 'Penskaya', 'taya@mail.com', 'kuku'),
    (2, 'alex', 'Alex', 'Smirnov', 'alex@mail.com', '2345');

insert into  person (person_id, login, first_name, last_name, email, password) values (3, 'sof', 'Sofia', 'Povarova', 'sss@mail.com', 'sss');
insert into  person (person_id, login, first_name, last_name, email, password) values (4, 'alyo', 'Alyona', 'Antonova', 'alyo@mail.com', 'alyo');
insert into  person (person_id, login, first_name, last_name, email, password) values (5, 'nadya', 'Nadya', 'Gorokhova', 'nad@mail.com', 'nadya');

insert into destination
    (dest_id, dest_name) values
    (1, 'Amsterdam'),
    (2, 'London'),
    (3, 'New York'),
    (4, 'Saint Petersburg'), 
    (5, 'Limassol'),
    (6, 'Belgrade'),
    (7, 'Kostroma');

insert into route
    (route_id, start_point_id, end_point_id) values
    (1, 4, 1),
    (2, 6, 2),
    (3, 7, 4), 
    (4, 5, 4),
    (5, 7, 3),
    (6, 3, 6);

insert into trip
    (trip_id, route_id, trip_date) values
    (1, 1, '2022-05-21'),
    (2, 6, '2022-07-15'),
    (3, 4, '2022-09-01'),
    (4, 5, '2022-02-27'),
    (5, 2, '2022-10-07'),
    (6, 3, '2022-12-12');

insert into person_trip
    (person_id, trip_id) values
    (2, 1),
    (1, 5);