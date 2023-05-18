""" Módulo que contiene los métodos de movimientos generados por IA. """
import random

valor_piezas = {'K': 0, 'Q': 10, 'R': 5, 'B': 3, 'N': 3, 'p': 1}
JAQUEMATE = 1000
TABLAS = 0
PROFUNDIDAD = 3  # Profundidad del árbol de búsqueda, no sobrepasarse de 4
global mov_siguiente


def getMovimientoAleatorio(movs_legales):
    return movs_legales[random.randint(0, len(movs_legales) - 1)]


def getMovimientoNotMinMax(partida, movs_legales):
    signo = 1 if partida.turnoBlanco else -1
    puntaje_minmax_enemigo = JAQUEMATE
    mejor_mov_jugador = None
    random.shuffle(movs_legales)
    for mov_jugador in movs_legales:
        partida.Mover(mov_jugador)
        movs_enemigo = partida.movimientos_legales()
        if partida.TABLAS:
            puntaje_max_enemigo = TABLAS
        elif partida.jaquemate:
            puntaje_max_enemigo = -JAQUEMATE
        else:
            puntaje_max_enemigo = -JAQUEMATE
            for mov_enemigo in movs_enemigo:
                partida.Mover(mov_enemigo)
                if partida.jaquemate:
                    puntaje = JAQUEMATE
                elif partida.TABLAS:
                    puntaje = TABLAS
                else:
                    puntaje = ValorMaterial(partida.tablero) * -signo
                if puntaje > puntaje_max_enemigo:
                    puntaje_max_enemigo = puntaje
                partida.Deshacer()
        if puntaje_max_enemigo < puntaje_minmax_enemigo:
            puntaje_minmax_enemigo = puntaje_max_enemigo
            mejor_mov_jugador = mov_jugador
        partida.Deshacer()
    return mejor_mov_jugador


# Método auxiliar para el algoritmo MinMax
def getMejorMovimiento(partida, movs_legales):
    global mov_siguiente
    mov_siguiente = None
    random.shuffle(movs_legales)
    getMovimientoNegaMaxAlfaBeta(partida, movs_legales,
                                 PROFUNDIDAD, -JAQUEMATE, JAQUEMATE, 1 if partida.turnoBlanco else -1)
    return mov_siguiente


def getMovimientoMinmax(partida, movs_legales, profundidad, turnoblanco):
    global mov_siguiente
    if profundidad == 0:
        return ValorMaterial(partida.tablero)

    if turnoblanco:
        puntaje_max = -JAQUEMATE
        for mov in movs_legales:
            partida.Mover(mov)
            mvl = partida.movimientos_legales()
            random.shuffle(mvl)
            puntaje = getMovimientoMinmax(partida, mvl, profundidad - 1, False)
            if puntaje > puntaje_max:
                puntaje_max = puntaje
                if profundidad == PROFUNDIDAD:
                    mov_siguiente = mov
            partida.Deshacer()
        return puntaje_max
    else:
        puntaje_min = JAQUEMATE
        for mov in movs_legales:
            partida.Mover(mov)
            mvl = partida.movimientos_legales()
            random.shuffle(mvl)
            puntaje = getMovimientoMinmax(partida, mvl, profundidad - 1, True)
            if puntaje < puntaje_min:
                puntaje_min = puntaje
                if profundidad == PROFUNDIDAD:
                    mov_siguiente = mov
            partida.Deshacer()
        return puntaje_min


def getMovimientoNegaMax(partida, movs_legales, profundidad, signo_turno):
    global mov_siguiente
    if profundidad == 0:
        return signo_turno * ValorTablero(partida)

    puntaje_max = -JAQUEMATE
    for mov in movs_legales:
        partida.Mover(mov)
        mvl = partida.movimientos_legales()
        random.shuffle(mvl)
        puntaje = -getMovimientoNegaMax(partida, mvl, profundidad - 1, -signo_turno)
        if puntaje > puntaje_max:
            puntaje_max = puntaje
            if profundidad == PROFUNDIDAD:
                mov_siguiente = mov
        partida.Deshacer()
    return puntaje_max


def getMovimientoNegaMaxAlfaBeta(partida, movs_legales, profundidad, alfa, beta, signo_turno):
    global mov_siguiente
    if profundidad == 0:
        return signo_turno * ValorTablero(partida)

    # Añadir ordenamiento de movimientos según puntaje
    puntaje_max = -JAQUEMATE
    for mov in movs_legales:
        partida.Mover(mov)
        mvl = partida.movimientos_legales()
        random.shuffle(mvl)
        puntaje = -getMovimientoNegaMaxAlfaBeta(partida, mvl, profundidad - 1, -beta, -alfa, -signo_turno)
        if puntaje > puntaje_max:
            puntaje_max = puntaje
            if profundidad == PROFUNDIDAD:
                mov_siguiente = mov
        partida.Deshacer()
        if puntaje_max > alfa:
            alfa = puntaje_max
        if alfa >= beta:
            break
    return puntaje_max


def ValorMaterial(tablero):
    puntaje = 0
    for f in range(len(tablero.casillas)):
        for c in range(len(tablero.casillas[0])):
            if tablero.casillas[f][c] is not None:
                if tablero.casillas[f][c].color == 'w':
                    puntaje += valor_piezas[tablero.casillas[f][c].tipo]
                elif tablero.casillas[f][c].color == 'b':
                    puntaje -= valor_piezas[tablero.casillas[f][c].tipo]
    return puntaje


def ValorTablero(partida):
    # Valor > 0: Ventaja para las blancas
    # Valor < 0: Ventaja para las negras
    if partida.jaquemate:
        if partida.turnoBlanco:
            return -JAQUEMATE
        else:
            return JAQUEMATE
    elif partida.tablas:
        return TABLAS

    puntaje = 0
    for f in range(len(partida.tablero.casillas)):
        for c in range(len(partida.tablero.casillas[0])):
            if partida.tablero.casillas[f][c] is not None:
                if partida.tablero.casillas[f][c].color == 'w':
                    puntaje += valor_piezas[partida.tablero.casillas[f][c].tipo]
                elif partida.tablero.casillas[f][c].color == 'b':
                    puntaje -= valor_piezas[partida.tablero.casillas[f][c].tipo]
    return puntaje
