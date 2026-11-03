-- Datos de DEMOSTRACIÓN para HU-05, HU-06, HU-07, HU-15, Cajero y Repartidor (ids 9201 en adelante).
-- Necesita antes rest/datos_demo_hu.sql (usa Mario Mesero 9101, Rita Repartidora 9101, Cajero Demo 9101 y los productos 9101-9103).
-- Se puede ejecutar varias veces (INSERT IGNORE).
-- Cargar con:  python cargar_datos_prueba.py rest/datos_demo_daniela.sql
INSERT IGNORE INTO Cliente (id_cliente, nombre, direccion, telefono) VALUES (9201, 'Sofía Ramírez', 'Calle 57 # 12-30 Apto 402', '3104567890'), (9202, 'Andrés Gómez', 'Carrera 7 # 45-10', '3209876543');
INSERT IGNORE INTO Mesa (id_mesa, numero, estado) VALUES (9201, 201, 'Disponible'), (9202, 202, 'Disponible'), (9203, 203, 'Disponible');
INSERT IGNORE INTO Pedido (id_pedido, estado, fecha_creacion, fecha_ultima_actualizacion, tipo_pedido, Mesero_id_mesero) VALUES (9201, 'LISTO', NOW() - INTERVAL 40 MINUTE, NOW() - INTERVAL 5 MINUTE, 'mesa', 9101), (9202, 'PENDIENTE', NOW() - INTERVAL 8 MINUTE, NOW() - INTERVAL 8 MINUTE, 'mesa', 9101), (9203, 'ENTREGADO', NOW() - INTERVAL 70 MINUTE, NOW() - INTERVAL 20 MINUTE, 'mesa', 9101);
INSERT IGNORE INTO Pedido (id_pedido, estado, fecha_creacion, fecha_ultima_actualizacion, tipo_pedido, Repartidor_id_repartidor, Cliente_id_cliente) VALUES (9204, 'LISTO', NOW() - INTERVAL 35 MINUTE, NOW() - INTERVAL 3 MINUTE, 'domicilio', 9101, 9201), (9205, 'EN PREPARACION', NOW() - INTERVAL 15 MINUTE, NOW() - INTERVAL 10 MINUTE, 'domicilio', 9101, 9202);
INSERT IGNORE INTO PedidoMesa (id_pedido_mesa, Mesa_id_mesa, Pedido_id_pedido) VALUES (9201, 9201, 9201), (9202, 9202, 9202), (9203, 9203, 9203);
INSERT IGNORE INTO DetallePedido (id_detalle_pedido, cantidad, notas, Pedido_id_pedido, Producto_idProducto) VALUES (9201, 1, NULL, 9201, 9101), (9202, 1, NULL, 9201, 9103), (9203, 2, 'Una sin sal', 9202, 9102), (9204, 3, NULL, 9203, 9101), (9205, 3, 'Con poco hielo', 9203, 9103), (9206, 2, NULL, 9204, 9101), (9207, 1, 'Bien caliente', 9205, 9102);
