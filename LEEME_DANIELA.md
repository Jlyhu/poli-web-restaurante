# Daniela: HU-05, HU-06, HU-07, HU-15 + pantallas de Cajero y Repartidor

Con esto todos los botones del diagrama de navegación quedan activos, menos **reservas** (no está en las 15 HU).

## Cómo probarlo
1. `pip install -r requirements.txt` (ahora incluye **flask-cors**, que faltaba).
2. Datos de demostración (primero los de Angie, luego los míos; se pueden repetir):
   ```
   python cargar_datos_prueba.py rest/datos_demo_hu.sql
   python cargar_datos_prueba.py rest/datos_demo_daniela.sql
   ```
3. Desde la raíz: `python -m rest.mainService`
4. `cliente/login.html` con Live Server. Contraseña de todos: `1234`.

| Entrar como | Pantalla | Qué probar |
|---|---|---|
| Mario Mesero | `estado-pedido.html` | HU-05 ver estado y detalle · HU-06 **Entregar** el 9201 (LISTO) · HU-07 **Cancelar** el 9202 (pide confirmar) |
| Mario Mesero | `mesas.html` | Ver mesas libres / ocupadas |
| Ana Administradora | `trazabilidad.html` | HU-15: filtros, línea de tiempo, mesero, tiempo y pago de cada pedido |
| Cajero Demo | `pagos.html` | Cobrar pedidos ENTREGADOS (el monto lo calcula el servidor) |
| Cajero Demo | `caja.html` | Ver lo recaudado, cerrar la caja y abrir una nueva |
| Rita Repartidora | `entregas.html` | Domicilios asignados con dirección y teléfono; entregar el 9204 |

## Pantallas → MVC (cliente/js)
| Pantalla | Modelo | Vista | Controlador | Arranque |
|---|---|---|---|---|
| estado-pedido.html | SeguimientoModel + DetallePedidoModel | EstadoPedidoView + DetallePanelView | EstadoPedidoController | app-estado-pedido.js |
| trazabilidad.html | SeguimientoModel + DetallePedidoModel | TrazabilidadView + DetallePanelView | TrazabilidadController | app-trazabilidad.js |
| pagos.html | SeguimientoModel + CajaModel | PagosView | PagosController | app-pagos.js |
| caja.html | CajaModel | CajaView | CajaController | app-caja.js |
| entregas.html | SeguimientoModel + DetallePedidoModel | EntregasView + DetallePanelView | EntregasController | app-entregas.js |
| mesas.html | PedidoModel (ya existía) | MesasView | MesasController | app-mesas.js |

Entidad nueva: `PedidoDetallado.js` (con las reglas `sePuedeEntregar()` y `sePuedeCancelar()`).

## Endpoints nuevos (`rest/routes/SeguimientoRoutes.py`)
| Método y ruta | Para qué |
|---|---|
| `GET /getPedidosDetallados?estado=&activos=1&mesero=&repartidor=&tipo=&sinPago=1` | Pedido + mesa + mesero + repartidor + cliente + total + pago |
| `GET /getEstadoPedido/<id>` | HU-05 |
| `GET /getTrazabilidadPedido/<id>` | HU-15: fechas, eventos y minutos |
| `PUT /entregarPedido/<id>` | HU-06: solo LISTO → ENTREGADO (409 si no) |
| `PUT /cancelarPedido/<id>` | HU-07: PENDIENTE / EN PREPARACION → CANCELADO (409 si no) |
| `GET /getCajaAbierta?cajero=<id>` | Caja sin cerrar, con pagos, recaudado y esperado |
| `POST /abrirCaja` `{Cajero_id_cajero, monto_inicial}` | 409 si ya tiene una abierta |
| `POST /registrarPagoPedido` `{Pedido_id_pedido, Cajero_id_cajero, metodo_pago}` | Solo pedidos ENTREGADOS sin pago y con caja abierta; el monto se calcula en el servidor |

Todo está en la colección `rest/postman/PoliRestaurante-Daniela.postman_collection.json`.

## Archivos de otras que toqué (poquito)
- `cliente/js/core/permisos.js`: los `null` de mis botones ahora apuntan a sus pantallas.
- `cliente/js/config.js`: endpoints nuevos al final.
- `cliente/js/views/BaseView.js`: badge `PAGADO`.
- `cliente/js/views/DetallePanelView.js`: el subtítulo dice "Domicilio · cliente" cuando no hay mesa.
- `cliente/css/styles.css`: bloque nuevo al final.
- `requirements.txt`: agregado `flask-cors`.
