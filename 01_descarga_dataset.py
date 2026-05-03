import os
import zipfile
import urllib.request

# ============================================================
# CONFIGURACIÓN INICIAL DE DIRECTORIOS
# ============================================================
# Definimos 'data' como la carpeta base del proyecto
if not os.path.exists('data'):
    os.makedirs('data')
    print("Carpeta 'data' creada con éxito.")

# 1. Descargar dataset movieLens
url = "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
zip_path = "ml-latest-small.zip"
extract_path = "data"

# Descargar el archivo ZIP
print(f"Descargando {zip_path}...")
urllib.request.urlretrieve(url, zip_path)

# Descomprimir el ZIP y almacenar los archivos en la carpeta 'ml-latest-small' y esta a a su vez dentro de la carpeta 'data'
with zipfile.ZipFile(zip_path, "r") as zip_ref:
    zip_ref.extractall(extract_path)

print(f"Dataset descomprimido en la carpeta: {extract_path}")

# 4. Verificación
# Listamos el contenido de data/ml-latest-small para asegurar que la ruta es correcta
# para tus siguientes scripts (02 y 03)
check_path = os.path.join(extract_path, "ml-latest-small")
if os.path.exists(check_path):
    print("Contenido verificado en:", check_path)
    print(os.listdir(check_path))