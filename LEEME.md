# Guía rápida — PoliRestaurante

1. Instala dependencias: `pip install -r requirements.txt`.
2. Copia `.env.example` a `.env` y configura la conexión a MySQL.
3. Ejecuta `polirestaurante.sql` y después `rest/datos_prueba.sql` en MySQL Workbench.
4. Desde la raíz del proyecto, inicia Flask con `python -m rest.mainService`.
5. Prueba `http://127.0.0.1:5000/health` y luego importa `rest/PoliRestaurante.postman_collection.json` en Postman.
6. Para probar los DAO, ejecuta los módulos `orm.consola.ConsolaAdministrador`, `ConsolaCocinero`, `ConsolaDetallePedido`, `ConsolaPago` o `ConsolaPedidoMesa` con `python -m`.

Las tablas usan identificadores no autoincrementales. La API calcula un siguiente ID para facilitar las pruebas, pero `MAX(id)+1` puede tener colisiones con solicitudes simultáneas.
