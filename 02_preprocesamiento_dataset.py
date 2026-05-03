"""si les sale error descarguen esto desde el CMD: pip install pandas"""
# Cargar el dataset con Pandas
import pandas as pd
import os

# Crear la carpeta 'data' si no existe
if not os.path.exists('data'):
    os.makedirs('data')
    print("Carpeta 'data' creada con éxito.")

# 3. Cargar archivos principales
ratings = pd.read_csv("ml-latest-small/ratings.csv")
movies = pd.read_csv("ml-latest-small/movies.csv")

""" Lo comentado es para revisar los datos, no es necesario 
para el proceso de creación del grafo. 
# print(ratings.head())
# print(movies.head())

# # Revisar tamaño del dataset
# print("Ratings:", ratings.shape)
# print("Películas:", movies.shape)

# print("Usuarios únicos:", ratings["userId"].nunique())
# print("Películas únicas con ratings:", ratings["movieId"].nunique())"""

# 4. Unir ratings con películas
df = ratings.merge(movies, on="movieId")

#print(df.head()) # Revisar la estructura del DataFrame combinado"""

# 5. Extraer año desde el título
df["year"] = df["title"].str.extract(r"\((\d{4})\)")
df["year"] = pd.to_numeric(df["year"], errors="coerce")

#print(df[["title", "year"]].head()) # Revisar que el año se haya extraído correctamente

# 6. Filtrar películas desde el año 2000
df_2000 = df[df["year"] >= 2000].copy()

df_2000.to_csv("data/peliculas_2000.csv", index=False) # Guardar el dataset preprocesado en un nuevo archivo CSV

print("Dataset preprocesado guardado correctamente.")

# """# 7. Verificar nodos contra el requisito de 2500 nodos
# ratings_2000 = len(df_2000)
# usuarios = df_2000["userId"].nunique()
# peliculas = df_2000["movieId"].nunique()
# total_nodos = usuarios + peliculas
# aristas = len(df_2000)

# print("Ratings desde el año 2000:", ratings_2000)
# print("Usuarios únicos:", usuarios)
# print("Películas únicas:", peliculas)
# print("Total de nodos:", total_nodos)
# print("Total de aristas:", aristas)

# if total_nodos >= 2500:
#     print("El dataset cumple con el mínimo requerido de 2500 nodos.")
# else:
#     print("El dataset no cumple con el mínimo requerido.")"""