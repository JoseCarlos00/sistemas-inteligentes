import random
import math
import matplotlib.pyplot as plt # type: ignore

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


# Definición de las 5 ciudades (nodos) y sus coordenadas
ciudades = {
    'A': (0, 0),
    'B': (10, 0),
    'C': (5, 10),
    'D': (15, 8),
    'E': (8, 2)
}

distancias = {
    'A': {'B': 10, 'C': 15, 'D': 20, 'E': 25},
    'B': {'A': 10, 'C': 35, 'D': 25, 'E': 30},
    'C': {'A': 15, 'B': 35, 'D': 30, 'E': 20},
    'D': {'A': 20, 'B': 25, 'C': 30, 'E': 10},
    'E': {'A': 25, 'B': 30, 'C': 20, 'D': 10}
}

# --- Generación de 50 ciudades ---
num_ciudades_a_generar = 50
rango_x_coords = (0, 100) # Las ciudades estarán entre x=0 y x=100
rango_y_coords = (0, 100) # Las ciudades estarán entre y=0 y y=100

# 1. Generar las ciudades con coordenadas aleatorias
ciudades_50 = generar_ciudades_dispersas(num_ciudades_a_generar, rango_x_coords, rango_y_coords)

# 2. Construir la matriz de distancias a partir de las coordenadas
distancias_50 = construir_matriz_distancias(ciudades_50)

if ciudades_50:
    ciudades = ciudades_50
if distancias_50:
    distancias = distancias_50

# Función para visualizar las ciudades en un gráfico
def visualizar_ciudades(ciudades_dict):
    nombres_ciudades = list(ciudades_dict.keys())
    coordenadas_x = [ciudades_dict[ciudad][0] for ciudad in nombres_ciudades]
    coordenadas_y = [ciudades_dict[ciudad][1] for ciudad in nombres_ciudades]

    plt.figure(figsize=(8, 6))
    # Dibujar los puntos de las ciudades
    plt.scatter(coordenadas_x, coordenadas_y, s=100, c='blue', label='Ciudades', zorder=2) 

    # Dibujar líneas de conexión posibles entre todas las ciudades (opcional)
    for i in range(len(nombres_ciudades)):
        for j in range(i + 1, len(nombres_ciudades)):
            plt.plot([coordenadas_x[i], coordenadas_x[j]], 
                     [coordenadas_y[i], coordenadas_y[j]], 
                     'gray', linestyle='--', alpha=0.5, zorder=1) # Detrás de los puntos

    # Añadir etiquetas de texto para cada ciudad
    for i, nombre_ciudad in enumerate(nombres_ciudades):
        plt.text(coordenadas_x[i] + 0.3,  # Pequeño desfase en X
                 coordenadas_y[i] + 0.3,  # Pequeño desfase en Y
                 nombre_ciudad,
                 fontsize=9,
                 zorder=3) # Encima de los puntos y líneas

    plt.legend(loc='upper left', fontsize=10) # Leyenda para 'Ciudades'
    plt.title('Ubicación de las Ciudades')
    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.grid(True)
    plt.axis('equal')
    plt.show()


# Visualizar las ciudades iniciales
# visualizar_ciudades(ciudades)



# Parámetros del Algoritmo Genético
NUM_CIUDADES = len(ciudades.keys())
TAM_POBLACION = 10
NUM_GENERACIONES = 700
TASA_MUTACION = 0.1



# Función para calcular la aptitud (costo/distancia total de la ruta)
def calcular_aptitud(ruta):
    costo_total = 0
    num_ciudades_ruta = len(ruta) 
    
    for i in range(num_ciudades_ruta):
        ciudad_actual = ruta[i] # A | B | C...
        ciudad_siguiente = ruta[(i + 1) % num_ciudades_ruta] # Vuelve a la ciudad inicial
        costo_total += distancias[ciudad_actual][ciudad_siguiente]

    return costo_total

# Función para crear una ruta (cromosoma) aleatoria válida
def crear_ruta_aleatoria(ciudades_disponibles):
    ruta = list(ciudades_disponibles)
    random.shuffle(ruta)

    return ruta

# Generación de la población inicial
poblacion = [crear_ruta_aleatoria(list(ciudades.keys())) for _ in range(TAM_POBLACION)]

# Ejemplo de evaluación de aptitud de un individuo
# print(f"Primera ruta generada: {poblacion[0]}, Costo: {calcular_aptitud(poblacion[0])}")

# Función de selección por torneo
def seleccion_por_torneo(poblacion_actual, k=3):
    # Asegurarse de que k no sea mayor que el tamaño de la población
    k_valido = min(k, len(poblacion_actual))
    if k_valido == 0: # Si la población está vacía, no se puede seleccionar
        return None 
    
    torneo = random.sample(poblacion_actual, k_valido)

    # Elige la ruta con menor costo (mejor aptitud)
    return min(torneo, key=calcular_aptitud) 

# Implementación de Cruce Order Crossover (OX)
def cruce_ox(padre1, padre2):
    num_ciudades_ruta = len(padre1)

    # Elegir dos puntos de corte aleatorios
    punto1 = random.randint(0, num_ciudades_ruta - 1)
    punto2 = random.randint(0, num_ciudades_ruta - 1)

    if punto1 == punto2: # Asegurar que los puntos sean diferentes para tener un segmento
        punto2 = (punto1 + 1) % num_ciudades_ruta # Si es el último, vuelve al primero

    if punto1 > punto2:
        punto1, punto2 = punto2, punto1

    hijo1 = [None] * num_ciudades_ruta
    # Copiar segmento central del padre1 al hijo1
    hijo1[punto1:punto2+1] = padre1[punto1:punto2+1]

    # Llenar el resto del hijo1 con las ciudades del padre2 en el orden que aparecen
    # pero saltándose las que ya están en el segmento copiado
    puntos_padre2 = []
    for ciudad in padre2:
        if ciudad not in hijo1: # Más eficiente que "not in hijo1[punto1:punto2+1]" si hijo1 ya tiene Nones
            puntos_padre2.append(ciudad)

    idx_hijo = (punto2 + 1) % num_ciudades_ruta
    idx_padre2_fill = 0 # Índice para recorrer puntos_padre2
    
    # Llenar los espacios restantes en hijo1
    for i in range(num_ciudades_ruta - (punto2 - punto1 + 1)): # Número de elementos a llenar
        while hijo1[idx_hijo] is not None: 
            idx_hijo = (idx_hijo + 1) % num_ciudades_ruta
        if idx_padre2_fill < len(puntos_padre2): # Asegurar que no nos pasemos del índice
            hijo1[idx_hijo] = puntos_padre2[idx_padre2_fill]
            idx_padre2_fill += 1
        idx_hijo = (idx_hijo + 1) % num_ciudades_ruta


    # Repetir para hijo2 (padre2 como base, padre1 para rellenar)
    hijo2 = [None] * num_ciudades_ruta
    hijo2[punto1:punto2+1] = padre2[punto1:punto2+1]
    puntos_padre1 = []
    for ciudad in padre1:
        if ciudad not in hijo2:
            puntos_padre1.append(ciudad)
            
    idx_hijo = (punto2 + 1) % num_ciudades_ruta
    idx_padre1_fill = 0
    for i in range(num_ciudades_ruta - (punto2 - punto1 + 1)):
        while hijo2[idx_hijo] is not None:
            idx_hijo = (idx_hijo + 1) % num_ciudades_ruta
        if idx_padre1_fill < len(puntos_padre1):
            hijo2[idx_hijo] = puntos_padre1[idx_padre1_fill]
            idx_padre1_fill += 1
        idx_hijo = (idx_hijo + 1) % num_ciudades_ruta

    return hijo1, hijo2

# Función de mutación por intercambio
def mutacion_por_intercambio(ruta_original):
    ruta = list(ruta_original) # Crear una copia para no modificar la ruta original en la población
    idx1, idx2 = random.sample(range(len(ruta)), 2)
    
    # print('Ruta before:', ruta)
    # print('\n', 'idx1:', idx1,'\n', 'idx2:', idx2, '\n', 'Ciudad 1:', ruta[idx1], '\n', 'Ciudad 2:', ruta[idx2])

    # Intercambiar las ciudades en las posiciones idx1 y idx2
    ruta[idx1], ruta[idx2] = ruta[idx2], ruta[idx1]
    # print('Ruta after:', ruta)
    return ruta


# print('Test mutacion:','\n', 'Ruta:', poblacion[0], '\n',)
# mutacion_por_intercambio(poblacion[0])

# Otros parámetros del Algoritmo Genético
prob_cruce = 0.8
elitismo = 1 # Número de los mejores individuos a preservar

mejor_ruta_global = None
costo_mejor_ruta_global = float('inf')
historial_mejores_costos = []

# Bucle principal del Algoritmo Genético
for generacion in range(NUM_GENERACIONES):
    # Evaluar la población actual y encontrar la mejor ruta
    aptitudes_poblacion = [(calcular_aptitud(ind), ind) for ind in poblacion]
    aptitudes_poblacion.sort(key=lambda x: x[0]) # Ordenar por costo (ascendente)

    mejor_ruta_actual_generacion = aptitudes_poblacion[0][1] # Renombrado para claridad
    costo_mejor_actual_generacion = aptitudes_poblacion[0][0] # Renombrado para claridad

    if costo_mejor_actual_generacion < costo_mejor_ruta_global:
        costo_mejor_ruta_global = costo_mejor_actual_generacion
        mejor_ruta_global = list(mejor_ruta_actual_generacion) # Guardar una copia

    historial_mejores_costos.append(costo_mejor_ruta_global)

    # Preparar la próxima generación
    nueva_poblacion = []
    # Aplicar elitismo: copiar los mejores individuos directamente
    # Asegurarse de copiar las rutas, no solo las referencias
    for i in range(min(elitismo, len(aptitudes_poblacion))): # Evitar IndexError si elitismo > TAM_POBLACION
        nueva_poblacion.append(list(aptitudes_poblacion[i][1]))


    while len(nueva_poblacion) < TAM_POBLACION:
        padre1 = seleccion_por_torneo(poblacion)
        padre2 = seleccion_por_torneo(poblacion)
        
        # Asegurarse de que se seleccionaron padres válidos (si la población es muy pequeña o k es grande)
        if padre1 is None or padre2 is None:
            # Si no se pueden seleccionar padres (ej. población vacía después de elitismo extremo),
            # rellenar con rutas aleatorias o manejar de otra forma.
            # Por ahora, simplemente rompemos o rellenamos con aleatorios si es necesario.
            # Esto no debería ocurrir con la configuración actual.
            if len(nueva_poblacion) < TAM_POBLACION:
                 nueva_poblacion.append(crear_ruta_aleatoria(list(ciudades.keys())))
            continue


        hijo1, hijo2 = list(padre1), list(padre2) # Copiar para no modificar los padres originales en la población

        if random.random() < prob_cruce:
            hijo1_temp, hijo2_temp = cruce_ox(padre1, padre2)
            # Asegurarse de que el cruce produjo hijos válidos antes de asignarlos
            if hijo1_temp and hijo2_temp: # cruce_ox ahora debería siempre devolver hijos válidos
                hijo1, hijo2 = hijo1_temp, hijo2_temp


        if random.random() < TASA_MUTACION:
            hijo1 = mutacion_por_intercambio(hijo1)
        if random.random() < TASA_MUTACION:
            hijo2 = mutacion_por_intercambio(hijo2)

        nueva_poblacion.append(hijo1)
        if len(nueva_poblacion) < TAM_POBLACION: # Añadir hijo2 solo si hay espacio
            nueva_poblacion.append(hijo2)


    poblacion = nueva_poblacion[:TAM_POBLACION] # Asegurar el tamaño de la población

    # Imprimir el progreso
    if generacion % 10 == 0:
        print(f"Generación {generacion}: Mejor costo = {costo_mejor_ruta_global}")

print("\n--- Resultados Finales ---")
print(f"Mejor ruta encontrada: {mejor_ruta_global}")
print(f"Costo de la mejor ruta: {costo_mejor_ruta_global}")

# Visualizar la mejor ruta encontrada
if mejor_ruta_global:
    plt.figure(figsize=(10, 7))
    # Añadir la primera ciudad al final para cerrar el ciclo
    nombres_ciudades_ruta = mejor_ruta_global + [mejor_ruta_global[0]] 
    coordenadas_x_ruta = [ciudades[ciudad][0] for ciudad in nombres_ciudades_ruta]
    coordenadas_y_ruta = [ciudades[ciudad][1] for ciudad in nombres_ciudades_ruta]

    # Dibujar las conexiones de la ruta
    plt.plot(coordenadas_x_ruta, coordenadas_y_ruta, 'o-', markersize=8, label=f'Mejor Ruta (Costo: {costo_mejor_ruta_global})', zorder=1)

    # Dibujar los puntos de las ciudades
    todos_nombres_ciudades = list(ciudades.keys())
    todas_coordenadas_x = [ciudades[ciudad][0] for ciudad in todos_nombres_ciudades]
    todas_coordenadas_y = [ciudades[ciudad][1] for ciudad in todos_nombres_ciudades]
    plt.scatter(todas_coordenadas_x, todas_coordenadas_y, s=100, c='red', zorder=2)

    for i, nombre_ciudad in enumerate(todos_nombres_ciudades):
        plt.text(todas_coordenadas_x[i] + 0.3, todas_coordenadas_y[i] + 0.3, nombre_ciudad, fontsize=12)
    
    plt.title('Mejor Ruta Encontrada por el Algoritmo Genético')
    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    # plt.show()


# Gráfico de evolución del costo
plt.figure(figsize=(10,5)) # Crear una nueva figura para este gráfico
plt.plot(historial_mejores_costos)
plt.title('Evolución del Costo de la Mejor Ruta por Generación')
plt.xlabel('Generación')
plt.ylabel('Costo de la Ruta')
plt.grid(True)
plt.show()
