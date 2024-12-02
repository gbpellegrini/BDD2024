import mysql.connector

class BaseDeDatos:
    def __init__(self, host, user, password, database):
        self.config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database
        }
        self.conexion = None
        self.cursor = None

    def conectar(self):
        self.conexion = mysql.connector.connect(**self.config)
        self.cursor = self.conexion.cursor()

    def desconectar(self):
        if self.cursor:
            self.cursor.close()
        if self.conexion:
            self.conexion.close()

    def ejecutar(self, query, valores=None):
        self.cursor.execute(query, valores or ())
        self.conexion.commit()

    def obtener_datos(self, query, valores=None):
        self.cursor.execute(query, valores or ())
        return self.cursor.fetchall()

# Crear instancia global de la base de datos
db = BaseDeDatos(host="localhost", user="root", password="root", database="ventas")
db.conectar()

def cerrar_conexion():
    """
    Cierra la conexión a la base de datos.
    """
    try:
        db.desconectar()
        print("Conexión a la base de datos cerrada.")
    except Exception as e:
        print(f"Error al cerrar la conexión: {e}")
