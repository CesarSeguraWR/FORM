CREATE DATABASE formulario;
USE formulario;
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    rol tinyint(20) NOT NULL,
    UNIQUE (rol)
);
CREATE USER 'rooty'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON formulario.* TO 'rooty'@'localhost' IDENTIFIED BY 'password';
FLUSH PRIVILEGES;
