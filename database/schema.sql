DROP TABLE IF EXISTS profiles;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users;

CREATE TABLE profiles (
	id                   integer NOT NULL  PRIMARY KEY autoincrement,
	profile              text NOT NULL
 );

CREATE TABLE products (
	id                   integer NOT NULL  PRIMARY KEY autoincrement,
	name                 varchar(100) NOT NULL,
	price                double precision(4,2),
	description          text,
	image                text
 );

CREATE TABLE users (
	id                   integer NOT NULL  PRIMARY KEY autoincrement,
	username             varchar(100) NOT NULL UNIQUE,
	password             varchar(100) NOT NULL,
	id_profile           integer NOT NULL,
	FOREIGN KEY ( id_profile ) REFERENCES profiles( id )
 );
