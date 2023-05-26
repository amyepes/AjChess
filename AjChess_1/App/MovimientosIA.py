""" Módulo que contiene los métodos de movimientos generados por IA. """
import random

valor_piezas = {'K': 0, 'Q': 10, 'R': 5, 'B': 3, 'N': 3, 'p': 1}

valor_caballo = [[1 for _ in range(8)],
                 [1, 2, 2, 2, 2, 2, 2, 1],
                 [1, 2, 3, 3, 3, 3, 2, 1],
                 [1, 2, 3, 4, 4, 3, 2, 1],
                 [1, 2, 3, 4, 4, 3, 2, 1],
                 [1, 2, 3, 3, 3, 3, 2, 1],
                 [1, 2, 2, 2, 2, 2, 2, 1],
                 [1 for _ in range(8)]]

valor_alfil = [[4, 3, 2, 1, 1, 2, 3, 4],
               [3, 4, 3, 2, 2, 3, 4, 3],
               [2, 3, 4, 3, 3, 4, 3, 2],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [2, 3, 4, 3, 3, 4, 3, 2],
               [3, 4, 3, 2, 2, 3, 4, 3],
               [4, 3, 2, 1, 1, 2, 3, 4]]

valor_reina = [[1, 1, 1, 3, 1, 1, 1, 1],
               [1, 2, 3, 3, 3, 1, 1, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 1, 2, 3, 3, 1, 1, 1],
               [1, 1, 1, 3, 1, 1, 1, 1]]

valor_torre = [[4, 3, 4, 4, 4, 4, 3, 4],
               [4, 4, 4, 4, 4, 4, 4, 4],
               [1, 1, 2, 3, 3, 2, 1, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 1, 2, 3, 3, 2, 1, 1],
               [4, 4, 4, 4, 4, 4, 4, 4],
               [4, 3, 4, 4, 4, 4, 3, 4]]

valor_peonblanco = [[8 for _ in range(8)],
                    [8 for _ in range(8)],
                    [5, 6, 6, 7, 7, 6, 6, 5],
                    [2, 3, 3, 5, 5, 3, 3, 2],
                    [1, 2, 3, 4, 4, 3, 2, 1],
                    [1, 1, 2, 3, 3, 2, 1, 1],
                    [1 if 2 < i < 5 else 0 for i in range(8)],
                    [0 for _ in range(8)]]

valor_peonnegro = [[0 for _ in range(8)],
                   [1 if 2 < i < 5 else 0 for i in range(8)],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [8 for _ in range(8)],
                   [8 for _ in range(8)]]

valor_rey = [[3, 3, 4, 3, 3, 4, 3, 3],
             [2, 2, 3, 3, 3, 3, 2, 2],
             [2, 3, 2, 1, 1, 2, 3, 2],
             [2, 3, 1, 1, 1, 1, 3, 2],
             [2, 3, 1, 1, 1, 1, 3, 2],
             [2, 3, 2, 1, 1, 2, 3, 2],
             [2, 2, 3, 3, 3, 3, 2, 2],
             [3, 3, 4, 3, 3, 4, 3, 3]]

valor_piezas_pos = {'N': valor_caballo, 'B': valor_alfil, 'Q': valor_reina, 'R': valor_torre,
                    'bp': valor_peonnegro, 'wp': valor_peonblanco, 'K': valor_rey}

JAQUEMATE = 1000
TABLAS = 0
global mov_siguiente, profundidad_global


def getMovimientoAleatorio(movs_legales):
    return movs_legales[random.randint(0, len(movs_legales) - 1)]


# Método auxiliar para el algoritmo MinMax
def getMejorMovimiento(partida, movs_legales, profundidad, cola):
    global mov_siguiente, profundidad_global
    mov_siguiente = None
    profundidad_global = profundidad
    random.shuffle(movs_legales)
    getMovimientoNegaMaxAlfaBeta(partida, movs_legales,
                                 profundidad, -JAQUEMATE, JAQUEMATE, 1 if partida.turnoBlanco else -1)
    cola.put(mov_siguiente)


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
            if profundidad == profundidad_global:
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
            if profundidad == profundidad_global:
                mov_siguiente = mov
        partida.Deshacer()
        if puntaje_max > alfa:
            alfa = puntaje_max
        if alfa >= beta:
            break
    return puntaje_max


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
        for c in range(len(partida.tablero.casillas[f])):
            p = partida.tablero.casillas[f][c]

            if p is not None:
                puntaje_p_pos = 0

                if p.tipo == 'p':
                    puntaje_p_pos = valor_piezas_pos[p.nombre][f][c]
                else:
                    puntaje_p_pos = valor_piezas_pos[p.tipo][f][c]

                if p.color == 'w':
                    puntaje += valor_piezas[p.tipo] + puntaje_p_pos * .2
                elif p.color == 'b':
                    puntaje -= valor_piezas[p.tipo] + puntaje_p_pos * .2

    return puntaje
