-- create database
create database if not exists BookStore;

--create users table 
create table if not exists users(user_id int primary key auto_increment, name varchar(30), surname varchar(30),
email varchar(50), password varchar(30))

--create books table 
create table if not exists books(book_id int primary key auto_increment, bk_name varchar(30), authour varchar(30),
price int)

--create orders table 
create table if not exists orders(order_id int primary key auto_increment, book_id int, units int)

-- insert users
insert into users(name, surname, email, password) values(%s, %s, %s, %s)

-- insert books 
insert into books(bk_name, authour, price) values(%s, %s, %s)

-- insert orders
insert into orders(book_id, units) values(%s, %s)

