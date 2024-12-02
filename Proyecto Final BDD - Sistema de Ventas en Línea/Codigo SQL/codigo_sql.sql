-- Creación de la tabla clientes
CREATE TABLE clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    telefono VARCHAR(20),
    direccion VARCHAR(255)
);


-- Creación de la tabla productos
CREATE TABLE productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    categoria VARCHAR(255),
    precio DECIMAL(10, 2),
    stock INT
);

-- Creación de la tabla ordenes
CREATE TABLE ordenes (
    id_orden INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT,
    id_producto INT,
    cantidad INT,
    fecha_orden DATE,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);

CREATE INDEX idx_cliente ON ordenes(id_cliente);  --Índice en la columna id_cliente de la tabla ordenes:
CREATE INDEX idx_producto ON ordenes(id_producto); --Índice en la columna id_producto de la tabla ordenes
CREATE INDEX idx_producto_nombre ON productos(nombre); --Índice en la columna nombre de la tabla productos


INSERT INTO clientes (nombre, email, telefono, direccion) 
VALUES 
    ('Juan Pérez', 'juan@example.com', '123456789', 'Calle Ficticia 123'),
    ('María López', 'maria@example.com', '987654321', 'Av. Principal 456'),
    ('Carlos Sánchez', 'carlos@example.com', '123123123', 'Calle Larga 789'),
    ('Ana García', 'ana@example.com', '321321321', 'Plaza Mayor 101'),
    ('Luis Martínez', 'luis@example.com', '555555555', 'Calle Nueva 202'),
    ('Sofía Torres', 'sofia@example.com', '666666666', 'Av. Libertad 303'),
    ('Miguel Fernández', 'miguel@example.com', '777777777', 'Calle Sol 404'),
    ('Laura Morales', 'laura@example.com', '888888888', 'Calle Luna 505'),
    ('Pedro Rojas', 'pedro@example.com', '999999999', 'Av. de la Paz 606'),
    ('Lucía Díaz', 'lucia@example.com', '101010101', 'Calle del Mar 707');


INSERT INTO productos (nombre, descripcion, categoria, precio, stock)
VALUES 
    ('Laptop', 'Laptop con 16GB de RAM', 'Electrónica', 1000.00, 50),
    ('Teclado', 'Teclado mecánico', 'Accesorios', 80.00, 100),
    ('Mouse', 'Mouse inalámbrico', 'Accesorios', 40.00, 200),
    ('Monitor', 'Monitor 24 pulgadas', 'Electrónica', 200.00, 70),
    ('Impresora', 'Impresora multifuncional', 'Oficina', 150.00, 30),
    ('Smartphone', 'Teléfono inteligente de última generación', 'Electrónica', 800.00, 40),
    ('Auriculares', 'Auriculares inalámbricos', 'Accesorios', 60.00, 150),
    ('Cámara', 'Cámara digital profesional', 'Fotografía', 1200.00, 20),
    ('Tablet', 'Tablet con 10 pulgadas', 'Electrónica', 500.00, 35),
    ('Disco duro', 'Disco duro externo 1TB', 'Accesorios', 100.00, 60);


-- Órdenes para Juan Pérez (Cliente 1)
INSERT INTO ordenes (id_cliente, id_producto, cantidad, fecha_orden)
VALUES
    (1, 1, 1, '2024-11-25'),
    (1, 2, 2, '2024-11-26'),
    (1, 3, 1, '2024-11-27'),
    (1, 4, 1, '2024-11-28'),
    (1, 5, 1, '2024-11-29'),
    (1, 6, 1, '2024-11-30'),
    (1, 7, 2, '2024-12-01'),
    (1, 8, 1, '2024-12-02'),
    (1, 9, 1, '2024-12-03'),
    (1, 10, 2, '2024-12-04');

-- Órdenes para María López (Cliente 2)
INSERT INTO ordenes (id_cliente, id_producto, cantidad, fecha_orden)
VALUES
    (2, 2, 1, '2024-11-25'),
    (2, 3, 2, '2024-11-26'),
    (2, 4, 1, '2024-11-27'),
    (2, 5, 1, '2024-11-28'),
    (2, 6, 1, '2024-11-29'),
    (2, 7, 1, '2024-11-30'),
    (2, 8, 1, '2024-12-01'),
    (2, 9, 2, '2024-12-02'),
    (2, 10, 1, '2024-12-03'),
    (2, 1, 1, '2024-12-04');

-- Órdenes para Carlos Sánchez (Cliente 3)
INSERT INTO ordenes (id_cliente, id_producto, cantidad, fecha_orden)
VALUES
    (3, 1, 1, '2024-11-25'),
    (3, 2, 2, '2024-11-26'),
    (3, 3, 3, '2024-11-27'),
    (3, 4, 1, '2024-11-28'),
    (3, 5, 2, '2024-11-29'),
    (3, 6, 1, '2024-11-30'),
    (3, 7, 1, '2024-12-01'),
    (3, 8, 2, '2024-12-02'),
    (3, 9, 1, '2024-12-03'),
    (3, 10, 1, '2024-12-04');

-- Órdenes para Ana García (Cliente 4)
INSERT INTO ordenes (id_cliente, id_producto, cantidad, fecha_orden)
VALUES
    (4, 1, 1, '2024-11-25'),
    (4, 3, 1, '2024-11-26'),
    (4, 4, 2, '2024-11-27'),
    (4, 5, 1, '2024-11-28'),
    (4, 6, 1, '2024-11-29'),
    (4, 7, 2, '2024-11-30'),
    (4, 8, 1, '2024-12-01'),
    (4, 9, 2, '2024-12-02'),
    (4, 10, 3, '2024-12-03'),
    (4, 2, 1, '2024-12-04');

-- Órdenes para Luis Martínez (Cliente 5)
INSERT INTO ordenes (id_cliente, id_producto, cantidad, fecha_orden)
VALUES
    (5, 2, 1, '2024-11-25'),
    (5, 4, 1, '2024-11-26'),
    (5, 5, 2, '2024-11-27'),
    (5, 6, 1, '2024-11-28'),
    (5, 7, 3, '2024-11-29'),
    (5, 8, 2, '2024-11-30'),
    (5, 9, 1, '2024-12-01'),
    (5, 10, 2, '2024-12-02'),
    (5, 3, 1, '2024-12-03'),
    (5, 1, 1, '2024-12-04');

-- Órdenes para Sofía Torres (Cliente 6)
INSERT INTO ordenes (id_cliente, id_producto, cantidad, fecha_orden)
VALUES
    (6, 10, 1, '2024-11-25'),
    (6, 9, 1, '2024-11-26'),
    (6, 8, 1, '2024-11-27'),
    (6, 7, 2, '2024-11-28'),
    (6, 6, 1, '2024-11-29'),
    (6, 5, 2, '2024-11-30'),
    (6, 4, 1, '2024-12-01'),
    (6, 3, 2, '2024-12-02'),
    (6, 2, 1, '2024-12-03'),
    (6, 1, 1, '2024-12-04');


-- Órdenes para Miguel Fernández (Cliente 7)
INSERT INTO ordenes (id_cliente, id_producto, cantidad, fecha_orden)
VALUES
    (7, 1, 2, '2024-11-25'),
    (7, 2, 3, '2024-11-26'),
    (7, 4, 2, '2024-11-27'),
    (7, 5, 1, '2024-11-28'),
    (7, 6, 1, '2024-11-29'),
    (7, 7, 1, '2024-11-30'),
    (7, 8, 1, '2024-12-01'),
    (7, 9, 2, '2024-12-02'),
    (7, 10, 2, '2024-12-03'),
    (7, 3, 1, '2024-12-04');

-- Órdenes para Laura Morales (Cliente 8)
INSERT INTO ordenes (id_cliente, id_producto, cantidad, fecha_orden)
VALUES
    (8, 9, 1, '2024-11-25'),
    (8, 8, 1, '2024-11-26'),
    (8, 7, 1, '2024-11-27'),
    (8, 6, 1, '2024-11-28'),
    (8, 5, 2, '2024-11-29'),
    (8, 4, 1, '2024-11-30'),
    (8, 3, 2, '2024-12-01'),
    (8, 2, 1, '2024-12-02'),
    (8, 1, 1, '2024-12-03'),
    (8, 10, 1, '2024-12-04');

-- Órdenes para Diego Ramírez (Cliente 9)
INSERT INTO ordenes (id_cliente, id_producto, cantidad, fecha_orden)
VALUES
    (9, 2, 2, '2024-11-25'),
    (9, 4, 1, '2024-11-26'),
    (9, 6, 1, '2024-11-27'),
    (9, 8, 2, '2024-11-28'),
    (9, 10, 1, '2024-11-29'),
    (9, 1, 1, '2024-11-30'),
    (9, 3, 3, '2024-12-01'),
    (9, 5, 2, '2024-12-02'),
    (9, 7, 1, '2024-12-03'),
    (9, 9, 1, '2024-12-04');

-- Órdenes para Carolina Vega (Cliente 10)
INSERT INTO ordenes (id_cliente, id_producto, cantidad, fecha_orden)
VALUES
    (10, 3, 1, '2024-11-25'),
    (10, 5, 1, '2024-11-26'),
    (10, 7, 1, '2024-11-27'),
    (10, 9, 1, '2024-11-28'),
    (10, 1, 1, '2024-11-29'),
    (10, 2, 2, '2024-11-30'),
    (10, 4, 1, '2024-12-01'),
    (10, 6, 2, '2024-12-02'),
    (10, 8, 1, '2024-12-03'),
    (10, 10, 1, '2024-12-04');

