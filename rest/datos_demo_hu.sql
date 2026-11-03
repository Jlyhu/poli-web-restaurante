-- Datos de DEMOSTRACIÓN para HU-02, HU-03, HU-08, HU-09 y HU-14 (ids 9101 en adelante).
-- Se puede ejecutar varias veces (INSERT IGNORE). Orden: primero los "padres", luego los "hijos".
-- Cargar con:  python cargar_datos_prueba.py rest/datos_demo_hu.sql
INSERT IGNORE INTO Usuario (idUsuario, nombre, credenciales) VALUES (9101, 'Carlos Cocinero', '1234'), (9102, 'Ana Administradora', '1234'), (9103, 'Cajero Demo', '1234'), (9104, 'Laura Cocinera', '1234');
INSERT IGNORE INTO Cocinero (id_cocinero, estacion, Usuario_idUsuario) VALUES (9101, 'Parrilla', 9101), (9102, 'Cocina fría', 9104);
INSERT IGNORE INTO Administrador (id_administrador, Usuario_idUsuario) VALUES (9101, 9102);
INSERT IGNORE INTO Cajero (id_cajero, Usuario_idUsuario) VALUES (9101, 9103);
INSERT IGNORE INTO Caja (id_caja, fecha_apertura, monto_inicial, Cajero_id_cajero) VALUES (9101, NOW(), 200000, 9101);
INSERT IGNORE INTO Mesa (id_mesa, numero, estado) VALUES (9101, 101, 'Disponible'), (9102, 102, 'Disponible'), (9103, 103, 'Disponible'), (9104, 104, 'Disponible'), (9105, 105, 'Disponible'), (9106, 106, 'Disponible');
INSERT IGNORE INTO Categoria (id_categoria, nombre) VALUES (9101, 'Platos fuertes'), (9102, 'Bebidas'), (9103, 'Postres');
INSERT IGNORE INTO Producto (idProducto, nombre, descripcion, precio, cantidad_disponible, Categoria_id_categoria) VALUES (9101, 'Bandeja paisa', 'Plato típico completo', 28000, 20, 9101), (9102, 'Sopa del día', 'Consulte el sabor con el mesero', 12000, 15, 9101), (9103, 'Limonada de coco', 'Jarra personal', 6000, 30, 9102), (9104, 'Tres leches', 'Porción individual', 9000, 0, 9103);
INSERT IGNORE INTO Pedido (id_pedido, estado, fecha_creacion, fecha_ultima_actualizacion, tipo_pedido) VALUES (9101, 'PENDIENTE', NOW() - INTERVAL 25 MINUTE, NOW() - INTERVAL 25 MINUTE, 'mesa'), (9102, 'PENDIENTE', NOW() - INTERVAL 10 MINUTE, NOW() - INTERVAL 10 MINUTE, 'mesa'), (9103, 'EN PREPARACION', NOW() - INTERVAL 30 MINUTE, NOW() - INTERVAL 15 MINUTE, 'mesa'), (9104, 'LISTO', NOW() - INTERVAL 45 MINUTE, NOW() - INTERVAL 25 MINUTE, 'mesa'), (9105, 'ENTREGADO', NOW() - INTERVAL 3 HOUR, NOW() - INTERVAL 140 MINUTE, 'mesa'), (9106, 'ENTREGADO', NOW() - INTERVAL 1 DAY, NOW() - INTERVAL 1410 MINUTE, 'mesa');
INSERT IGNORE INTO PedidoMesa (id_pedido_mesa, Mesa_id_mesa, Pedido_id_pedido) VALUES (9101, 9101, 9101), (9102, 9102, 9102), (9103, 9103, 9103), (9104, 9104, 9104), (9105, 9105, 9105), (9106, 9105, 9106);
INSERT IGNORE INTO DetallePedido (id_detalle_pedido, cantidad, notas, Pedido_id_pedido, Producto_idProducto) VALUES (9101, 2, 'Sin cebolla', 9101, 9101), (9102, 2, NULL, 9101, 9103), (9103, 1, 'Sopa sin cilantro, por favor', 9102, 9102), (9104, 1, NULL, 9103, 9101), (9105, 1, 'Muy caliente', 9104, 9102), (9106, 2, NULL, 9105, 9101), (9107, 2, NULL, 9105, 9103), (9108, 2, NULL, 9106, 9101), (9109, 1, NULL, 9106, 9102), (9110, 2, 'Sin hielo', 9106, 9103);
INSERT IGNORE INTO Pago (id_pago, monto, metodo_pago, fecha_pago, Pedido_id_pedido, Caja_id_caja) VALUES (9101, 68000, 'Efectivo', NOW() - INTERVAL 130 MINUTE, 9105, 9101), (9102, 80000, 'Tarjeta', NOW() - INTERVAL 1 DAY, 9106, 9101);
INSERT IGNORE INTO Usuario (idUsuario, nombre, credenciales) VALUES (9105, 'Mario Mesero', '1234'), (9106, 'Rita Repartidora', '1234');
INSERT IGNORE INTO Mesero (id_mesero, zona_asignada, Usuario_idUsuario) VALUES (9101, 'Salón principal', 9105);
INSERT IGNORE INTO Repartidor (id_repartidor, placa_vehiculo, Usuario_idUsuario) VALUES (9101, 'ABC123', 9106);
