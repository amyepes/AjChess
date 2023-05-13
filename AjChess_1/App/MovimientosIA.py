import random

valor_piezas = {'K': 0, 'Q': 10, 'R': 5, 'B': 3, 'N': 3, 'p': 1}
jaque_mate = 1000
tablas = 0


def getMovimientoAleatorio(movs_legales):
    return movs_legales[random.randint(0, len(movs_legales) - 1)]


def getMovimiento(partida, movs_legales):
    signo = 1 if partida.turnoBlanco else -1
    max_puntaje = -jaque_mate
    mejor_mov = None
    for mov_jugador in movs_legales:
        partida.Mover(mov_jugador)
        if partida.jaquemate:
            puntaje = -jaque_mate
        elif partida.tablas:
            puntaje = tablas
        else:
            puntaje = ValorMaterial(partida.tablero) * signo
        if puntaje < max_puntaje:
            max_puntaje = puntaje
            mejor_mov = mov_jugador
        partida.Deshacer()
    return mejor_mov


def ValorMaterial(tablero):
    puntaje = 0
    for f in range(len(tablero.casillas)):
        for c in range(len(tablero.casillas[0])):
            if tablero.casillas[f][c] is not None:
                if tablero.casillas[f][c].color == 'w':
                    puntaje += valor_piezas[tablero.casillas[f][c].tipo]
                elif tablero.casillas[f][c].tipo == 'b':
                    puntaje -= valor_piezas[tablero.casillas[f][c].tipo]

    return puntaje
