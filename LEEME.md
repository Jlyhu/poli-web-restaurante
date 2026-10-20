# Entrega: Administrador, Cocinero, PedidoMesa, DetallePedido, Pago

Copiar las carpetas `orm/` y `rest/` a la raíz del repo (se mezclan con las que ya existen; no pisan nada de Cliente).

## ORM  (orm/modelos, orm/dao, orm/consola)
Desde la raíz del repo, con el .venv activo:
    python -m orm.consola.ConsolaCocinero      (igual con Administrador, PedidoMesa, DetallePedido, Pago)

## REST  (rest/modelos, rest/schemas, rest/routes)
1. Ejecutar `rest/datos_prueba.sql` en MySQL Workbench (crea los registros "padre" para las pruebas).
2. NO hay que registrar nada: mainService.py registra solo todos los archivos rest/routes/*Routes.py.
3. Arrancar el servicio desde la RAÍZ del repo (los imports parten de ahí):
       python -m rest.mainService
   Probar en el navegador: http://localhost:5000/getCocineros
4. En Postman: Import -> `rest/PoliRestaurante.postman_collection.json`.

Rutas por entidad: get<Plural>, get<Entidad>/<id>, insert<Entidad>, update<Entidad>/<id>, delete<Entidad>/<id>
(ej.: /getCocineros, /getCocinero/9001, /insertCocinero, /updateCocinero/9001, /deleteCocinero/9001)
