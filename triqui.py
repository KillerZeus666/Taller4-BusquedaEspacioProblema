
#Taller 4 / Juan Camilo Gómez - Miguel Posso - Natalia Jiménez - Katheryn Guasca

###########################################################################################################################################################
# Esta es la clase matriz, la cual está definida por una matriz 3x3 para la representación del juego,
# un peso asociado a la heurística definida que es 0 por defecto.
class Matriz:

    # Inicialización de la matriz
    def __init__(self, peso=0):

        # Acá es inicializada la matriz 3x3, la cual fue establecido
        # que se dejaría vacio para indicar que no hay ningún valor
        self.matriz = [["" for _ in range(3)] for _ in range(3)]

        # De igual manera se define el peso como default en 0
        self.peso = peso

        # Setter de símbolo para el juego

    def setterSimbolo(self, fila, columna, elemento):

        # Acá se define según el juego que elemento se pone en
        # la matriz y en que posición con ayuda de fila y de columna.
        if 0 <= fila < 3 and 0 <= columna < 3:
            self.matriz[fila][columna] = elemento
        else:
            raise IndexError("Fila o columna fuera de rango. Debe estar entre 0 y 2.")

    # Getter del símbolo para el juego
    def getterSimbolo(self, fila, columna):

        # Acá simplemente se obtiene el valor del símbolo ubicado
        # en la fila o en la columna dada
        if 0 <= fila < 3 and 0 <= columna < 3:
            return self.matriz[fila][columna]
        else:
            raise IndexError("Fila o columna fuera de rango. Debe estar entre 0 y 2.")

    # Método de impresión para mostrar la matriz
    def mostrarMatriz(self):
        for fila in self.matriz:
            print(fila)

    # Getter para settear a la matriz el peso según el cálculo de la heurística
    def setterPeso(self, peso):
        self.peso = peso

    # Getter para el peso
    def getterPeso(self):
        return self.peso


###########################################################################################################################################################
# Clase NodoArbol para la implementación del árbol
class NodoArbol:
    def __init__(self, tablero, jugador=None):
        # Cada nodo del árbol se define por el jugador que lo controla,
        # el tablero recibido y los posibles hijos
        self.tablero = tablero
        self.jugador = jugador
        self.hijos = []

        # Método para agregar un hijo al nodo

    def agregarHijo(self, hijo):
        self.hijos.append(hijo)

    def __str__(self):
        return f"Jugador: {self.jugador}, Tablero: {self.tablero}"


###########################################################################################################################################################
# Método para crear árbol de posibles respuestas a las jugadas que va a dos niveles
def crearArbolito(tableroRecibido, bot="X"):
    # Se inicializa un tablero y se genera la raíz como copia del tablero recibido
    tableroArbolito = Matriz()
    for i in range(3):
        for j in range(3):
            tableroArbolito.setterSimbolo(i, j, tableroRecibido.getterSimbolo(i, j))

    # Método auixiliar para generar el árbol
    def generarArbol(tableroActual, jugadorActual, nivel=0):
        nodo = NodoArbol(tableroActual, jugadorActual)

        # Cuando se llega al segundo nivel se para la recursión
        if nivel >= 2:
            return nodo

        # Estos for son los encargados de revisar si hay alguna casilla vacia osea : ""
        # Y así generar una posible respuesta según las casillas
        for fila in range(3):
            for columna in range(3):
                if tableroActual.getterSimbolo(fila, columna) == "":
                    # Si se encuentra vacia la casilla, se inicializa una nueva
                    # matriz y se coloca el símbolo en el lugar libre
                    nuevoTablero = Matriz()
                    for i in range(3):
                        for j in range(3):
                            nuevoTablero.setterSimbolo(i, j, tableroActual.getterSimbolo(i, j))
                    nuevoTablero.setterSimbolo(fila, columna, jugadorActual)

                    # De ahí se elige pasa al siguiente jugador y se genera otro subarbol
                    # añadiendo otro hijo
                    proximoJugador = "O" if jugadorActual == "X" else "X"
                    subarbol = generarArbol(nuevoTablero, proximoJugador, nivel + 1)
                    nodo.agregarHijo(subarbol)

        # Finalmente se devuelve el nodo raíz para crear otra iteración
        # del primer nivel
        return nodo

    # Se retorna el arbolito completo
    return generarArbol(tableroArbolito, bot, nivel=0)


# Función para imprimir el árbol
def imprimirArbol(nodo, nivel=0, prefijo=""):
    # Con esta impresión se muestra el jugador
    print(f"{prefijo}└─ (Jugador: {nodo.jugador})")

    # Dibujar el tablero con separadores horizontales, se hacen separadores para el primer
    # nivel
    for i, fila in enumerate(nodo.tablero.matriz):
        print(f"{prefijo}    " + "  |  ".join(f"{cel if cel else ' '}" for cel in fila))
        if i < 2:  # No imprimir línea después de la última fila
            print(f"{prefijo}    " + "-" * 15)

    # Se recorre cada hijo y se emplea la recursión en esta función para imprimir
    if nodo.hijos:
        for i, hijo in enumerate(nodo.hijos):
            nuevo_prefijo = prefijo + ("│   " if i < len(nodo.hijos) - 1 else "    ")
            imprimirArbol(hijo, nivel + 1, nuevo_prefijo)


###########################################################################################################################################################

# Método para imprimir el tablero actual para jugar, se imprime del 1 al 9
# para facilitar la lectura
def imprimirTablero(tablero):
    print("\n")
    for i in range(3):
        print(" " + " | ".join(
            [f" {tablero.getterSimbolo(i, j)} " if tablero.getterSimbolo(i, j) != "" else f" {(i * 3) + j + 1} " for j
             in range(3)]))
        if i < 2:
            print("-----------------")
    print("\n")


# Método para verificar que el juego ha terminado
def finalizarJuego(tablero, jugador):
    # Se revisa horizontal y vertical para revisar si hay 3 símbolos iguales
    for i in range(3):
        if all(tablero.getterSimbolo(i, j) == jugador for j in range(3)) or all(
                tablero.getterSimbolo(j, i) == jugador for j in range(3)):
            return True
    # Se revisan las diagonales por 3 símbolos iguales
    if all(tablero.getterSimbolo(i, i) == jugador for i in range(3)) or all(
            tablero.getterSimbolo(i, 2 - i) == jugador for i in range(3)):
        return True
    return False


# Método para declarar empate (cuando se han llenado todas las casillas)
def verificarEmpate(tablero):
    return all(tablero.getterSimbolo(i, j) != "" for i in range(3) for j in range(3))


###########################################################################################################################################################
# NUEVA FUNCIONALIDAD: Implementación de heurística para el bot "O"

# Función para evaluar si un jugador está a un movimiento de ganar
def estaApuntoDeGanar(tablero, jugador):
    # Revisar filas
    for i in range(3):
        if sum(1 for j in range(3) if tablero.getterSimbolo(i, j) == jugador) == 2 and sum(
                1 for j in range(3) if tablero.getterSimbolo(i, j) == "") == 1:
            return True

    # Revisar columnas
    for j in range(3):
        if sum(1 for i in range(3) if tablero.getterSimbolo(i, j) == jugador) == 2 and sum(
                1 for i in range(3) if tablero.getterSimbolo(i, j) == "") == 1:
            return True

    # Revisar diagonal principal
    if sum(1 for i in range(3) if tablero.getterSimbolo(i, i) == jugador) == 2 and sum(
            1 for i in range(3) if tablero.getterSimbolo(i, i) == "") == 1:
        return True

    # Revisar diagonal secundaria
    if sum(1 for i in range(3) if tablero.getterSimbolo(i, 2 - i) == jugador) == 2 and sum(
            1 for i in range(3) if tablero.getterSimbolo(i, 2 - i) == "") == 1:
        return True

    return False


# Función para calcular la heurística
def calcularHeuristica(tablero, jugador):
    # Jugador oponente
    oponente = "X" if jugador == "O" else "O"

    # Verificar si el jugador ha ganado (valor extremadamente alto)
    if finalizarJuego(tablero, jugador):
        return 1000

    # Verificar si el oponente ha ganado (valor extremadamente bajo)
    if finalizarJuego(tablero, oponente):
        return -500

    # Calcular valor base
    valor = 0

    # Verificar si el oponente está a punto de ganar (-50)
    if estaApuntoDeGanar(tablero, oponente):
        valor -= 3


    # Contar esquinas y darles valor (5 por cada esquina)
    esquinas = [(0, 0), (0, 2), (2, 0), (2, 2)]
    for fila, col in esquinas:
        if tablero.getterSimbolo(fila, col) == jugador:
            valor += 10
        elif tablero.getterSimbolo(fila, col) == oponente:
            valor -= 3  # Penalización menor si el oponente tiene esquinas

    # Si un movimiento lleva a perder, penalizar fuertemente (-100)
    # Esto se verifica indirectamente al evaluar si el oponente está a punto de ganar

    return valor


# Implementación del algoritmo MIN-MAX para la toma de decisiones del bot
def minimax(nodo, esMaximizando, jugador="O"):
    # Obtener oponente
    oponente = "X" if jugador == "O" else "X"

    # Evaluación de nodo terminal (nodo hoja o nivel 2)
    if not nodo.hijos:
        # Calcular y asignar la heurística al tablero
        heuristica = calcularHeuristica(nodo.tablero, jugador)
        nodo.tablero.setterPeso(heuristica)
        return heuristica

    # Si es nodo maximizador (turno del bot)
    if esMaximizando:
        mejorValor = float('-inf')
        for hijo in nodo.hijos:
            valor = minimax(hijo, False, jugador)
            mejorValor = max(mejorValor, valor)
        nodo.tablero.setterPeso(mejorValor)
        return mejorValor
    # Si es nodo minimizador (turno del oponente)
    else:
        mejorValor = float('inf')
        for hijo in nodo.hijos:
            valor = minimax(hijo, True, jugador)
            mejorValor = min(mejorValor, valor)
        nodo.tablero.setterPeso(mejorValor)
        return mejorValor


# Función que determina la mejor jugada para el bot "O" usando MIN-MAX
def determinarMejorJugada(tablero):

    # crear arbol de todas las posibles jugadas en ese tablero
    arbol = crearArbolito(tablero, "O")

    # Aplicar MIN-MAX al árbol
    minimax(arbol, True, "O")

    # Encontrar el hijo con el mejor valor
    mejorValor = float('-inf')
    mejorHijo = None

    for hijo in arbol.hijos:
        if hijo.tablero.getterPeso() > mejorValor:
            mejorValor = hijo.tablero.getterPeso()
            mejorHijo = hijo

    # Encontrar qué movimiento se hizo de la raíz al mejor hijo
    for fila in range(3):
        for columna in range(3):
            if tablero.getterSimbolo(fila, columna) == "" and mejorHijo.tablero.getterSimbolo(fila, columna) == "O":
                return (fila, columna)

    # Fallback: si algo va mal, tomar la primera casilla disponible
    # (no debería llegar aquí en el funcionamiento normal)
    for fila in range(3):
        for columna in range(3):
            if tablero.getterSimbolo(fila, columna) == "":
                return (fila, columna)


###########################################################################################################################################################
# Método principal del juego
def jugarTriqui():
    # Se inicializa la matriz principal del juego y se
    # le da el turno al jugador humano representado por X
    tablero = Matriz()

    print("¡Bienvenido al juego de Triqui!")
    flag = True

    # Se pregunta al usuario quién empieza y se valida la entrada
    while flag:
        try:
            eleccion = int(input("Escoge quien empieza: (1) empieza la IA o (0) empiezas tú: "))
            if eleccion not in [0, 1]:
                print("Entrada inválida. Debes ingresar 1 o 0.")
                continue
        except ValueError:
            print("Entrada inválida. Debes ingresar un número.")
            continue
        flag = False

    if(eleccion == 1):
        turno = "O"
    else:
        turno = "X"

    print("Tú juegas como X y la computadora juega como O")
    print("Las casillas están numeradas del 1 al 9, de izquierda a derecha y de arriba a abajo")

    # Se repite el ciclo del juego mientras no exista un ganador o empate
    while True:
        # Se imprime el tablero
        imprimirTablero(tablero)

        if turno == "X":  # Turno del jugador X
            print(f"Tu turno (X)")
            try:
                jugada = int(input("Ingresa el número de la casilla (1-9): "))
            except ValueError:
                print("Entrada inválida. Debes ingresar un número.")
                continue
            if jugada < 1 or jugada > 9:
                print("Número fuera de rango. Intenta de nuevo.")
                continue

            # Se hace la traducción según los números del 1 al 9
            fila = (jugada - 1) // 3
            columna = (jugada - 1) % 3

            # Control de errores y seteo del símbolo si es correcto
            if tablero.getterSimbolo(fila, columna) != "":
                print("Casilla ocupada. Intenta de nuevo.")
                continue
            tablero.setterSimbolo(fila, columna, turno)

        else:  # Turno del bot (O)
            print("Turno de la computadora (O)...")
            # Determinar la mejor jugada usando MIN-MAX
            fila, columna = determinarMejorJugada(tablero)
            tablero.setterSimbolo(fila, columna, turno)
            print(f"La computadora juega en la casilla {fila * 3 + columna + 1}")

        # Se revisa si ya finzaliza el juego y se anuncia el ganador
        if finalizarJuego(tablero, turno):
            imprimirTablero(tablero)
            if turno == "X":
                print("¡Has ganado! 🎉")
            else:
                print("¡La computadora ha ganado! 🤖")
            break

        # Se revisa si hay empate
        if verificarEmpate(tablero):
            imprimirTablero(tablero)
            print("¡Es un empate! 🤝")
            break

        # Se cambia el turno según corresponda y se crea el arbolito
        # para visualización de posibilidades si le toca al bot
        turno = "O" if turno == "X" else "X"

        if turno == "O":
            arbol = crearArbolito(tablero, turno)
            print("Árbol de opciones:")
            imprimirArbol(arbol)
    # Solo mostrar el árbol si se activa esta opción (comentado por defecto)
    # Para activar, descomentar las siguientes líneas

# Función pa jugar
if __name__ == "__main__":
    jugarTriqui()
