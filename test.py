import random
import math

def generar_ciudades_dispersas(num_ciudades, rango_x, rango_y):
    """
    Genera un diccionario de ciudades con coordenadas aleatorias.

    Args:
        num_ciudades (int): El número de ciudades a generar.
        rango_x (tuple): Tupla (min_x, max_x) para las coordenadas X.
        rango_y (tuple): Tupla (min_y, max_y) para las coordenadas Y.

    Returns:
        dict: Un diccionario donde la clave es el nombre de la ciudad (ej. 'Ciudad_0')
              y el valor es una tupla (x, y) de sus coordenadas.
    """
    ciudades = {}
    for i in range(num_ciudades):
        nombre_ciudad = f'Ciudad_{i}'
        x = random.randint(rango_x[0], rango_x[1])
        y = random.randint(rango_y[0], rango_y[1])
        ciudades[nombre_ciudad] = (x, y)
    return ciudades

def calcular_distancia_euclidiana(coord1, coord2):
    """
    Calcula la distancia euclidiana entre dos puntos.

    Args:
        coord1 (tuple): Coordenadas (x1, y1) del primer punto.
        coord2 (tuple): Coordenadas (x2, y2) del segundo punto.

    Returns:
        float: La distancia euclidiana.
    """
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

def construir_matriz_distancias(ciudades_dict):
    """
    Construye una matriz (diccionario de diccionarios) de distancias entre todas las ciudades.

    Args:
        ciudades_dict (dict): Diccionario de ciudades y sus coordenadas.

    Returns:
        dict: Diccionario de diccionarios donde distancias[ciudad1][ciudad2]
              es la distancia entre ciudad1 y ciudad2.
    """
    nombres_ciudades = list(ciudades_dict.keys())
    distancias = {}
    for i in range(len(nombres_ciudades)):
        ciudad1_nombre = nombres_ciudades[i]
        distancias[ciudad1_nombre] = {}
        for j in range(len(nombres_ciudades)):
            ciudad2_nombre = nombres_ciudades[j]
            if ciudad1_nombre == ciudad2_nombre:
                distancias[ciudad1_nombre][ciudad2_nombre] = 0
            else:
                coord1 = ciudades_dict[ciudad1_nombre]
                coord2 = ciudades_dict[ciudad2_nombre]
                distancia = calcular_distancia_euclidiana(coord1, coord2)
                distancias[ciudad1_nombre][ciudad2_nombre] = distancia
    return distancias

# --- Generación de 50 ciudades ---
num_ciudades_a_generar = 50
rango_x_coords = (0, 100) # Las ciudades estarán entre x=0 y x=100
rango_y_coords = (0, 100) # Las ciudades estarán entre y=0 y y=100

# 1. Generar las ciudades con coordenadas aleatorias
ciudades_50 = generar_ciudades_dispersas(num_ciudades_a_generar, rango_x_coords, rango_y_coords)

# 2. Construir la matriz de distancias a partir de las coordenadas
distancias_50 = construir_matriz_distancias(ciudades_50)

# Opcional: Imprimir algunas ciudades y sus distancias para verificar
print("Primeras 5 ciudades generadas:")
for i in range(5):
    nombre = f'Ciudad_{i}'
    print(f"{nombre}: {ciudades_50[nombre]}")

print("\nDistancias de Ciudad_0 a otras 5 ciudades:")
for i in range(1, 6):
   nombre_destino = f'Ciudad_{i}'
   if nombre_destino in distancias_50['Ciudad_0']:
       print(f"  a {nombre_destino}: {distancias_50['Ciudad_0'][nombre_destino]:.2f}")
