CREATE SCHEMA IF NOT EXISTS onlinerest;

CREATE TABLE onlinerest.users (
user_id BIGINT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(100),
address VARCHAR(100),
city VARCHAR(100),
phonenumber VARCHAR(100),
email VARCHAR(100),
password VARCHAR(100),
delivery_location_latitude FLOAT(6),
delivery_location_longitude FLOAT(6)
);

CREATE TABLE onlinerest.orders (
order_id BIGINT AUTO_INCREMENT PRIMARY KEY,
user_id VARCHAR(20),
ordertotal FLOAT(2),
paymentmethod VARCHAR(20),
order_date DATE,
time_ordered TIME,
time_order_picked TIME
);

CREATE TABLE onlinerest.orderitems (
order_id BIGINT,
item_name VARCHAR(200),
quantity INT
);

CREATE TABLE onlinerest.restaurants{
Restaurant_ID INT,
Restaurant_latitude FLOAT(6),
Restaurant_longitude FLOAT(6),
City_Name VARCHAR(100),
Driver_ID INT,
Delivery_person_Age INT,
Delivery_person_Ratings FLOAT(1),
Delivery_person_ID VARCHAR(100));

CREATE TABLE onlinerest.feedback (
order_id BIGINT,
user_id BIGINT,
delivery_rating FLOAT(1),
food_rating FLOAT(1));
