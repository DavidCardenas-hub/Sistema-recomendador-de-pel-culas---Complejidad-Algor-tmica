# Sistema Recomendador de Películas - Complejidad Algorítmica

## Descripción del proyecto

Este proyecto consiste en el desarrollo de un sistema recomendador de películas utilizando Python, grafos, búsqueda en amplitud (BFS) y filtrado colaborativo.

El sistema trabaja con películas estrenadas desde el año 2000 en adelante y utiliza calificaciones de usuarios para generar recomendaciones. Para ello, se emplea el dataset MovieLens y se modela la información como un grafo bipartito, donde los nodos representan usuarios y películas, y las aristas representan las calificaciones otorgadas.

La recomendación se basa en la idea de que usuarios con gustos similares pueden servir como referencia para sugerir nuevas películas. Si un usuario calificó positivamente una película, el sistema busca otros usuarios que también calificaron positivamente esa misma película. Luego, analiza otras películas bien calificadas por esos usuarios similares y las propone como recomendaciones.

Para el uso de imágenes se usó TMDB (https://www.themoviedb.org/)

---

## Curso y grupo

- Curso: Complejidad Algorítmica
- Código: 1ACC0184
- Grupo: 03

---

## Integrantes

- Cardenas Cabrera, Angel David
- Gonzales Galán, Bernabé
- Condori Valeriano, Andy Cristian
- Montesinos Condori, Tony
- Orbegoso Villanueva, Joseph Slater

---
## Dataset utilizado

El proyecto utiliza el dataset **MovieLens latest-small**, publicado por GroupLens.

Archivos principales utilizados:

- `ratings.csv`: contiene las calificaciones realizadas por los usuarios.
- `movies.csv`: contiene información de las películas, como título y género.

A partir de estos archivos se genera el dataset preprocesado:
```text
data/peliculas_2000.csv
```
---
## Técnicas utilizadas

Las técnicas y conceptos principales utilizados son:

- Grafos.
- Grafo bipartito.
- Búsqueda en amplitud (BFS).
- Filtrado colaborativo.
- Análisis de complejidad Big O.
- Representación mediante lista de adyacencia.
- Visualización de grafos con NetworkX, Matplotlib y PyVis.
- Exportación de resultados en CSV y Excel.
---
## Resultados generados

- data/peliculas_2000.csv
- data/recomendaciones_bfs.csv
- data/recomendaciones_bfs.xlsx
- data/grafo_bipartito_peliculas.gml
- grafo_colaborativo.html
- grafo_recomendacion_bfs.html
---
## Librerías utilizadas

Para ejecutar el proyecto se requieren las siguientes librerías de Python:

- `pandas`
- `numpy`
- `networkx`
- `matplotlib`
- `pyvis`
- `openpyxl`
- `ipykernel`

Instalación manual:

```bash
pip install pandas numpy networkx matplotlib pyvis openpyxl ipykernel
```
---
```markdown
## Extensiones recomendadas para Visual Studio Code

Estas extensiones no son obligatorias, pero facilitan la ejecución y visualización del proyecto:

- Python
- Jupyter
- Live Preview

Se pueden instalar desde la pestaña de extensiones de Visual Studio Code. También pueden instalarse desde la terminal con los siguientes comandos:

```bash
code --install-extension ms-python.python
code --install-extension ms-toolsai.jupyter
code --install-extension ms-vscode.live-server
```
---
## Ejecución del proyecto

Ejecutar los scripts en el siguiente orden:

```bash
python 01_descarga_dataset.py
python 02_preprocesamiento_dataset.py
python 03_grafo_bipartito_con_networkx.py
python 04_recomendacion_bfs.py
```
---
## Estructura del proyecto
```text
Sistema-recomendador-de-peliculas/
│
├── data/
│   ├── ml-latest-small/
│   │   ├── links.csv
│   │   ├── movies.csv
│   │   ├── ratings.csv
│   │   ├── README.txt
│   │   └── tags.csv
│   │
│   ├── grafo_bipartito_peliculas.gml
│   ├── peliculas_2000.csv
│   ├── recomendaciones_bfs.csv
│   └── recomendaciones_bfs.xlsx
│
├── 01_descarga_dataset.py
├── 02_preprocesamiento_dataset.py
├── 03_grafo_bipartito_con_networkx.py
├── 04_recomendacion_bfs.py
│
├── grafo_colaborativo.html
├── grafo_recomendacion_bfs.html
├── grafo_completo_3000_nodos.html   # Visualización opcional del grafo completo
│
└── README.md
```
