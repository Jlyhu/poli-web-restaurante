# Entrega: HU-02, HU-03 (+HU-04), HU-08, HU-09 y HU-14

Entidades: **PedidoMesa, DetallePedido, Cocinero, Administrador, Pago**.
Copiar las carpetas de este zip a la raíz del repo (mezclan con las existentes).

| HU | Pantalla | Entidades que usa |
|----|----------|-------------------|
| HU-02 Crear pedido | `crear-pedido.html` | PedidoMesa (+ Pedido y Mesa) |
| HU-03 Productos del pedido / HU-04 Observaciones | `productos-pedido.html` (`observaciones.html` redirige ahí) | DetallePedido |
| HU-08 Pedidos pendientes y su detalle | `pedidos-pendientes.html` | Pedido, DetallePedido |
| HU-09 Estado de preparación | `estado-preparacion.html` | Cocinero, Pedido |
| HU-14 Reportes (ventas y tiempos) | `reportes.html` | Administrador, Pago |

## Cómo probarlo
1. `pip install -r requirements.txt` y el `.env` con los datos de MySQL (igual que antes).
2. Cargar datos de demostración (ids 9101+, se puede repetir sin duplicar):
   `python cargar_datos_prueba.py rest/datos_demo_hu.sql`
3. Servicio, desde la **raíz** del repo: `python -m rest.mainService`  → http://localhost:5000
4. Cliente: abrir `cliente/crear-pedido.html` con Live Server (puerto 5500).

Flujo completo: crear pedido (HU-02) → agregar productos y observaciones (HU-03/04) → en cocina verlo en pendientes (HU-08) → iniciar preparación y marcarlo listo (HU-09). Los reportes (HU-14) muestran pagos de pedidos ENTREGADOS.

## Endpoints nuevos
| Método y ruta | Para qué |
|---|---|
| `GET /getMesasDisponibilidad` | Mesas con `disponible` (una mesa está ocupada si tiene pedido PENDIENTE, EN PREPARACION o LISTO) |
| `POST /crearPedidoMesa` `{Mesa_id_mesa}` | Crea Pedido PENDIENTE + PedidoMesa en una sola transacción. 400 sin mesa, 409 si la mesa ya tiene pedido activo |
| `GET /getPedidosConMesa?estado=&activos=1` | Pedidos con número de mesa, del más antiguo al más reciente |
| `GET /getDetallePedidoConProducto/<id_pedido>` | Renglones con nombre, precio, subtotal y total |
| `GET /getDetallesPedido?pedido=<id>` | (existente) ahora acepta el filtro `pedido` |
| `GET /reporteVentas?administrador=&desde=&hasta=` | Total, pagos y total por método de pedidos ENTREGADOS |
| `GET /reporteTiempos?administrador=&desde=&hasta=` | Minutos por pedido LISTO/ENTREGADO y promedio |

Cambios de reglas en rutas existentes (`DetallePedidoRoutes.py`): agregar, cambiar o quitar renglones solo si el pedido está PENDIENTE (409 con el motivo); el producto debe existir, no estar agotado y alcanzar en unidades; si se repite el mismo producto sin observación distinta se suma la cantidad. Para cambiar el estado se sigue usando `PUT /cambiarEstadoPedido/<id>` (ya valida el orden PENDIENTE → EN PREPARACION → LISTO → ENTREGADO).

## Archivos que ya existían y se tocaron (revisar al fusionar)
- `rest/mainService.py`: tenía **dos versiones pegadas** (merge) y la activa **no registraba PedidoRoutes**. Quedó una sola versión que registra automáticamente todos los `*Routes.py`.
- `rest/routes/DetallePedidoRoutes.py`, `rest/routes/PedidoMesaRoutes.py`, `rest/schemas/DetallePedidoSchema.py` (`notas` admite null).
- `cliente/js/config.js` (endpoints nuevos al final) y `cliente/css/styles.css` (bloque nuevo al final).
- `cargar_datos_prueba.py` ahora acepta la ruta de un .sql como argumento.

## Estructura MVC nueva en `cliente/js/`
- models: `Http.js` (fetch compartido), `Pedido`, `PedidoModel`, `DetallePedido`, `DetallePedidoModel`, `Cocinero`, `Administrador`, `PersonalModel`, `Pago`, `ReporteModel`
- views: `BaseView` (avisos, fechas, dinero, badges), `DetallePanelView`, `CrearPedidoView`, `ProductosPedidoView`, `PendientesView`, `PreparacionView`, `ReportesView`
- controllers: `CrearPedido`, `ProductosPedido`, `Pendientes`, `Preparacion`, `Reportes` + un `app-*.js` por página

## Limitaciones conocidas (hablarlo con el equipo)
1. **No hay historial de estados** (RF-21/22/23, HU-15). HU-09 actualiza `fecha_ultima_actualizacion`, pero no se guarda *quién* cambió el estado: el cocinero elegido solo aparece en el mensaje. Y el reporte de tiempos mide creación → última actualización, no cada tramo. Con una tabla `HistorialEstadoPedido` ambas cosas quedarían exactas.
2. **Sin sesión:** el login actual no guarda el usuario. Por eso HU-09 pide elegir el cocinero y HU-14 el administrador (el servicio verifica que exista en la tabla Administrador, 403 si no). Cuando el login guarde `usuario.rol` y el id, esos selectores se llenan solos.
3. El pedido se crea sin mesero (`Mesero_id_mesero` queda vacío); el servicio ya acepta el campo.
4. Agregar productos no descuenta `cantidad_disponible` (solo valida que alcance).
5. `rest/utils.py` también tiene dos versiones pegadas (la última sobrescribe a la primera); no lo toqué.
