-- Initial script for mysql

-- mysql -uroot -p
--  CREATE DATABASE index_db CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
--  CREATE USER user_2013;
--  SET PASSWORD FOR user_2013 = PASSWORD("ilovechina");
--  GRANT ALL PRIVILEGES ON index_db.* TO "user_2013"@"%" IDENTIFIED BY "ilovechina";
--  FLUSH PRIVILEGES;
--  EXIT;

use index_db;

drop table usertext;
drop table userevent;
drop table userprofile;
drop table serviceprofile;

-- ############################### CREATE TABLE #############################################
CREATE TABLE if not exists usertext(
       id bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'pk',
       from_username VARCHAR(50) NOT NULL,
       to_username VARCHAR(50) NOT NULL,
       createtime int,
       content VARCHAR(1000) NOT NULL,
       msgid VARCHAR(50) NOT NULL,
       memo VARCHAR(200),
       primary key(id)
);

CREATE INDEX user_text_index ON usertext (from_username, to_username) USING BTREE;

CREATE TABLE if not exists userevent(
       id bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT 'pk',
       from_username VARCHAR(50) NOT NULL,
       to_username VARCHAR(50) NOT NULL,
       createtime int,
       event VARCHAR(50) NOT NULL,
       eventkey VARCHAR(50) NOT NULL,
       memo VARCHAR(200),
       primary key(id)
);
CREATE INDEX user_event_index ON userevent (from_username, to_username) USING BTREE;

CREATE TABLE if not exists userprofile(
       username VARCHAR(50) NOT NULL,
       service_name VARCHAR(50) NOT NULL,
       index_key VARCHAR(100) NOT NULL,
       index_value VARCHAR(100) NOT NULL,
       memo VARCHAR(200),
       primary key(username, service_name, index_key)
);

CREATE TABLE if not exists serviceprofile(
       service_name VARCHAR(50) NOT NULL,
       index_key VARCHAR(100) NOT NULL,
       index_value VARCHAR(100) NOT NULL,
       memo VARCHAR(200),
       primary key(service_name, index_key)
);

-- ###########################################################################################