create database control_alquiler_Reych;
USE control_alquiler_Reych;


CREATE TABLE marca(
ID INT NOT NULL AUTO_INCREMENT,
Nombre VARCHAR(45) NOT NULL,
PRIMARY KEY(ID)
);
INSERT INTO `control_alquiler_Reych`.`marca` (`ID`, `Nombre`) VALUES ('1', 'MAZDA');
INSERT INTO `control_alquiler_Reych`.`marca` (`ID`, `Nombre`) VALUES ('2', 'TOYOTA');
INSERT INTO `control_alquiler_Reych`.`marca` (`ID`, `Nombre`) VALUES ('3', 'FORD');
INSERT INTO `control_alquiler_Reych`.`marca` (`ID`, `Nombre`) VALUES ('4', 'CHEVROLET');


CREATE TABLE modelo(
ID INT NOT NULL AUTO_INCREMENT,
Nombre VARCHAR(45) NOT NULL,
ID_Marca INT,
PRIMARY KEY(ID),
FOREIGN KEY(ID_Marca) REFERENCES marca(ID)
);

INSERT INTO `control_alquiler_Reych`.`modelo` (`Nombre`, `ID_Marca`) VALUES ('BT50', '1');
INSERT INTO `control_alquiler_Reych`.`modelo` (`Nombre`, `ID_Marca`) VALUES ('HILUX', '2');
INSERT INTO `control_alquiler_Reych`.`modelo` (`Nombre`, `ID_Marca`) VALUES ('TRITON', '3');
INSERT INTO `control_alquiler_Reych`.`modelo` (`Nombre`, `ID_Marca`) VALUES ('SILVERADO', '4');


CREATE TABLE vehiculo(
Placa VARCHAR(20) NOT NULL,
Color VARCHAR(45) NOT NULL,
Año YEAR NOT NULL,
ID_Marca INT NOT NULL,
PRIMARY KEY(Placa),
FOREIGN KEY(ID_Marca) REFERENCES marca(ID)
);

INSERT INTO `control_alquiler_Reych`.`vehiculo` (`Placa`,`Color`,`Año`,`ID_Marca`,`ID_Modelo`) VALUES ('AB928BQ','BLANCO',2012,1,1);
INSERT INTO `control_alquiler_Reych`.`vehiculo` (`Placa`,`Color`,`Año`,`ID_Marca`,`ID_Modelo`) VALUES ('AG851MM','VINOTINTO',2012,1,1);
INSERT INTO `control_alquiler_Reych`.`vehiculo` (`Placa`,`Color`,`Año`,`ID_Marca`,`ID_Modelo`) VALUES ('AH928FK','VINOTINTO',2012,1,1);
INSERT INTO `control_alquiler_Reych`.`vehiculo` (`Placa`,`Color`,`Año`,`ID_Marca`,`ID_Modelo`) VALUES ('AY698KG','BLANCO',2012,1,1);
INSERT INTO `control_alquiler_Reych`.`vehiculo` (`Placa`,`Color`,`Año`,`ID_Marca`,`ID_Modelo`) VALUES ('CD338ME','BLANCO',2012,1,1);
INSERT INTO `control_alquiler_Reych`.`vehiculo` (`Placa`,`Color`,`Año`,`ID_Marca`,`ID_Modelo`) VALUES ('CP592JK','AZUL',2012,1,1);
INSERT INTO `control_alquiler_Reych`.`vehiculo` (`Placa`,`Color`,`Año`,`ID_Marca`,`ID_Modelo`) VALUES ('DF736KD','BLANCO',2010,2,2);
INSERT INTO `control_alquiler_Reych`.`vehiculo` (`Placa`,`Color`,`Año`,`ID_Marca`,`ID_Modelo`) VALUES ('DI487FF','GRIS',2012,2,2);
INSERT INTO `control_alquiler_Reych`.`vehiculo` (`Placa`,`Color`,`Año`,`ID_Marca`,`ID_Modelo`) VALUES ('DK493MM','BLANCO',2010,2,2);
INSERT INTO `control_alquiler_Reych`.`vehiculo` (`Placa`,`Color`,`Año`,`ID_Marca`,`ID_Modelo`) VALUES ('EF838HW','GRIS',2012,2,2);
INSERT INTO `control_alquiler_Reych`.`vehiculo` (`Placa`,`Color`,`Año`,`ID_Marca`,`ID_Modelo`) VALUES ('GA195WV','BLANCO',2009,3,3);
INSERT INTO `control_alquiler_Reych`.`vehiculo` (`Placa`,`Color`,`Año`,`ID_Marca`,`ID_Modelo`) VALUES ('GG939LL','GRIS',2012,4,4);
INSERT INTO `control_alquiler_Reych`.`vehiculo` (`Placa`,`Color`,`Año`,`ID_Marca`,`ID_Modelo`) VALUES ('GI934KR','BLANCO',2009,3,3);
INSERT INTO `control_alquiler_Reych`.`vehiculo` (`Placa`,`Color`,`Año`,`ID_Marca`,`ID_Modelo`) VALUES ('GJ020PP','BLANCO',2009,3,3);
INSERT INTO `control_alquiler_Reych`.`vehiculo` (`Placa`,`Color`,`Año`,`ID_Marca`,`ID_Modelo`) VALUES ('GN043FI','BLANCO',2009,3,3);
INSERT INTO `control_alquiler_Reych`.`vehiculo` (`Placa`,`Color`,`Año`,`ID_Marca`,`ID_Modelo`) VALUES ('GP034GT','VINOTINTO',2014,4,4);
INSERT INTO `control_alquiler_Reych`.`vehiculo` (`Placa`,`Color`,`Año`,`ID_Marca`,`ID_Modelo`) VALUES ('GP582QW','BLANCO',2009,3,3);
INSERT INTO `control_alquiler_Reych`.`vehiculo` (`Placa`,`Color`,`Año`,`ID_Marca`,`ID_Modelo`) VALUES ('GQ442QQ','GRIS',2014,4,4);
INSERT INTO `control_alquiler_Reych`.`vehiculo` (`Placa`,`Color`,`Año`,`ID_Marca`,`ID_Modelo`) VALUES ('GT665GK','BLANCO',2009,3,3);
INSERT INTO `control_alquiler_Reych`.`vehiculo` (`Placa`,`Color`,`Año`,`ID_Marca`,`ID_Modelo`) VALUES ('GW772WW','GRIS',2014,4,4);

ALTER TABLE vehiculo ADD COLUMN ID_Modelo INT;
ALTER TABLE vehiculo ADD FOREIGN KEY (ID_Modelo) REFERENCES modelo(ID);


CREATE TABLE representante(
CI VARCHAR(20) NOT NULL,
nombre VARCHAR(45) NOT NULL,
apellido VARCHAR(45) NOT NULL,
PRIMARY KEY(CI)
);


CREATE TABLE contratista(
RIF VARCHAR(20) NOT NULL,
nombre VARCHAR(255) NOT NULL,
direccion VARCHAR(450) NOT NULL,
telefono INT UNSIGNED NOT NULL,
Representante_CI VARCHAR(20) NOT NULL,
PRIMARY KEY(RIF),
FOREIGN KEY(Representante_CI) REFERENCES representante(CI)
);


CREATE TABLE alquiler(
COD_Alquiler INT AUTO_INCREMENT,
Fecha DATETIME NOT NULL,
RIF_Empresa VARCHAR(20) NOT NULL,
Placa_Vehiculo VARCHAR(20) NOT NULL,
Fecha_Expiracion datetime,
PRIMARY KEY(COD_Alquiler),
FOREIGN KEY(RIF_Empresa) REFERENCES contratista(RIF),
FOREIGN KEY(Placa_Vehiculo) REFERENCES vehiculo(Placa)
);


CREATE TABLE mantenimiento (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Placa VARCHAR(10) NOT NULL,
    Fecha DATE NOT NULL,
    Kilometraje INT,
    Descripcion VARCHAR(255),
    Costo DECIMAL(10,2),
    FOREIGN KEY (Placa) REFERENCES vehiculo(Placa)
);


