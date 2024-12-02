import mysql.connector
import datetime

# Conexión a la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="ventas"
)

cursor = conexion.cursor()

def obtener_ordenes():
    """
    Recupera todas las órdenes almacenadas en la base de datos y calcula el total de cada orden.
    
    Returns:
        list: Lista de tuplas con los datos de las órdenes, incluyendo el total calculado.
    """
    try:
        sql = "SELECT id_orden, id_cliente, id_producto, cantidad, fecha_orden FROM ordenes"  # Selecciona las columnas necesarias
        
        # Ejecutar la consulta
        cursor.execute(sql)
        
        # Obtener los resultados
        ordenes = cursor.fetchall()
        
        # Lista para almacenar las órdenes con el total calculado
        ordenes_con_total = []
        
        for orden in ordenes:
            id_orden, id_cliente, id_producto, cantidad, fecha_orden = orden
            
            # Obtener el precio del producto asociado a esta orden
            cursor.execute("SELECT precio FROM productos WHERE id_producto = %s", (id_producto,))
            producto = cursor.fetchone()
            
            if producto:
                precio = producto[0]
                # Calcular el total de la orden
                total = cantidad * precio
                # Agregar la orden con el total calculado a la lista
                ordenes_con_total.append((id_orden, id_cliente, id_producto, cantidad, total, fecha_orden))
        
        return ordenes_con_total  # Devolver la lista de órdenes con el total calculado
    except Exception as e:
        print(f"Error al obtener las órdenes: {e}")
        return []  # Si ocurre un error, se devuelve una lista vacía


def obtener_ordenes_por_cliente(id_cliente): 
    """
    Recupera las órdenes de un cliente específico basándose en el ID del cliente y calcula el total de cada orden.

    Args:
        id_cliente (int): El ID del cliente cuyas órdenes se desean recuperar.

    Returns:
        list: Lista de tuplas con los datos de las órdenes del cliente,
              incluyendo el total calculado para cada una.
    """
    try:
        sql = """
        SELECT id_orden, id_cliente, id_producto, cantidad, fecha_orden
        FROM ordenes
        WHERE id_cliente = %s
        """
        cursor.execute(sql, (id_cliente,))
        ordenes = cursor.fetchall()
        
        # Lista para almacenar las órdenes con el total calculado
        ordenes_con_total = []
        
        for orden in ordenes:
            id_orden, id_cliente, id_producto, cantidad, fecha_orden = orden
            
            # Obtener el precio del producto asociado a esta orden
            cursor.execute("SELECT precio FROM productos WHERE id_producto = %s", (id_producto,))
            producto = cursor.fetchone()
            
            if producto:
                precio = producto[0]
                # Calcular el total de la orden
                total = cantidad * precio
                # Agregar la orden con el total calculado a la lista
                ordenes_con_total.append((id_orden, id_cliente, id_producto, cantidad, total, fecha_orden))
        
        return ordenes_con_total  # Devolver la lista de órdenes con el total calculado
    except Exception as e:
        print(f"Error al obtener órdenes del cliente con ID {id_cliente}: {e}")
        return []  # Si ocurre un error, se devuelve una lista vacía

    

def crear_orden(id_cliente, id_producto, cantidad):
    global cursor
    try:
        # Verificar el stock disponible
        cursor.execute("SELECT stock, precio FROM productos WHERE id_producto = %s", (id_producto,))
        producto = cursor.fetchone()

        if producto is None:
            return False  # Producto no encontrado

        stock_disponible, precio = producto

        # Verificar si la cantidad solicitada es mayor al stock disponible
        if cantidad > stock_disponible:
            return False  # No hay suficiente stock

        # Insertar la orden en la tabla ordenes
        fecha_actual = datetime.date.today()  # Obtener la fecha actual
        cursor.execute("""
            INSERT INTO ordenes (id_cliente, id_producto, cantidad, fecha_orden)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_cliente, id_producto, cantidad, fecha_actual))
        conexion.commit()

        # Actualizar el stock del producto después de realizar la orden
        cursor.execute("""
            UPDATE productos
            SET stock = stock - %s
            WHERE id_producto = %s
        """, (cantidad, id_producto))
        conexion.commit()

        return True  # Orden creada correctamente

    except mysql.connector.Error as e:
        print(f"Error en la base de datos: {e}")
        conexion.rollback()  # Si ocurre un error, revertimos la transacción
        return False
    except Exception as e:
        print(f"Error inesperado: {e}")
        conexion.rollback()  # Revertir transacción si hay algún error inesperado
        return False
    finally:
        # Cerrar el cursor después de todas las operaciones
        if cursor:
            cursor.close()
        # Crear un nuevo cursor para futuras operaciones
        cursor = conexion.cursor()
