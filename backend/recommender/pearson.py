import sys
from pathlib import Path

import numpy as np
import pandas as pd


# Permite ejecutar este archivo desde la raíz del proyecto
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))


def calcular_pearson_vectores(ratings_a, ratings_b, min_comunes=2):
    """
    Calcula la correlación de Pearson entre dos usuarios.

    Parámetros:
        ratings_a: Serie de pandas o diccionario {movieId: rating}
        ratings_b: Serie de pandas o diccionario {movieId: rating}
        min_comunes: mínimo de películas en común para comparar

    Retorna:
        similitud, cantidad de películas en común
    """
    usuario_a = pd.Series(ratings_a, dtype=float).dropna()
    usuario_b = pd.Series(ratings_b, dtype=float).dropna()

    peliculas_comunes = usuario_a.index.intersection(usuario_b.index)

    if len(peliculas_comunes) < min_comunes:
        return 0, len(peliculas_comunes)

    valores_a = usuario_a.loc[peliculas_comunes]
    valores_b = usuario_b.loc[peliculas_comunes]

    if valores_a.std() == 0 or valores_b.std() == 0:
        return 0, len(peliculas_comunes)

    similitud = np.corrcoef(valores_a, valores_b)[0, 1]

    if np.isnan(similitud):
        return 0, len(peliculas_comunes)

    return float(similitud), len(peliculas_comunes)


def calcular_pearson_usuario(matriz, calificaciones_usuario_nuevo, user_id, min_comunes=2):
    """
    Calcula la similitud de Pearson entre el usuario nuevo
    y un usuario existente de la matriz usuario-película.

    Parámetros:
        matriz: DataFrame usuario-película
        calificaciones_usuario_nuevo: diccionario {movieId: rating}
        user_id: usuario existente
        min_comunes: mínimo de películas en común

    Retorna:
        similitud, cantidad de películas en común
    """
    if user_id not in matriz.index:
        return 0, 0

    usuario_existente = matriz.loc[user_id].dropna()

    return calcular_pearson_vectores(
        calificaciones_usuario_nuevo,
        usuario_existente,
        min_comunes=min_comunes
    )


def obtener_usuarios_similares(
    matriz,
    calificaciones_usuario_nuevo,
    min_comunes=2,
    top_k=10,
    solo_positivos=True
):
    """
    Compara al usuario nuevo contra todos los usuarios existentes.

    Parámetros:
        matriz: DataFrame usuario-película
        calificaciones_usuario_nuevo: diccionario {movieId: rating}
        min_comunes: mínimo de películas en común
        top_k: cantidad máxima de usuarios similares
        solo_positivos: si True, solo toma similitudes mayores a 0

    Retorna:
        DataFrame con columnas:
        userId, similitud, peliculas_en_comun
    """
    usuarios_similares = []

    for user_id in matriz.index:
        similitud, comunes = calcular_pearson_usuario(
            matriz,
            calificaciones_usuario_nuevo,
            user_id,
            min_comunes=min_comunes
        )

        if solo_positivos and similitud <= 0:
            continue

        if not solo_positivos and similitud == 0:
            continue

        usuarios_similares.append({
            "userId": user_id,
            "similitud": round(similitud, 4),
            "peliculas_en_comun": comunes
        })

    df_similares = pd.DataFrame(usuarios_similares)

    if df_similares.empty:
        return df_similares

    df_similares = df_similares.sort_values(
        by=["similitud", "peliculas_en_comun"],
        ascending=False
    )

    return df_similares.head(top_k).reset_index(drop=True)


def obtener_rating_usuario(matriz, user_id, movie_id):
    """
    Obtiene el rating de un usuario para una película.
    Si no existe, retorna None.
    """
    if user_id not in matriz.index:
        return None

    if movie_id not in matriz.columns:
        return None

    rating = matriz.loc[user_id, movie_id]

    if pd.isna(rating):
        return None

    return float(rating)


def explicar_similitud(matriz, calificaciones_usuario_nuevo, user_id, min_comunes=2):
    """
    Muestra las películas en común entre el usuario nuevo y un usuario existente.
    Sirve para justificar la similitud calculada.
    """
    if user_id not in matriz.index:
        return pd.DataFrame()

    usuario_nuevo = pd.Series(calificaciones_usuario_nuevo, dtype=float)
    usuario_existente = matriz.loc[user_id].dropna()

    peliculas_comunes = usuario_nuevo.index.intersection(usuario_existente.index)

    if len(peliculas_comunes) < min_comunes:
        return pd.DataFrame()

    datos = []

    for movie_id in peliculas_comunes:
        datos.append({
            "movieId": int(movie_id),
            "rating_usuario_nuevo": float(usuario_nuevo.loc[movie_id]),
            "rating_usuario_existente": float(usuario_existente.loc[movie_id])
        })

    return pd.DataFrame(datos)


def prueba_pearson():
    """
    Prueba rápida del módulo desde consola.
    """
    from backend.recommender.data_loader import (
        preparar_matriz_usuario_pelicula,
        validar_calificaciones_usuario,
    )

    matriz, ratings, movies = preparar_matriz_usuario_pelicula()

    calificaciones_usuario_nuevo = {
        4993: 5.0,
        5952: 4.5,
        7153: 5.0,
        6377: 4.0,
        58559: 4.5
    }

    calificaciones_usuario_nuevo = validar_calificaciones_usuario(
        calificaciones_usuario_nuevo,
        matriz
    )

    print("PRUEBA DEL MÓDULO PEARSON")
    print("=" * 60)

    print("\nPelículas calificadas por el usuario nuevo:")
    print(calificaciones_usuario_nuevo)

    usuarios_similares = obtener_usuarios_similares(
        matriz=matriz,
        calificaciones_usuario_nuevo=calificaciones_usuario_nuevo,
        min_comunes=2,
        top_k=10
    )

    print("\nUsuarios más similares:")
    print(usuarios_similares)

    if not usuarios_similares.empty:
        primer_usuario = usuarios_similares.iloc[0]["userId"]

        print(f"\nExplicación de similitud con el usuario {primer_usuario}:")
        explicacion = explicar_similitud(
            matriz,
            calificaciones_usuario_nuevo,
            primer_usuario
        )

        explicacion = explicacion.merge(
            movies,
            on="movieId",
            how="left"
        )

        print(explicacion[[
            "movieId",
            "title",
            "rating_usuario_nuevo",
            "rating_usuario_existente"
        ]])


if __name__ == "__main__":
    prueba_pearson()