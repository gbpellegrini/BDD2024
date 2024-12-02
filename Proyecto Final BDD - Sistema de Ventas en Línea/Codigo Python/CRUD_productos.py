import mysql.connector

# Conexión a la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="ventas"
)

cursor = conexion.cursor()

def agregar_producto(nombre, descripcion, categoria, precio, stock):
    """
    Agrega un producto a la base de datos.

    Args:
    - nombre (str): Nombre del producto.
    - descripcion (str): Descripción del producto.
    - categoria (str): Categoría del producto.
    - precio (float): Precio unitario del producto.
    - stock (int): Cantidad disponible en inventario.
    """
    try:
        # SQL para insertar el producto en la tabla productos
        sql = """
        INSERT INTO productos (nombre, descripcion, categoria, precio, stock)
        VALUES (%s, %s, %s, %s, %s)
        """
        valores = (nombre, descripcion, categoria, precio, stock)

        # Ejecutar la consulta
        cursor.execute(sql, valores)
        conexion.commit()

        print("Producto agregado con éxito.")
    except Exception as e:
        print(f"Error al agregar producto: {e}")
        conexion.rollback()

def obtener_productos():
    """
    Recupera todos los productos de la base de datos.

    Returns:
        list: Lista de tuplas con los datos de los productos.
              Cada tupla contiene (ID, Nombre, Descripción, Categoría, Precio, Stock).
    """
    global cursor
    try:
        sql = "SELECT * FROM productos;"
        cursor.execute(sql)
        productos = cursor.fetchall()
        return productos
    except Exception as e:
        print(f"Error al obtener productos: {e}")
        return []
    finally:
        # Asegurarse de recrear el cursor
        conexion.commit()
        if cursor:
            cursor.close()
        cursor = conexion.cursor()

def actualizar_producto(id_producto, nombre, descripcion, categoria, precio, stock):
    """
    Actualiza los datos de un producto en la base de datos.

    Args:
    - id_producto (int): ID del producto a actualizar.
    - nombre (str): Nuevo nombre del producto.
    - descripcion (str): Nueva descripción del producto.
    - categoria (str): Nueva categoría del producto.
    - precio (float): Nuevo precio del producto.
    - stock (int): Nueva cantidad en stock.
    """
    try:
        # SQL para actualizar el producto
        sql = """
        UPDATE productos
        SET nombre = %s, descripcion = %s, categoria = %s, precio = %s, stock = %s
        WHERE id_producto = %s
        """
        valores = (nombre, descripcion, categoria, precio, stock, id_producto)

        cursor.execute(sql, valores)
        conexion.commit()

        print("Producto actualizado con éxito.")
    except Exception as e:
        print(f"Error al actualizar producto: {e}")
        conexion.rollback()

def eliminar_producto(id_producto):
    try:
        # Asegúrate de que se usa el nombre correcto de la columna en la cláusula WHERE
        sql = "DELETE FROM productos WHERE id_producto = %s"
        cursor.execute(sql, (id_producto,))  # Pasamos el ID como tupla
        conexion.commit()
    except Exception as e:
        raise Exception(f"Error al eliminar producto: {e}")
    
def obtener_productos_mas_vendidos():
    """
    Recupera los productos más vendidos de la base de datos basándose en la cantidad total de productos vendidos
    (no solo el número de órdenes), sumando las cantidades en cada orden.

    Returns:
        list: Lista de tuplas con los datos de los productos más vendidos,
              ordenados de mayor a menor por la cantidad total vendida.
    """
    global cursor
    try:
        sql = """
        SELECT 
            p.id_producto, 
            p.nombre, 
            p.descripcion, 
            p.categoria, 
            p.precio, 
            p.stock, 
            SUM(o.cantidad) AS total_vendido
        FROM productos p
        JOIN ordenes o ON p.id_producto = o.id_producto
        GROUP BY p.id_producto, p.nombre, p.descripcion, p.categoria, p.precio, p.stock
        ORDER BY total_vendido DESC
        LIMIT 10;
        """
        cursor.execute(sql)
        productos = cursor.fetchall()
        return productos
    except Exception as e:
        print(f"Error al obtener productos más vendidos: {e}")
        return []
    finally:
        conexion.commit()
        # Asegurarse de cerrar y recrear el cursor
        if cursor:
            cursor.close()
        cursor = conexion.cursor()


def obtener_productos_menos_vendidos():
    """
    Recupera los productos menos vendidos de la base de datos basándose en la cantidad total de productos vendidos.
    
    Returns:
        list: Lista de tuplas con los datos de los productos menos vendidos, 
              ordenados de menor a mayor por la cantidad total vendida.
    """
    global cursor
    try:
        sql = """
        SELECT 
            p.id_producto, 
            p.nombre, 
            p.descripcion, 
            p.categoria, 
            p.precio, 
            p.stock, 
            IFNULL(SUM(o.cantidad), 0) AS total_vendido
        FROM productos p
        LEFT JOIN ordenes o ON p.id_producto = o.id_producto
        GROUP BY p.id_producto, p.nombre, p.descripcion, p.categoria, p.precio, p.stock
        ORDER BY total_vendido ASC
        LIMIT 10;
        """
        cursor.execute(sql)
        productos = cursor.fetchall()
        return productos
    except Exception as e:
        print(f"Error al obtener productos menos vendidos: {e}")
        return []
    finally:
        conexion.commit()
        # Asegurarse de cerrar y recrear el cursor
        if cursor:
            cursor.close()
        cursor = conexion.cursor()

def obtener_productos_con_mas_stock():
    """
    Recupera los productos con más stock de la base de datos.
    
    Returns:
        list: Lista de tuplas con los productos con más stock, 
              ordenados de mayor a menor stock.
    """
    global cursor
    try:
        sql = """
        SELECT 
            p.id_producto, 
            p.nombre, 
            p.descripcion, 
            p.categoria, 
            p.precio, 
            p.stock
        FROM productos p
        ORDER BY p.stock DESC
        LIMIT 10;
        """
        cursor.execute(sql)
        productos = cursor.fetchall()
        return productos
    except Exception as e:
        print(f"Error al obtener productos con más stock: {e}")
        return []
    finally:
        conexion.commit()
        # Asegurarse de cerrar y recrear el cursor
        if cursor:
            cursor.close()
        cursor = conexion.cursor()

def obtener_productos_con_menos_stock():
    """
    Recupera los productos con menos stock de la base de datos.
    
    Returns:
        list: Lista de tuplas con los productos con menos stock, 
              ordenados de menor a mayor stock.
    """
    global cursor
    try:
        sql = """
        SELECT 
            p.id_producto, 
            p.nombre, 
            p.descripcion, 
            p.categoria, 
            p.precio, 
            p.stock
        FROM productos p
        ORDER BY p.stock ASC
        LIMIT 10;
        """
        cursor.execute(sql)
        productos = cursor.fetchall()
        return productos
    except Exception as e:
        print(f"Error al obtener productos con menos stock: {e}")
        return []
    finally:
        conexion.commit()
        # Asegurarse de cerrar y recrear el cursor
        if cursor:
            cursor.close()
        cursor = conexion.cursor()

def agregar_stock(id_producto, cantidad_a_agregar):
    """
    Agrega una cantidad específica al stock de un producto.

    Args:
        id_producto (int): ID del producto al que se le quiere agregar stock.
        cantidad_a_agregar (int): Cantidad de stock a agregar.

    Returns:
        bool: True si se actualizó el stock correctamente, False en caso contrario.
    """
    global cursor
    try:
        # Verificar si el producto existe
        cursor.execute("SELECT stock FROM productos WHERE id_producto = %s", (id_producto,))
        producto = cursor.fetchone()

        if not producto:
            print("El producto no existe.")
            return False

        # Actualizar el stock
        nuevo_stock = producto[0] + cantidad_a_agregar
        cursor.execute("UPDATE productos SET stock = %s WHERE id_producto = %s", (nuevo_stock, id_producto))
        conexion.commit()

        print(f"Stock actualizado correctamente. Nuevo stock: {nuevo_stock}")
        return True

    except mysql.connector.Error as e:
        print(f"Error en la base de datos: {e}")
        conexion.rollback()
        return False
    except Exception as e:
        print(f"Error inesperado: {e}")
        conexion.rollback()
        return False
    finally:
        conexion.commit()
        # Asegurarse de cerrar y recrear el cursor
        if cursor:
            cursor.close()
        cursor = conexion.cursor()
