DROP TABLE IF EXISTS profiles;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS roles;

CREATE TABLE profiles (
	id                   integer NOT NULL  PRIMARY KEY autoincrement,
	profile              text NOT NULL
 );

CREATE TABLE products (
	id                   integer NOT NULL  PRIMARY KEY autoincrement,
	name                 varchar(100) NOT NULL,
	price                double precision(4,2),
	description          text,
	image                text,
	id_category          integer,
	FOREIGN KEY ( id_category ) REFERENCES product_categories( id )
 );

CREATE TABLE roles (
	id                   integer NOT NULL  PRIMARY KEY,
	name                 varchar(100) NOT NULL
);

CREATE TABLE users (
	id                   integer NOT NULL  PRIMARY KEY autoincrement,
	username             varchar(100) NOT NULL UNIQUE,
	password             varchar(100) NOT NULL,
	id_profile           integer NOT NULL,
	id_role              integer NOT NULL,
	FOREIGN KEY ( id_role ) REFERENCES roles( id ),
	FOREIGN KEY ( id_profile ) REFERENCES profiles( id )
 );

CREATE TABLE orders (
	id                      integer NOT NULL  PRIMARY KEY autoincrement,
	id_profile              integer NOT NULL,
	FOREIGN KEY ( id_profile ) REFERENCES profiles( id)
);

CREATE TABLE baskets (
	id                     integer NOT NULL  PRIMARY KEY autoincrement,
	id_order               integer NOT NULL,
	id_product             integer NOT NULL,
	FOREIGN KEY ( id_order ) REFERENCES orders( id ),
	FOREIGN KEY ( id_product ) REFERENCES products( id )
);


CREATE TABLE product_categories (
	id                     integer NOT NULL  PRIMARY KEY autoincrement,
	name                   varchar(100) NOT NULL,
	label                  varchar(100) NOT NULL
);
