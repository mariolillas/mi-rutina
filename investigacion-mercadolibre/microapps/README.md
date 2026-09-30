# Radar de microapps para México

Scripts para medir, con datos públicos de la App Store de México, qué nichos de apps tienen demanda, quién los domina y de qué se quejan los usuarios. Es un trabajo en curso: el informe con resultados se agrega en esta carpeta cuando termina la recolección.

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
