import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog, messagebox, scrolledtext
from CRUD_productos import agregar_producto, obtener_productos, actualizar_producto, eliminar_producto, obtener_productos_mas_vendidos, obtener_productos_menos_vendidos, obtener_productos_con_mas_stock, obtener_productos_con_menos_stock, agregar_stock
from CRUD_clientes import agregar_cliente, obtener_clientes, actualizar_cliente, obtener_clientes_con_mas_ordenes, obtener_clientes_con_menos_ordenes, obtener_clientes_con_ordenes_mas_antiguas, obtener_clientes_con_ordenes_mas_actuales
from CRUD_ordenes import obtener_ordenes, obtener_ordenes_por_cliente, crear_orden
from conexion import cerrar_conexion

def abrir_ventana_productos():  #Ventana gestion productos
    if hasattr(ventana, "ventana_productos") and ventana.ventana_productos.winfo_exists():
        ventana.ventana_productos.deiconify()
        return

    ventana.ventana_productos = tk.Toplevel(ventana)
    ventana.ventana_productos.title("Productos")
    ventana.ventana_productos.geometry("900x500")
    ventana.ventana_productos.resizable(False, False)

    etiqueta = tk.Label(ventana.ventana_productos, text="Gestión de Productos", font=("Arial", 14))
    etiqueta.pack(pady=10)

    combobox_opciones = ttk.Combobox(ventana.ventana_productos, font=("Arial", 12), state="readonly")
    combobox_opciones['values'] = ("Productos Más Vendidos", "Productos Menos Vendidos","Productos con Más Stock","Productos con Menos Stock")
    combobox_opciones.pack(pady=10)

    # Cuadro de texto con scroll para mostrar los productos
    cuadro_productos = scrolledtext.ScrolledText(ventana.ventana_productos, wrap=tk.WORD, width=90, height=15, font=("Arial", 10))
    cuadro_productos.pack(pady=10)
    cuadro_productos.config(state=tk.DISABLED)

    def agregar_producto_interfaz():
        nombre = simpledialog.askstring("Agregar Producto", "Ingrese el nombre del producto:")
        descripcion = simpledialog.askstring("Agregar Producto", "Ingrese la descripción del producto:")
        categoria = simpledialog.askstring("Agregar Producto", "Ingrese la categoria del producto:")
        precio = simpledialog.askfloat("Agregar Producto", "Ingrese el precio del producto:")
        stock = simpledialog.askinteger("Agregar Producto", "Ingrese la cantidad en stock del producto:")
        ventana.ventana_productos.grab_release()

        if nombre and descripcion and precio and categoria is not None and stock is not None:
            try:
                agregar_producto(nombre, descripcion, categoria, precio, stock)
                messagebox.showinfo("Éxito", f"Producto '{nombre}' agregado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar el producto: {e}")
        else:
            messagebox.showwarning("Campos Vacíos", "Todos los campos son obligatorios.")

    def ver_productos():
        try:
            productos = obtener_productos()  # Intentar obtener los productos
            if productos:
                cuadro_productos.config(state=tk.NORMAL)  # Activar el cuadro para modificarlo
                cuadro_productos.delete(1.0, tk.END)  # Limpiar el cuadro de texto antes de mostrar los productos
                
                # Mostrar los productos de forma horizontal
                for producto in productos:
                    producto_info = f"ID: {producto[0]}  Nombre: {producto[1]}  Descripción: {producto[2]}  " \
                                    f"Categoría: {producto[3]}  Precio: {producto[4]:.2f}  Stock: {producto[5]}\n"
                    cuadro_productos.insert(tk.END, producto_info)
                cuadro_productos.config(state=tk.DISABLED)  # Desactivar el cuadro después de actualizar
            else:
                messagebox.showwarning("No hay productos", "No se encontraron productos en la base de datos.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo obtener los productos: {e}")

    def actualizar_producto_interfaz():
        # Pedir el ID del producto a actualizar
        id_producto = simpledialog.askinteger("Actualizar Producto", "Ingrese el ID del producto a actualizar:")
    
        if id_producto:
            # Verificar si el ID existe en la base de datos
            productos = obtener_productos()  # O utilizar una consulta SQL para buscar el producto por ID
            if not any(p[0] == id_producto for p in productos):
                messagebox.showwarning("ID no encontrado", "No se encontró un producto con ese ID.")
                return

            # Pedir los nuevos datos del producto
            nombre = simpledialog.askstring("Actualizar Producto", "Ingrese el nuevo nombre del producto:")
            descripcion = simpledialog.askstring("Actualizar Producto", "Ingrese la nueva descripción del producto:")
            categoria = simpledialog.askstring("Actualizar Producto", "Ingrese la nueva categoría del producto:")
            precio = simpledialog.askfloat("Actualizar Producto", "Ingrese el nuevo precio del producto:")
            stock = simpledialog.askinteger("Actualizar Producto", "Ingrese la nueva cantidad en stock del producto:")

            if nombre and descripcion and categoria and precio is not None and stock is not None:
                try:
                    # Llamar a la función para actualizar el producto
                    actualizar_producto(id_producto, nombre, descripcion, categoria, precio, stock)
                    messagebox.showinfo("Éxito", f"Producto con ID {id_producto} actualizado correctamente.")
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo actualizar el producto: {e}")
            else:
                messagebox.showwarning("Campos Vacíos", "Todos los campos son obligatorios.")
        else:
            messagebox.showwarning("ID inválido", "Debe ingresar un ID válido del producto.")

    def eliminar_producto_interfaz():
        # Solicitar el ID del producto a eliminar
        producto_id = simpledialog.askinteger("Eliminar Producto", "Ingrese el ID del producto a eliminar:")

        if producto_id is not None:
            # Confirmación de eliminación
            confirmacion = simpledialog.askstring("Confirmación", f"¿Estás seguro de eliminar el producto con ID {producto_id}? (s/n)")

            if confirmacion and confirmacion.lower() == "s":
                try:
                    eliminar_producto(producto_id)
                    messagebox.showinfo("Éxito", f"Producto con ID {producto_id} eliminado correctamente.")
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo eliminar el producto: {e}")
            elif confirmacion and confirmacion.lower() == "n":
                messagebox.showinfo("Cancelado", "Eliminación cancelada.")
            else:
                messagebox.showwarning("Entrada no válida", "Por favor, ingresa 's' para sí o 'n' para no.")

    def actualizar_cuadro_productos(event=None):
        cuadro_productos.config(state=tk.NORMAL)
        cuadro_productos.delete(1.0, tk.END)  # Limpiar el cuadro de texto antes de mostrar los productos

        opcion = combobox_opciones.get()  # Obtener la opción seleccionada
        if opcion == "Productos Más Vendidos":
            productos = obtener_productos_mas_vendidos()
            mostrar_productos_mas_vendidos(productos)  # Función específica para mostrar productos más vendidos
        elif opcion == "Productos Menos Vendidos":
            productos = obtener_productos_menos_vendidos()
            mostrar_productos_menos_vendidos(productos)  # Función específica para mostrar productos menos vendidos
        elif opcion == "Productos con Más Stock":
            productos = obtener_productos_con_mas_stock()
            mostrar_productos_con_mas_stock(productos)  # Función específica para mostrar productos con más stock
        elif opcion == "Productos con Menos Stock":
            productos = obtener_productos_con_menos_stock()
            mostrar_productos_con_menos_stock(productos)  # Función específica para mostrar productos con menos stock
        else:
            productos = []

        cuadro_productos.config(state=tk.DISABLED)  # Desactivar el cuadro después de actualizar


        # Función para mostrar los productos más vendidos
    def mostrar_productos_mas_vendidos(productos):
        cuadro_productos.config(state=tk.NORMAL)  # Hacer el cuadro editable
        cuadro_productos.delete(1.0, tk.END)  # Limpiar el cuadro de texto
        if productos:
            for producto in productos:
                id_producto = producto[0]
                nombre = producto[1]
                total_vendido = producto[6]  # El total vendido está en la posición 6 de la tupla
                producto_info = f"ID: {id_producto}  Nombre: {nombre}  Total Vendido: {total_vendido}\n"
                cuadro_productos.insert(tk.END, producto_info)
        else:
            cuadro_productos.insert(tk.END, "No se encontraron productos.\n")
        cuadro_productos.config(state=tk.DISABLED)  # Deshabilitar el cuadro después de mostrar los productos


    # Función para mostrar los productos menos vendidos
    def mostrar_productos_menos_vendidos(productos):
        cuadro_productos.config(state=tk.NORMAL)
        cuadro_productos.delete(1.0, tk.END)
        if productos:
            for producto in productos:
                producto_info = f"ID: {producto[0]}  Nombre: {producto[1]}  Total Vendido: {producto[-1]}\n"
                cuadro_productos.insert(tk.END, producto_info)
        else:
            cuadro_productos.insert(tk.END, "No se encontraron productos.\n")
        cuadro_productos.config(state=tk.DISABLED)

    # Función para mostrar los productos con más stock
    def mostrar_productos_con_mas_stock(productos):
        cuadro_productos.config(state=tk.NORMAL)
        cuadro_productos.delete(1.0, tk.END)
        if productos:
            for producto in productos:
                producto_info = f"ID: {producto[0]}  Nombre: {producto[1]}  Stock: {producto[-1]}\n"
                cuadro_productos.insert(tk.END, producto_info)
        else:
            cuadro_productos.insert(tk.END, "No se encontraron productos.\n")
        cuadro_productos.config(state=tk.DISABLED)

    # Función para mostrar los productos con menos stock
    def mostrar_productos_con_menos_stock(productos):
        cuadro_productos.config(state=tk.NORMAL)
        cuadro_productos.delete(1.0, tk.END)
        if productos:
            for producto in productos:
                producto_info = f"ID: {producto[0]}  Nombre: {producto[1]}  Stock: {producto[-1]}\n"
                cuadro_productos.insert(tk.END, producto_info)
        else:
            cuadro_productos.insert(tk.END, "No se encontraron productos.\n")
        cuadro_productos.config(state=tk.DISABLED)


    def agregar_stock_interfaz():
        # Solicitar el ID del producto al usuario
        id_producto = simpledialog.askinteger("Agregar Stock", "Ingrese el ID del Producto:", parent=ventana.ventana_productos)

        if id_producto is None:
            return  # Si el usuario cancela o no ingresa un valor

        # Solicitar la cantidad de stock a agregar
        cantidad_a_agregar = simpledialog.askinteger("Agregar Stock", "Ingrese la cantidad de stock a agregar:", parent=ventana.ventana_productos)

        if cantidad_a_agregar is None:
            return  # Si el usuario cancela o no ingresa un valor

        if cantidad_a_agregar < 0:
            messagebox.showwarning("Error", "La cantidad debe ser un número positivo.")
            return

        # Intentar agregar el stock
        if agregar_stock(id_producto, cantidad_a_agregar):
            messagebox.showinfo("Éxito", "Stock agregado con éxito.")
        else:
            messagebox.showerror("Error", "Error al agregar stock. Verifique el ID del producto.")

     # Vincular el evento del combobox para actualizar los productos cuando se seleccione una opción
    combobox_opciones.bind("<<ComboboxSelected>>", actualizar_cuadro_productos)


    # Botones de la ventana
    boton_agregar = tk.Button(ventana.ventana_productos, text="Agregar Producto", font=("Arial", 12), command=agregar_producto_interfaz)
    boton_agregar.pack(side=tk.LEFT, padx=20, pady=10)

    boton_ver_productos = tk.Button(ventana.ventana_productos, text="Ver Productos", font=("Arial", 12), command=ver_productos)
    boton_ver_productos.pack(side=tk.LEFT, padx=20, pady=10)

    # Botón para actualizar producto
    boton_actualizar = tk.Button(ventana.ventana_productos, text="Actualizar Producto", font=("Arial", 12), command=actualizar_producto_interfaz)
    boton_actualizar.pack(side=tk.LEFT, padx=20, pady=10)

    # Botón para eliminar producto
    boton_eliminar = tk.Button(ventana.ventana_productos, text="Eliminar Producto", font=("Arial", 12), command=eliminar_producto_interfaz)
    boton_eliminar.pack(side=tk.LEFT, padx=20, pady=10)

    # Botón para agregar stock
    boton_agregar_stock = tk.Button(ventana.ventana_productos, text="Agregar Stock", font=("Arial", 12), command=agregar_stock_interfaz)
    boton_agregar_stock.pack(side=tk.LEFT, padx=20, pady=10)

def abrir_ventana_clientes():  #Ventana gestion clientes
    if hasattr(ventana, "ventana_clientes") and ventana.ventana_clientes.winfo_exists():
        ventana.ventana_clientes.deiconify()
        return

    ventana.ventana_clientes = tk.Toplevel(ventana)
    ventana.ventana_clientes.title("Clientes")
    ventana.ventana_clientes.geometry("800x500")
    ventana.ventana_clientes.resizable(False, False)  

    etiqueta = tk.Label(ventana.ventana_clientes, text="Gestión de Clientes", font=("Arial", 14))
    etiqueta.pack(pady=10)

    combobox_opciones = ttk.Combobox(ventana.ventana_clientes, font=("Arial", 12), state="readonly")
    combobox_opciones['values'] = ("Clientes con Más Órdenes", "Clientes con Menos Órdenes","Clientes con Órdenes Más Actuales","Clientes con Órdenes Más Antiguas")
    combobox_opciones.pack(pady=10)

    # Cuadro de texto con scroll para mostrar los clientes
    cuadro_clientes = scrolledtext.ScrolledText(ventana.ventana_clientes, wrap=tk.WORD, width=90, height=15, font=("Arial", 10))
    cuadro_clientes.pack(pady=10)
    cuadro_clientes.config(state=tk.DISABLED)

    def actualizar_clientes():
        opcion = combobox_opciones.get()  # Obtener la opción seleccionada

        # Obtener los clientes según la opción seleccionada
        if opcion == "Clientes con Más Órdenes":
            clientes = obtener_clientes_con_mas_ordenes()
            mostrar_clientes_mas_ordenes(clientes)  # Función específica para mostrar clientes con más órdenes
        elif opcion == "Clientes con Menos Órdenes":
            clientes = obtener_clientes_con_menos_ordenes()
            mostrar_clientes_menos_ordenes(clientes)  # Función específica para mostrar clientes con menos órdenes
        elif opcion == "Clientes con Órdenes Más Actuales":
            clientes = obtener_clientes_con_ordenes_mas_actuales()
            mostrar_clientes_ordenes_actuales(clientes)  # Función específica para mostrar clientes con órdenes más actuales
        elif opcion == "Clientes con Órdenes Más Antiguas":
            clientes = obtener_clientes_con_ordenes_mas_antiguas()
            mostrar_clientes_ordenes_antiguas(clientes)  # Función específica para mostrar clientes con órdenes más antiguas
        else:
            clientes = []

    # Función para mostrar clientes con más órdenes
    def mostrar_clientes_mas_ordenes(clientes):
        cuadro_clientes.config(state=tk.NORMAL)  # Hacer el cuadro editable
        cuadro_clientes.delete(1.0, tk.END)  # Limpiar el cuadro de texto
        if clientes:
            for cliente in clientes:
                cliente_info = f"ID: {cliente[0]}  Nombre: {cliente[1]}  Total Órdenes: {cliente[2]}\n"
                cuadro_clientes.insert(tk.END, cliente_info)
        else:
            cuadro_clientes.insert(tk.END, "No se encontraron clientes.\n")
        cuadro_clientes.config(state=tk.DISABLED)  # Deshabilitar el cuadro después de mostrar los clientes

    # Función para mostrar clientes con menos órdenes
    def mostrar_clientes_menos_ordenes(clientes):
        cuadro_clientes.config(state=tk.NORMAL)
        cuadro_clientes.delete(1.0, tk.END)
        if clientes:
            for cliente in clientes:
                cliente_info = f"ID: {cliente[0]}  Nombre: {cliente[1]}  Total Órdenes: {cliente[2]}\n"
                cuadro_clientes.insert(tk.END, cliente_info)
        else:
            cuadro_clientes.insert(tk.END, "No se encontraron clientes.\n")
        cuadro_clientes.config(state=tk.DISABLED)

    # Función para mostrar clientes con órdenes más actuales
    def mostrar_clientes_ordenes_actuales(clientes):
        cuadro_clientes.config(state=tk.NORMAL)
        cuadro_clientes.delete(1.0, tk.END)
        if clientes:
            for cliente in clientes:
                cliente_info = f"ID: {cliente[0]}  Nombre: {cliente[1]}  Última Orden: {cliente[3]}\n"
                cuadro_clientes.insert(tk.END, cliente_info)
        else:
            cuadro_clientes.insert(tk.END, "No se encontraron clientes.\n")
        cuadro_clientes.config(state=tk.DISABLED)


    # Función para mostrar clientes con órdenes más antiguas
    def mostrar_clientes_ordenes_antiguas(clientes):
        cuadro_clientes.config(state=tk.NORMAL)
        cuadro_clientes.delete(1.0, tk.END)
        if clientes:
            for cliente in clientes:
                # Mostrar la fecha de la primera orden (cliente[3] contiene la fecha)
                cliente_info = f"ID: {cliente[0]}  Nombre: {cliente[1]}  Primera Orden: {cliente[3]}\n"
                cuadro_clientes.insert(tk.END, cliente_info)
        else:
            cuadro_clientes.insert(tk.END, "No se encontraron clientes.\n")
        cuadro_clientes.config(state=tk.DISABLED)

    combobox_opciones.bind("<<ComboboxSelected>>", lambda event: actualizar_clientes())

    # Función para agregar un cliente
    def agregar_cliente_interfaz():
        nombre = simpledialog.askstring("Agregar Cliente", "Ingrese el nombre del cliente:")
        email = simpledialog.askstring("Agregar Cliente", "Ingrese el email del cliente:")
        telefono = simpledialog.askstring("Agregar Cliente", "Ingrese el teléfono del cliente:")
        direccion = simpledialog.askstring("Agregar Cliente", "Ingrese la direccion del cliente:")

        if nombre and email and telefono and direccion is not None:
            try:
                agregar_cliente(nombre, email, telefono, direccion)
                messagebox.showinfo("Éxito", f"Cliente '{nombre}' agregado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar el cliente: {e}")
        else:
            messagebox.showwarning("Campos Vacíos", "Todos los campos son obligatorios.")

    # Función para ver los clientes
    def ver_clientes():
        # Obtener los clientes de la base de datos
        clientes = obtener_clientes()
        if clientes:  # Si hay clientes
            cuadro_clientes.config(state=tk.NORMAL)  # Hacer el cuadro editable para insertar los clientes
            cuadro_clientes.delete(1.0, tk.END)  # Limpiar el cuadro de texto antes de mostrar los clientes
            
            # Mostrar los clientes
            for cliente in clientes:
                cliente_info = f"ID: {cliente[0]}  Nombre: {cliente[1]}  Email: {cliente[2]}  Teléfono: {cliente[3]}  Dirección: {cliente[4]}\n"
                cuadro_clientes.insert(tk.END, cliente_info)
            cuadro_clientes.config(state=tk.DISABLED)  # Deshabilitar el cuadro después de mostrar los clientes
        else:
            messagebox.showwarning("No hay clientes", "No se encontraron clientes en la base de datos.")

    def actualizar_cliente_interfaz():
        # Solicitar el ID del cliente a actualizar
        id_cliente = simpledialog.askinteger("Actualizar Cliente", "Ingrese el ID del cliente a actualizar:")
        if id_cliente:
            # Verificar si el ID existe en la base de datos
            clientes = obtener_clientes()
            if not any(cliente[0] == id_cliente for cliente in clientes):
                messagebox.showwarning("ID no encontrado", "No se encontró un cliente con ese ID.")
                return

            # Pedir los nuevos datos del cliente
            nombre = simpledialog.askstring("Actualizar Cliente", "Ingrese el nuevo nombre del cliente:")
            email = simpledialog.askstring("Actualizar Cliente", "Ingrese el nuevo email del cliente:")
            telefono = simpledialog.askstring("Actualizar Cliente", "Ingrese el nuevo teléfono del cliente:")
            direccion = simpledialog.askstring("Actualizar Cliente", "Ingrese la nueva dirección del cliente:")

            if nombre and email and telefono and direccion:
                try:
                    # Llamar a la función para actualizar el cliente
                    actualizar_cliente(id_cliente, nombre, email, telefono, direccion)
                    messagebox.showinfo("Éxito", f"Cliente con ID {id_cliente} actualizado correctamente.")
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo actualizar el cliente: {e}")
            else:
                messagebox.showwarning("Campos Vacíos", "Todos los campos son obligatorios.")
        else:
            messagebox.showwarning("ID inválido", "Debe ingresar un ID válido del cliente.")

    # Botones de la ventana de clientes
    boton_agregar = tk.Button(ventana.ventana_clientes, text="Agregar Cliente", font=("Arial", 12), command=agregar_cliente_interfaz)
    boton_agregar.pack(side=tk.LEFT, padx=70, pady=10)  # Reducir margen izquierdo/derecho

    boton_ver_clientes = tk.Button(ventana.ventana_clientes, text="Ver Clientes", font=("Arial", 12), command=ver_clientes)
    boton_ver_clientes.pack(side=tk.LEFT, padx=70, pady=10)

    boton_actualizar_cliente = tk.Button(ventana.ventana_clientes, text="Actualizar Cliente", font=("Arial", 12), command=actualizar_cliente_interfaz)
    boton_actualizar_cliente.pack(side=tk.LEFT, padx=70, pady=10)

def abrir_ventana_ordenes():  #Ventana gestion ordenes
    if hasattr(ventana, "ventana_ordenes") and ventana.ventana_ordenes.winfo_exists():
        ventana.ventana_ordenes.deiconify()
        return

    ventana.ventana_ordenes = tk.Toplevel(ventana)
    ventana.ventana_ordenes.title("Ordenes")
    ventana.ventana_ordenes.geometry("800x500")
    ventana.ventana_ordenes.resizable(False, False)

    etiqueta = tk.Label(ventana.ventana_ordenes, text="Gestión de Órdenes", font=("Arial", 14))
    etiqueta.pack(pady=10)

    # Cuadro de texto con scroll para mostrar las órdenes
    cuadro_ordenes = scrolledtext.ScrolledText(ventana.ventana_ordenes, wrap=tk.WORD, width=90, height=15, font=("Arial", 10))
    cuadro_ordenes.pack(pady=10)
    cuadro_ordenes.config(state=tk.DISABLED)

    def ver_ordenes():  # Función para ver todas las órdenes
        try:
            ordenes = obtener_ordenes()  # Obtener las órdenes desde la base de datos
            if ordenes:
                cuadro_ordenes.config(state=tk.NORMAL)  # Activar el cuadro de texto para editar
                cuadro_ordenes.delete(1.0, tk.END)  # Limpiar el cuadro de texto antes de mostrar las nuevas órdenes

                # Mostrar las órdenes de forma legible
                for orden in ordenes:
                    id_orden, id_cliente, id_producto, cantidad, total, fecha_orden = orden
                    orden_info = f"ID Orden: {id_orden}  ID Cliente: {id_cliente}  ID Producto: {id_producto}  " \
                              f"Cantidad: {cantidad}  Total: ${total:.2f}  Fecha: {fecha_orden}\n"
                    cuadro_ordenes.insert(tk.END, orden_info)
                cuadro_ordenes.config(state=tk.DISABLED)  # Desactivar el cuadro después de actualizar
            else:
                messagebox.showwarning("No hay órdenes", "No se encontraron órdenes en la base de datos.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron obtener las órdenes: {e}")


    def ver_ordenes_cliente():  # Función para ver las órdenes de un cliente por ID
        try:
            # Solicitar el ID del cliente
            id_cliente = simpledialog.askinteger("Ver Órdenes de Cliente", "Ingrese el ID del cliente:")
        
            if id_cliente is not None:
                # Obtener las órdenes del cliente
                ordenes_cliente = obtener_ordenes_por_cliente(id_cliente)
            
                if ordenes_cliente:
                    cuadro_ordenes.config(state=tk.NORMAL)  # Habilitar el cuadro de texto para editar
                    cuadro_ordenes.delete(1.0, tk.END)  # Limpiar el cuadro de texto antes de mostrar las órdenes

                    # Mostrar las órdenes del cliente
                    for orden in ordenes_cliente:
                        id_orden, id_cliente, id_producto, cantidad, total, fecha_orden = orden
                        orden_info = f"ID Orden: {id_orden}  ID Producto: {id_producto}  Cantidad: {cantidad}  " \
                                    f"Total: ${total:.2f}  Fecha: {fecha_orden}\n"
                        cuadro_ordenes.insert(tk.END, orden_info)

                    cuadro_ordenes.config(state=tk.DISABLED)  # Desactivar el cuadro después de actualizar
                else:
                    messagebox.showwarning("No hay órdenes", f"No se encontraron órdenes para el cliente con ID {id_cliente}.")
            else:
                messagebox.showwarning("ID inválido", "Debe ingresar un ID válido de cliente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron obtener las órdenes del cliente: {e}")


    def crear_orden_interfaz():  #Funcion para crear una orden
        try:
            # Pedir el ID del cliente, producto y cantidad
            id_cliente = simpledialog.askinteger("Crear Orden", "Ingrese el ID del cliente:")
            id_producto = simpledialog.askinteger("Crear Orden", "Ingrese el ID del producto:")
            cantidad = simpledialog.askinteger("Crear Orden", "Ingrese la cantidad de productos:")

            # Verificar que los datos sean válidos
            if id_cliente and id_producto and cantidad:
                # Llamar a la función para crear la orden
                exito = crear_orden(id_cliente, id_producto, cantidad)

                if exito:
                    messagebox.showinfo("Éxito", "La orden se ha creado correctamente.")
                else:
                    messagebox.showerror("Error", "No se pudo crear la orden. Verifique el stock o los datos ingresados.")
            else:
                messagebox.showwarning("Campos Vacíos", "Todos los campos son obligatorios.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear la orden: {e}")


    # Botón para ver las órdenes
    boton_ver_ordenes = tk.Button(ventana.ventana_ordenes, text="Ver Órdenes", font=("Arial", 12), command=ver_ordenes)
    boton_ver_ordenes.pack(side=tk.LEFT, padx=70, pady=10)
    # Botón para ver las órdenes de un cliente por ID
    boton_ver_ordenes_cliente = tk.Button(ventana.ventana_ordenes, text="Ver Órdenes de Cliente", font=("Arial", 12), command=ver_ordenes_cliente)
    boton_ver_ordenes_cliente.pack(side=tk.LEFT, padx=70, pady=10)
    # Botón para crear una orden
    boton_crear_orden = tk.Button(ventana.ventana_ordenes, text="Crear Orden", font=("Arial", 12), command=crear_orden_interfaz)
    boton_crear_orden.pack(side=tk.LEFT, padx=70, pady=10)

# Ventana principal
ventana = tk.Tk()
ventana.title("Gestión de Aplicación")

# Obtener las dimensiones de la pantalla
pantalla_ancho = ventana.winfo_screenwidth()
pantalla_alto = ventana.winfo_screenheight()
# Tamaño de la ventana principal
ventana_ancho = 400
ventana_alto = 300
# Calcular la posición para centrar la ventana en la pantalla
pos_x = int((pantalla_ancho - ventana_ancho) / 2)
pos_y = int((pantalla_alto - ventana_alto) / 2)
# Establecer la geometría de la ventana con la posición calculada
ventana.geometry(f"{ventana_ancho}x{ventana_alto}+{pos_x}+{pos_y}")

label_titulo = tk.Label(ventana, text="Gestión de Ventas", font=("Arial", 16))
label_titulo.pack(pady=20)

boton_productos = tk.Button(ventana, text="Productos", font=("Arial", 12),width=15,  command=abrir_ventana_productos)
boton_productos.pack(pady=5)

# Botón en la ventana principal para abrir la ventana de clientes
boton_clientes = tk.Button(ventana, text="Clientes", font=("Arial", 12),width=15, command=abrir_ventana_clientes)
boton_clientes.pack(pady=10)

boton_ordenes = tk.Button(ventana, text="Ordenes", font=("Arial", 12),width=15,  command=abrir_ventana_ordenes)
boton_ordenes.pack(pady=10)

# Cierra la conexión al salir
ventana.protocol("WM_DELETE_WINDOW", lambda: (cerrar_conexion(), ventana.destroy()))

ventana.mainloop()




