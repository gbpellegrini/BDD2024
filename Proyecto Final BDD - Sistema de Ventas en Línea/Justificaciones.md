**Diseño de la base de datos**
El diseño se basa en tres tablas principales: clientes, productos y ordenes.

- Tabla clientes: Representa a los clientes de la plataforma. Incluye atributos como nombre, email, telefono y direccion.
- Tabla productos: Contiene la información de los productos disponibles, como nombre, descripcion, categoria, precio y stock.
- Tabla ordenes: Registra las órdenes realizadas por los clientes. Cada registro contiene la relación entre un cliente (id_cliente) y un producto (id_producto), así como la cantidad pedida (cantidad) y la fecha de la orden (fecha_orden).


**Entidades Fuertes**
*Clientes*

Representa a los usuarios que realizan órdenes de compra en la plataforma.

Atributos:
- id_cliente (PK): Identificador único del cliente.
- nombre: Nombre del cliente.
- email: Correo electrónico del cliente.
- telefono: Número de teléfono.
- direccion: Dirección del cliente.

Justificación: Es una entidad fuerte porque su existencia no depende de ninguna otra entidad y tiene un identificador único.

*Productos*

Representa los productos disponibles para la venta.

Atributos:
- id_producto (PK): Identificador único del producto.
- nombre: Nombre del producto.
- descripcion: Descripción del producto.
- categoria: Categoría del producto.
- precio: Precio unitario del producto.
- stock: Cantidad disponible en inventario.

Justificación: Es una entidad fuerte ya que existe de manera independiente y no depende de otras entidades.

*Órdenes*

Representa las transacciones realizadas por los clientes.

Atributos:
- id_orden (PK): Identificador único de la orden.
- id_cliente (FK): Cliente que realizó la orden.
- id_producto (FK): Producto incluido en la orden.
- cantidad: Cantidad pedida del producto.
- fecha_orden: Fecha en la que se realizó la orden.

Justificación: Es una entidad fuerte porque puede tener una identificación independiente, aunque sus relaciones están vinculadas a las entidades clientes y productos.

**Entidades debiles**
En este diseño, no hay entidades débiles de manera estricta, ya que todas las entidades principales tienen claves primarias independientes que no dependen de otras entidades para su identificación. Sin embargo, si consideramos las relaciones entre las entidades, podemos ver que las órdenes dependen de las entidades clientes y productos a través de claves foráneas, pero esto no hace que las órdenes sean una entidad débil, sino que simplemente implica una relación de dependencia o de existencia.

**Relaciones y Cardinalidades**
1. Relación entre Clientes y Órdenes

Tipo: Uno a Muchos (1:N)
Descripción: Un cliente puede realizar múltiples órdenes, pero cada orden está asociada a un solo cliente.
Implementación: Llave foránea id_cliente en la tabla ordenes referenciando a id_cliente en clientes.

2. Relación entre Productos y Órdenes

Tipo: Uno a Muchos (1:N)
Descripción: Un producto puede aparecer en múltiples órdenes, pero cada orden hace referencia a un único producto.
Implementación: Llave foránea id_producto en la tabla ordenes referenciando a id_producto en productos.


**Atributos**
Clientes:
- Simples: nombre, email, telefono.
- Clave primaria: id_cliente.

Productos:
- Simples: nombre, descripcion, categoria, precio, stock.
- Clave primaria: id_producto.

Órdenes:
- Simples: cantidad, fecha_orden.
- Llaves foráneas: id_cliente, id_producto.
- Clave primaria: id_orden.