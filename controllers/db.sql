create table admin(
    user varchar(50),
    contraseña varchar(50)
);

create table users(    
    user varchar(50),
    cedula varchar(100),
    contraseña varchar(50),
    PRIMARY KEY (cedula)
);

create table clientes(
    nombre varchar(100),
    apellido varchar(100),
    cedula int,
    dirección varchar(200),
    telefono int(20),
    correo varchar(100),
    PRIMARY KEY (cedula)
);

create table productos(
    id_producto int auto_increment,
    nombre varchar(100), -- debe incluir la talla camisa manga largar tallaXXL
    precio decimal(10,2),
    color varchar(50),
    imagen varchar(100),
    cantidad int,
    PRIMARY KEY (id_producto)
);

create table venta(
    id_venta int,
    n_cliente varchar(50),
    n_apellido varchar(50),
    dirección varchar (100),
    cedula int,
    fecha date,
    n_productos varchar(100),
    color varchar(50),
    cantidad int,
    precio float(10,2),
    resultado float(10,2),
    total decimal(10,2),
    PRIMARY KEY (id_venta),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
)
