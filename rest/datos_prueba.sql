-- Datos "padre" para poder probar los CRUD en Postman (ids 9001+ para no chocar con otros).
-- Ejecutar una vez en MySQL Workbench sobre la base del proyecto.
INSERT IGNORE INTO Usuario (idUsuario, nombre, credenciales) VALUES (9001, 'Usuario Prueba REST 1', 'x'), (9002, 'Usuario Prueba REST 2', 'x');
INSERT IGNORE INTO Cajero (id_cajero, Usuario_idUsuario) VALUES (9001, 9001);
INSERT IGNORE INTO Caja (id_caja, fecha_apertura, monto_inicial, Cajero_id_cajero) VALUES (9001, NOW(), 100000, 9001);
INSERT IGNORE INTO Mesa (id_mesa, numero, estado) VALUES (9001, 91, 'libre'), (9002, 92, 'libre');
INSERT IGNORE INTO Categoria (id_categoria, nombre) VALUES (9001, 'Categoria Prueba');
INSERT IGNORE INTO Producto (idProducto, nombre, descripcion, precio, cantidad_disponible, Categoria_id_categoria) VALUES (9001, 'Producto Prueba', 'Solo para pruebas', 12000, 50, 9001);
INSERT IGNORE INTO Pedido (id_pedido, estado, fecha_creacion, tipo_pedido) VALUES (9001, 'pendiente', NOW(), 'mesa');

-- LIMPIEZA (cuando termines de probar; en este orden por las llaves foráneas):
-- DELETE FROM Pago WHERE id_pago >= 9001;  DELETE FROM DetallePedido WHERE id_detalle_pedido >= 9001;
-- DELETE FROM PedidoMesa WHERE id_pedido_mesa >= 9001;  DELETE FROM Cocinero WHERE id_cocinero >= 9001;
-- DELETE FROM Administrador WHERE id_administrador >= 9001;  DELETE FROM Pedido WHERE id_pedido = 9001;
-- DELETE FROM Producto WHERE idProducto = 9001;  DELETE FROM Categoria WHERE id_categoria = 9001;
-- DELETE FROM Mesa WHERE id_mesa IN (9001, 9002);  DELETE FROM Caja WHERE id_caja = 9001;
-- DELETE FROM Cajero WHERE id_cajero = 9001;  DELETE FROM Usuario WHERE idUsuario IN (9001, 9002);
