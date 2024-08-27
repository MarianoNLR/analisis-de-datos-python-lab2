create database lab2_analisis_datos;

use lab2_analisis_datos;

#Tabla de productos
CREATE TABLE productos (
	codigo_producto varchar(255) NOT NULL,
    nombre varchar(255) NOT NULL,
    precio decimal NOT NULL,
    stock int NOT NULL,
    marca varchar(255) NOT NULL,
    categoria varchar(255) NOT NULL,
    PRIMARY KEY (codigo_producto)
);

#Tabla de productos alimenticios
CREATE TABLE productos_alimenticios (
	codigo_producto varchar(255) NOT NULL,
	fecha_vencimiento date NOT NULL,
    es_libre_gluten boolean NOT NULL,
    PRIMARY KEY (codigo_producto),
    FOREIGN KEY (codigo_producto) REFERENCES productos(codigo_producto) 
);

#Tabla de producto electronicos
CREATE TABLE productos_electronicos (
	codigo_producto varchar(255) NOT NULL,
    color varchar(255) NOT NULL,
    meses_garantia int NOT NULL,
    PRIMARY KEY (codigo_producto),
    FOREIGN KEY (codigo_producto) REFERENCES productos(codigo_producto)
);









