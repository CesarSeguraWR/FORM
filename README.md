CREATE DATABASE formulario_db;

USE formulario_db;

CREATE TABLE contactos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL
);
