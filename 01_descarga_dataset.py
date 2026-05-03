import os
import zipfile
import urllib.request
# 1. Descargar dataset movieLens
url = "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
zip_path = "ml-latest-small.zip"
extract_path = "ml-latest-small"

# Descargar el archivo ZIP
urllib.request.urlretrieve(url, zip_path)

# Descomprimir el ZIP
with zipfile.ZipFile(zip_path, "r") as zip_ref:
    zip_ref.extractall(".")

print("Dataset descargado y descomprimido correctamente.")

# """Comprobar que el dataset se ha descargado 
# y descomprimido correctamente listando los 
# archivos en el directorio."""

print(os.listdir("ml-latest-small"))