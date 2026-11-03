# Acceso por rol + HU-02, 03, 08, 09 y 14

Base: `poli-web-restaurante-main`. Todo lo nuevo vive en `cliente/` y en 4 rutas de `rest/`.

## Cómo probarlo
1. `pip install -r requirements.txt` y el `.env` con los datos de MySQL.
2. Datos de demostración (ids 9101+, se puede repetir):
   `python cargar_datos_prueba.py rest/datos_demo_hu.sql`
3. Desde la raíz del repo: `python -m rest.mainService`  → http://127.0.0.1:5000/health
4. Abrir `cliente/login.html` con Live Server (puerto 5500).

Usuarios de demo (contraseña `1234`): Ana Administradora, Carlos Cocinero, Laura Cocinera,
Mario Mesero, Cajero Demo, Rita Repartidora.

## Estructura = diagrama de navegación
`cliente/js/core/permisos.js` es el diagrama hecho datos (rol → botones → pantalla).
- Login → guarda la sesión (`core/sesion.js`) → `index.html` muestra SOLO los botones del rol.
- `core/guard.js` va en cada pantalla: sin sesión → login; rol sin permiso → inicio; dibuja el menú lateral del rol.
- Botón con `pagina: null` = pantalla del diagrama que aún no existe (sale deshabilitado, "pendiente").
  Para activarlo: poner el nombre del .html en `permisos.js`.

| Rol | Botones |
|---|---|
| Administrador | Gestionar usuarios, productos y categorías, mesas, Consultar reservas*, **Reportes (HU-14)**, Consultar pedidos* |
| Mesero | **Crear pedido (HU-02)**, Ver mesas*, **Agregar/modificar detalles (HU-03/04)**, Consultar estado*, Gestionar reservas* |
| Cocinero | **Ver pedidos pendientes y detalle (HU-08)**, **Cambiar estado del pedido (HU-09)** |
| Cajero / Repartidor | todos pendientes* |

\* pantalla aún no implementada.

## Mis HU (MVC en cliente/js)
| HU | Pantalla | Modelo / Vista / Controlador |
|---|---|---|
| 02 | crear-pedido.html | PedidoModel / CrearPedidoView / CrearPedidoController |
| 03-04 | productos-pedido.html | DetallePedidoModel + ProductoModel / ProductosPedidoView / ProductosPedidoController |
| 08 | pedidos-pendientes.html | PedidoModel + DetallePedidoModel / PendientesView + DetallePanelView / PendientesController |
| 09 | estado-preparacion.html | PedidoModel + PersonalModel / PreparacionView / PreparacionController |
| 14 | reportes.html | ReporteModel + PersonalModel / ReportesView / ReportesController |

Con la sesión: el mesero queda asociado al pedido (HU-02), el cocinero se elige solo (HU-09) y el administrador también (HU-14).

## Limitaciones conocidas
- No hay historial de estados (RF-21/22/23, HU-15): no se guarda quién cambió cada estado y el reporte de tiempos mide creación → última actualización.
- El control de acceso es de interfaz; los endpoints de Flask siguen abiertos (falta validar el rol en el backend).
- Agregar productos valida existencias pero no las descuenta.
