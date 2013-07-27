-- Initial script for mysql

-- /usr/bin/mysql -uroot -p

-- CREATE DATABASE wj CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
use wj;

-- ############################### CREATE TABLE #############################################
CREATE TABLE if not exists expenses(
       expenseid bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'pk',
       userid VARCHAR(50) NOT NULL,
       source_expenseid VARCHAR(50),
       amount float,
       category VARCHAR(50),
       -- date TIMESTAMP NOT NULL DEFAULT NOW(),
       date VARCHAR(50),
       createtime VARCHAR(50),
       branding VARCHAR(50),
       latitude FLOAT,
       LONGITUDE FLOAT,
       NOTES VARCHAR(200),
       memo VARCHAR(200),
       primary key(expenseid)
);
CREATE INDEX expense_date_index ON expenses (date) USING BTREE;

-- userprofile table's schema may be changed all the times
CREATE TABLE if not exists userprofile(
       username VARCHAR(50) NOT NULL,
       service_name VARCHAR(50) NOT NULL,
       nickname VARCHAR(50) NOT NULL,
       gender int,
       primary key(username, service_name)
);

-- ###########################################################################################