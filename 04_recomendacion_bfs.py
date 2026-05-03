#%%
# ============================================================
# Objetivo:
# Implementar una recomendación de películas usando la lógica de
# BFS sobre un grafo bipartito Usuario-Película.
#
# El recorrido se interpreta así:
#
# Nivel 0: Usuario objetivo
# Nivel 1: Películas calificadas positivamente por el usuario
# Nivel 2: Usuarios similares que calificaron esas mismas películas
# Nivel 3: Películas candidatas calificadas positivamente por usuarios similares
# ============================================================

# ============================================================
# 1. Importar librerías
# ============================================================

import pandas as pd
import networkx as nx
from collections import deque, defaultdict

#%%
# ============================================================
# 2. Cargar dataset y grafo bipartito
# ============================================================

# Dataset preprocesado
df_2000 = pd.read_csv("data/peliculas_2000.csv")

# Grafo construido en el archivo 03_grafo_bipartito_con_networkx.py
G = nx.read_gml("data/grafo_bipartito_peliculas.gml")

print("Dataset y grafo cargados correctamente.")
print("Cantidad de registros:", len(df_2000))
print("Cantidad de nodos:", G.number_of_nodes())
print("Cantidad de aristas:", G.number_of_edges())


#%%
# ============================================================
# 3. Separar usuarios y películas del grafo
# ============================================================

usuarios_grafo = [
    n for n, d in G.nodes(data=True)
    if d["tipo"] == "usuario"
]

peliculas_grafo = [
    n for n, d in G.nodes(data=True)
    if d["tipo"] == "pelicula"
]

print("Usuarios en el grafo:", len(usuarios_grafo))
print("Películas en el grafo:", len(peliculas_grafo))


#%%
# ============================================================
# 4. Seleccionar usuario objetivo
# ============================================================

# Para la prueba inicial, se elige el usuario con más conexiones.
# Esto permite obtener más información para generar recomendaciones.

usuario_objetivo = max(usuarios_grafo, key=lambda u: G.degree(u))

print("Usuario objetivo seleccionado:", usuario_objetivo)
print("Cantidad de películas calificadas:", G.degree(usuario_objetivo))

#%%
# ============================================================
# 5. Función auxiliar: obtener rating de una arista
# ============================================================

def obtener_rating(G, nodo1, nodo2):
    """
    Devuelve el rating almacenado en la arista entre nodo1 y nodo2.
    Si no existe rating, retorna 0.
    """
    return G[nodo1][nodo2].get("rating", 0)


#%%
# ============================================================
# 6. Recomendación usando lógica BFS
# ============================================================

def recomendar_peliculas_bfs(G, usuario_objetivo, rating_min=4.0, top_n=10):
    """
    Recomienda películas usando una lógica basada en BFS
    sobre un grafo bipartito Usuario-Película.

    Parámetros:
    - G: grafo bipartito construido con NetworkX.
    - usuario_objetivo: nodo del usuario objetivo, por ejemplo 'U_1'.
    - rating_min: calificación mínima considerada positiva.
    - top_n: cantidad de recomendaciones a devolver.

    Retorna:
    - DataFrame con las películas recomendadas.
    """

    # ------------------------------------------------------------
    # Nivel 0: usuario objetivo
    # ------------------------------------------------------------

    if usuario_objetivo not in G:
        print("El usuario objetivo no existe en el grafo.")
        return pd.DataFrame()

    # ------------------------------------------------------------
    # Nivel 1: películas calificadas positivamente por el usuario
    # ------------------------------------------------------------

    peliculas_usuario = set()
    peliculas_positivas_usuario = set()

    for pelicula in G.neighbors(usuario_objetivo):
        if G.nodes[pelicula]["tipo"] == "pelicula":
            peliculas_usuario.add(pelicula)

            rating = obtener_rating(G, usuario_objetivo, pelicula)

            if rating >= rating_min:
                peliculas_positivas_usuario.add(pelicula)

    print("Películas calificadas por el usuario:", len(peliculas_usuario))
    print("Películas positivas del usuario:", len(peliculas_positivas_usuario))

    if len(peliculas_positivas_usuario) == 0:
        print("El usuario no tiene suficientes películas con calificación positiva.")
        return pd.DataFrame()

    # ------------------------------------------------------------
    # Nivel 2: usuarios similares
    # ------------------------------------------------------------

    usuarios_similares = set()

    for pelicula in peliculas_positivas_usuario:
        for usuario in G.neighbors(pelicula):
            if (
                usuario != usuario_objetivo
                and G.nodes[usuario]["tipo"] == "usuario"
            ):
                rating = obtener_rating(G, usuario, pelicula)

                if rating >= rating_min:
                    usuarios_similares.add(usuario)

    print("Usuarios similares encontrados:", len(usuarios_similares))

    if len(usuarios_similares) == 0:
        print("No se encontraron usuarios similares.")
        return pd.DataFrame()

    # ------------------------------------------------------------
    # Nivel 3: películas candidatas
    # ------------------------------------------------------------

    peliculas_candidatas = defaultdict(list)

    for usuario in usuarios_similares:
        for pelicula in G.neighbors(usuario):
            if G.nodes[pelicula]["tipo"] == "pelicula":

                # No recomendar películas que el usuario objetivo ya calificó
                if pelicula in peliculas_usuario:
                    continue

                rating = obtener_rating(G, usuario, pelicula)

                if rating >= rating_min:
                    peliculas_candidatas[pelicula].append(rating)

    print("Películas candidatas encontradas:", len(peliculas_candidatas))

    if len(peliculas_candidatas) == 0:
        print("No se encontraron películas candidatas.")
        return pd.DataFrame()

    # ------------------------------------------------------------
    # Ranking de recomendaciones
    # ------------------------------------------------------------

    recomendaciones = []

    for pelicula, ratings in peliculas_candidatas.items():
        datos_pelicula = G.nodes[pelicula]

        rating_promedio = sum(ratings) / len(ratings)
        cantidad_votos = len(ratings)

        recomendaciones.append({
            "movie_node": pelicula,
            "titulo": datos_pelicula.get("titulo", pelicula),
            "year": datos_pelicula.get("year", ""),
            "generos": datos_pelicula.get("generos", ""),
            "rating_promedio": round(rating_promedio, 2),
            "cantidad_votos_similares": cantidad_votos
        })

    recomendaciones_df = pd.DataFrame(recomendaciones)

    recomendaciones_df = recomendaciones_df.sort_values(
        by=["rating_promedio", "cantidad_votos_similares"],
        ascending=False
    )

    return recomendaciones_df.head(top_n)


#%%
# ============================================================
# 7. Ejecutar recomendación
# ============================================================

recomendaciones = recomendar_peliculas_bfs(
    G,
    usuario_objetivo=usuario_objetivo,
    rating_min=4.0,
    top_n=10
)

print("\n========== RECOMENDACIONES ==========")
print(recomendaciones)
print("=====================================\n")


#%%
# ============================================================
# 8. Mostrar explicación del recorrido BFS aplicado
# ============================================================

print("Interpretación del recorrido BFS aplicado:")
print("Nivel 0: Usuario objetivo:", usuario_objetivo)
print("Nivel 1: Películas calificadas positivamente por el usuario.")
print("Nivel 2: Usuarios similares que calificaron positivamente esas películas.")
print("Nivel 3: Películas candidatas calificadas positivamente por usuarios similares.")


#%%
# ============================================================
# 9. Implementación explícita de BFS hasta profundidad 3
# ============================================================

def bfs_limitado(G, inicio, profundidad_max=3):
    """
    Realiza BFS desde un nodo inicial hasta una profundidad máxima.

    Retorna:
    - visitados: conjunto de nodos visitados
    - niveles: diccionario con el nivel de cada nodo
    - padres: diccionario con el padre de cada nodo en el recorrido
    """

    visitados = set()
    niveles = {}
    padres = {}

    cola = deque()

    visitados.add(inicio)
    niveles[inicio] = 0
    padres[inicio] = None
    cola.append(inicio)

    while cola:
        nodo_actual = cola.popleft()
        nivel_actual = niveles[nodo_actual]

        if nivel_actual == profundidad_max:
            continue

        for vecino in G.neighbors(nodo_actual):
            if vecino not in visitados:
                visitados.add(vecino)
                niveles[vecino] = nivel_actual + 1
                padres[vecino] = nodo_actual
                cola.append(vecino)

    return visitados, niveles, padres


visitados, niveles, padres = bfs_limitado(
    G,
    inicio=usuario_objetivo,
    profundidad_max=3
)

print("\n========== BFS LIMITADO ==========")
print("Nodos visitados hasta profundidad 3:", len(visitados))

niveles_conteo = defaultdict(int)

for nodo, nivel in niveles.items():
    niveles_conteo[nivel] += 1

for nivel in sorted(niveles_conteo.keys()):
    print(f"Nivel {nivel}: {niveles_conteo[nivel]} nodos")

print("=================================\n")


#%%
# ============================================================
# 10. Guardar recomendaciones en CSV
# ============================================================

recomendaciones.to_csv("data/recomendaciones_bfs.csv", index=False)

print("Recomendaciones guardadas en: data/recomendaciones_bfs.csv")
# %%
