CREATE TABLE address (
	id                   integer NOT NULL  PRIMARY KEY autoincrement ,
	address              text NOT NULL
 );

CREATE TABLE products (
	id                   integer NOT NULL  PRIMARY KEY autoincrement ,
	name                 varchar(100) NOT NULL    ,
	price                double precision(4,2)     ,
	description          text     ,
	image                text
 );

CREATE TABLE users (
	id                   integer NOT NULL  PRIMARY KEY autoincrement ,
	username             varchar(100) NOT NULL    ,
	password             varchar(100) NOT NULL    ,
	id_address           integer NOT NULL    ,
	FOREIGN KEY ( id_address ) REFERENCES address( id )
 );
