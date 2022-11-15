drop database if exists db;
create database db;
use db;

create table person (
    person_id int not null auto_increment,
    login varchar(255),
    first_name varchar(255),
    last_name varchar(255),
    email varchar(255),
    password varchar(255),
    primary key (person_id)
);

create table destination (
    dest_id int not null auto_increment,
    dest_name varchar(255),
    primary key (dest_id)
);

create table route (
    route_id int not null auto_increment,
    start_point_id int,
    end_point_id int,
    primary key (route_id),
    foreign key (start_point_id) references destination(dest_id),
    foreign key (end_point_id) references destination(dest_id)
);

create table trip (
    trip_id int not null auto_increment,
    route_id int,
    trip_date date,
    primary key (trip_id),
    foreign key (route_id) references route(route_id)
);

create table person_trip (
    person_id int not null auto_increment,
    trip_id int,
    primary key (person_id, trip_id),
    foreign key (person_id) references person(person_id),
    foreign key (trip_id) references trip(trip_id)
);