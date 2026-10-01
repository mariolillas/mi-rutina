# Radar de microapps para México

Scripts para medir, con datos públicos de la App Store de México, qué nichos de apps tienen demanda, quién los domina y de qué se quejan los usuarios. Versión interactiva del informe: https://claude.ai/artifact/D5pkUvGza9iDQCtabotzsv. Una copia local está en [`radar-microapps.html`](radar-microapps.html) y los datos resumidos en [`datos/`](datos/).

## Cómo correrlo

Desde la carpeta `scripts/`, con Python 3 y sin dependencias:

1. `python3 fetch_search.py`: busca cada nicho de `terms.py` en la API pública de búsqueda de iTunes (país `mx`). Apple limita el ritmo de consultas; el script espera y reintenta.
2. `python3 analyze.py`: calcula por nicho la demanda (calificaciones de las apps relevantes), la calidad de los líderes, la antigüedad de sus actualizaciones y cuántas apps son recién llegadas.
3. `python3 fetch_charts.py` y `python3 charts_analysis.py`: bajan las listas de más ingresos y más descargadas por categoría y marcan las apps populares pero mal calificadas.
4. `python3 fetch_reviews.py lista.json` y `python3 reviews_analysis.py lista.json salida.json`: leen las reseñas recientes de México de las apps que elijas y cuentan de qué se quejan.

## Límites

- Solo cubre la App Store. En México Android es 78% de los celulares (StatCounter, junio 2026).
- Las calificaciones son una medida indirecta de uso, no de descargas ni de ingresos.
- La relevancia de cada app para un nicho se decide con una regla simple sobre su nombre y descripción.
- Las reseñas recientes son una muestra chica por app.

## Resultados (30 sep al 1 oct 2026)

- Se midieron 65 nichos y 784 apps relevantes. 302 (39%) se lanzaron en los últimos 12 meses, y 294 de ellas tienen menos de 20 calificaciones.
- En 13 nichos hay 8 o más apps lanzadas en los últimos 12 meses (costeo de recetas, cotizaciones, cuentas por cobrar, calculadora de materiales, mantenimiento de auto, inventario para Mercado Libre, citas de salón, catálogo y pedidos por WhatsApp, etiquetas de envío, examen de admisión, presupuesto de obra y de boda). De 144 apps nuevas, solo 1 tiene 100 calificaciones o más.
- 99% de las apps de estos nichos se descarga gratis. Treinta, Abona, tiendita.app y Tiendatek ya cubren tienditas, fiado y punto de venta.
- Hay apps chicas entre las que más ingresos generan en México: rastreadores de paquetes (3 de las 6 de Compras), finanzas (Quanto, Finno, Kelo), escáneres de PDF, ENARMaster y Cruce Directo Garitas.
- Las reseñas recientes muestran descontento con el líder en agenda para salones y barberías (AgendaPro 2.45★, WeiBook 2.21★, SalonAppy 3.13★), en el rastreo de paquetes de más ingresos (1.75★ en sus últimas 51 reseñas) y en las garitas (1.93★).
- Las apps populares y odiadas de bancos, afores, telefónicas, servicios y gobierno no se pueden reemplazar: dependen de la cuenta de cada persona con la empresa.

Recomendación: plan principal con el servicio de contenido más herramientas a la medida para esos mismos clientes, y dos pruebas antes de programar: un rastreador de paquetes en español y una agenda para estéticas y barberías con recordatorios por WhatsApp. Son hipótesis, no resultados.
