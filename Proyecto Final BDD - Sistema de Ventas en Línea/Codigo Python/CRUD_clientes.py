import mysql.connector

# Conexión a la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="ventas"
)

cursor = conexion.cursor()

def agregar_cliente(nombre, email, telefono, direccion):
    try:
        # Consulta SQL para insertar un nuevo cliente
        query = "INSERT INTO clientes (nombre, email, telefono, direccion) VALUES (%s, %s, %s, %s)"
        valores = (nombre, email, telefono, direccion)

        # Ejecutar la consulta
        cursor.execute(query, valores)

        # Confirmar la transacción
        conexion.commit()

        print(f"Cliente {nombre} agregado correctamente.")
    except mysql.connector.Error as err:
        # En caso de error, mostrar el error
        print(f"Error al agregar cliente: {err}")
        conexion.rollback()

def actualizar_cliente(id_cliente, nombre, email, telefono, direccion):
    try:
        # Consulta para actualizar el cliente en la base de datos
        query = """
        UPDATE clientes
        SET nombre = %s, email = %s, telefono = %s, direccion = %s
        WHERE id_cliente = %s;
        """
        valores = (nombre, email, telefono, direccion, id_cliente)
        
        cursor.execute(query, valores)
        conexion.commit()

        if cursor.rowcount > 0:
            print(f"Cliente con ID {id_cliente} actualizado correctamente.")
        else:
            print(f"No se encontró un cliente con ID {id_cliente}.")
    
    except mysql.connector.Error as e:
        print(f"Error al actualizar el cliente: {e}")
        conexion.rollback()

def obtener_clientes():
    """
    Recupera todos los clientes de la base de datos.

    Returns:
        list: Lista de tuplas con los datos de los clientes.
              Cada tupla contiene (ID_cliente, Nombre, Email, Teléfono, Dirección).
    """
    try:
        sql = "SELECT * FROM clientes;"
        cursor.execute(sql)
        clientes = cursor.fetchall()
        return clientes
    except Exception as e:
        print(f"Error al obtener clientes: {e}")
        return []

import mysql.connector

def eliminar_cliente(id_cliente):
    global cursor, conexion
    try:
        # Verificar si el cliente tiene órdenes asociadas (esto es para evitar eliminarlo si tiene órdenes)
        cursor.execute("SELECT COUNT(*) FROM ordenes WHERE id_cliente = %s", (id_cliente,))
        result = cursor.fetchone()
        if result[0] > 0:
            raise Exception("El cliente tiene órdenes asociadas. No se puede eliminar.")

        # Si no tiene órdenes asociadas, proceder a eliminar el cliente
        cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (id_cliente,))
        conexion.commit()

        # Verificar si la eliminación fue exitosa
        if cursor.rowcount > 0:
            return True  # Cliente eliminado correctamente
        else:
            return False  # No se encontró el cliente con el ID dado

    except mysql.connector.Error as e:
        print(f"Error en la base de datos: {e}")
        conexion.rollback()  # Revertir si hubo algún error en la transacción
        return False
    except Exception as e:
        print(f"Error inesperado: {e}")
        conexion.rollback()  # Revertir en caso de errores inesperados
        return False
    finally:
        # Cerrar el cursor después de la operación
        conexion.commit()
        if cursor:
            cursor.close()
        # Crear un nuevo cursor para futuras operaciones
        cursor = conexion.cursor()


def obtener_clientes_con_mas_ordenes():
    global cursor
    try:
        # Consulta SQL para obtener los clientes con más órdenes
        query = """
            SELECT c.id_cliente, c.nombre, COUNT(o.id_orden) AS total_ordenes
            FROM clientes c
            LEFT JOIN ordenes o ON c.id_cliente = o.id_cliente
            GROUP BY c.id_cliente
            ORDER BY total_ordenes DESC;
        """
        cursor.execute(query)

        # Obtener los resultados
        clientes = cursor.fetchall()

        return clientes  # Retornar la lista de clientes con más órdenes

    except mysql.connector.Error as e:
        print(f"Error en la base de datos: {e}")
        return []
    except Exception as e:
        print(f"Error inesperado: {e}")
        return []
    finally:
        # Asegurarse de recrear el cursor
        conexion.commit()
        if cursor:
            cursor.close()
        cursor = conexion.cursor()

def obtener_clientes_con_menos_ordenes():
    try:
        # Consulta SQL para obtener los clientes con menos órdenes
        query = """
            SELECT c.id_cliente, c.nombre, COUNT(o.id_orden) AS total_ordenes
            FROM clientes c
            LEFT JOIN ordenes o ON c.id_cliente = o.id_cliente
            GROUP BY c.id_cliente
            ORDER BY total_ordenes ASC;
        """
        cursor.execute(query)

        # Obtener los resultados
        clientes = cursor.fetchall()

        return clientes  # Retornar la lista de clientes con menos órdenes

    except mysql.connector.Error as e:
        print(f"Error en la base de datos: {e}")
        return []
    except Exception as e:
        print(f"Error inesperado: {e}")
        return []

def obtener_clientes_con_ordenes_mas_actuales():
    query = """
    SELECT c.id_cliente, c.nombre, COUNT(o.id_orden) AS total_ordenes, 
           DATE_FORMAT(MAX(o.fecha_orden), '%d/%m/%Y') AS ultima_orden
    FROM clientes c
    LEFT JOIN ordenes o ON c.id_cliente = o.id_cliente
    WHERE o.id_orden IS NOT NULL  -- Asegura que solo se muestren clientes con al menos una orden
    GROUP BY c.id_cliente
    ORDER BY ultima_orden DESC;
    """
    cursor.execute(query)
    return cursor.fetchall()


def obtener_clientes_con_ordenes_mas_antiguas():
    query = """
    SELECT c.id_cliente, c.nombre, COUNT(o.id_orden) AS total_ordenes, 
           DATE_FORMAT(MIN(o.fecha_orden), '%d/%m/%Y') AS primera_orden
    FROM clientes c
    LEFT JOIN ordenes o ON c.id_cliente = o.id_cliente
    WHERE o.id_orden IS NOT NULL  -- Asegura que solo se muestren clientes con al menos una orden
    GROUP BY c.id_cliente
    ORDER BY primera_orden ASC;
    """
    cursor.execute(query)
    return cursor.fetchall()

