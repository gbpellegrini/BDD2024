-- Tabla Productos
INSERT INTO PRODUCTOS (Nombre, Precio, Categoria) VALUES
    ('Producto A', 29.99, 'Categoría 1'),
    ('Producto B', 49.50, 'Categoría 2'),
    ('Producto C', 15.00, 'Categoría 1'),
    ('Producto D', 99.99, 'Categoría 3'),
    ('Producto E', 19.99, 'Categoría 2');

-- Tabla Competencia de Precios
INSERT INTO COMPRETENCIA_PRECIOS (NombreProducto, PrecioCompetencia, Categoria) VALUES
    ('Producto A', 25.00, 'Categoría 1'),
    ('Producto B', 45.00, 'Categoría 2'),
    ('Producto C', 20.00, 'Categoría 1'),
    ('Producto D', 95.00, 'Categoría 3'),
    ('Producto E', 18.00, 'Categoría 2');
