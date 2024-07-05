import heapq

class Nodo:
    def __init__(self, x, y, g=float('inf'), h=0, f=float('inf'), parent=None):
        self.x = x
        self.y = y
        self.g = g  # Costo acumulado desde el nodo inicial hasta este nodo
        self.h = h  # Heurística (distancia estimada al nodo objetivo)
        self.f = f  # Costo total estimado (f = g + h)
        self.parent = parent  # Nodo padre en el camino hacia el nodo inicial

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

def obtener_coordenadas(mensaje):
    while True:
        try:
            entrada = input(mensaje)
            x, y = map(int, entrada.split())
            return (x, y)
        except ValueError:
            print("Por favor, ingresa dos números enteros separados por espacio.")

def agregar_obstaculo(tablero):
    while True:
        print("Ingresa las coordenadas del obstáculo (x y), o 'fin' para terminar:")
        entrada = input()
        if entrada.lower() == 'fin':
            break
        try:
            x, y = map(int, entrada.split())
            if tablero[x][y] == 0:
                tablero[x][y] = 1  # Colocar obstáculo en la posición
            else:
                print("Ya hay un obstáculo en esa posición.")
        except (ValueError, IndexError):
            print("Coordenadas inválidas. Intenta nuevamente.")

def encontrar_ruta(mapa, inicio, objetivo):
    n_filas = len(mapa)
    n_columnas = len(mapa[0])

    nodos_abiertos = []
    nodos_cerrados = []

    nodo_inicio = Nodo(inicio[0], inicio[1])
    nodo_objetivo = Nodo(objetivo[0], objetivo[1])

    heapq.heappush(nodos_abiertos, nodo_inicio)
    nodo_inicio.g = 0
    nodo_inicio.f = calcular_f(nodo_inicio, nodo_objetivo)

    while nodos_abiertos:
        nodo_actual = heapq.heappop(nodos_abiertos)

        if nodo_actual == nodo_objetivo:
            return construir_camino(nodo_actual)

        nodos_cerrados.append(nodo_actual)

        vecinos = obtener_vecinos(mapa, nodo_actual, n_filas, n_columnas)
        for vecino in vecinos:
            if vecino in nodos_cerrados:
                continue

            nuevo_costo_g = nodo_actual.g + 1  # Costo uniforme, todos los movimientos tienen el mismo costo

            if nuevo_costo_g < vecino.g:
                vecino.parent = nodo_actual
                vecino.g = nuevo_costo_g
                vecino.h = calcular_f(vecino, nodo_objetivo)
                vecino.f = vecino.g + vecino.h

                heapq.heappush(nodos_abiertos, vecino)

    return None  # No se encontró ruta válida

def obtener_vecinos(mapa, nodo, n_filas, n_columnas):
    vecinos = []
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Movimientos arriba, abajo, izquierda, derecha

    for dx, dy in direcciones:
        x_vecino, y_vecino = nodo.x + dx, nodo.y + dy

        if 0 <= x_vecino < n_filas and 0 <= y_vecino < n_columnas:
            if mapa[x_vecino][y_vecino] != 1:  # No es un obstáculo
                vecino = Nodo(x_vecino, y_vecino)
                vecinos.append(vecino)

    return vecinos

def calcular_f(nodo, objetivo):
    return abs(nodo.x - objetivo.x) + abs(nodo.y - objetivo.y)

def construir_camino(nodo_final):
    camino = []
    nodo_actual = nodo_final

    while nodo_actual is not None:
        camino.append((nodo_actual.x, nodo_actual.y))
        nodo_actual = nodo_actual.parent

    return camino[::-1]  # Devolver el camino en orden desde el inicio al objetivo

def imprimir_tablero_con_ruta(tablero, ruta, inicio, destino):
    n_filas = len(tablero)
    n_columnas = len(tablero[0])

    # Crear una copia del tablero para modificarlo con la ruta
    tablero_con_ruta = [fila[:] for fila in tablero]

    # Colocar 'i' en el punto de inicio y 'd' en el punto de destino
    tablero_con_ruta[inicio[0]][inicio[1]] = 'i'
    tablero_con_ruta[destino[0]][destino[1]] = 'd'

    # Marcar la ruta en el tablero con '.'
    for paso in ruta:
        x, y = paso
        if tablero_con_ruta[x][y] != 'i' and tablero_con_ruta[x][y] != 'd':
            tablero_con_ruta[x][y] = '.'

    # Imprimir el tablero con la ruta marcada
    for fila in tablero_con_ruta:
        for celda in fila:
            print(celda, end=' ')
        print()

# Ejemplo de uso
if __name__ == "__main__":
    # Definir las dimensiones del tablero
    n_filas = 10
    n_columnas = 10

    # Crear el tablero inicial lleno de ceros (caminos libres)
    tablero = [[0 for _ in range(n_columnas)] for _ in range(n_filas)]

    # Agregar obstáculos
    agregar_obstaculo(tablero)

    # Solicitar punto de inicio
    inicio = obtener_coordenadas("Ingresa las coordenadas del punto de inicio (x y): ")

    # Solicitar punto de destino
    destino = obtener_coordenadas("Ingresa las coordenadas del punto de destino (x y): ")

    # Encontrar la ruta más corta entre inicio y destino
    ruta = encontrar_ruta(tablero, inicio, destino)

    if ruta:
        print("Ruta encontrada:")
        imprimir_tablero_con_ruta(tablero, ruta, inicio, destino)
    else:
        print("No se encontró ruta válida.")
