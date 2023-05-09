""" Driver principal de la aplicación, encargado de mostrar
y ejecutar la interfaz gráfica. """

import pygame as pg
import Motor

ancho = altura = 440  # Tamaño de la pantalla
dimension = 8  # El tablero tiene dimensión 8x8
dimCasilla = altura // dimension
fps = 15  # Fps para animaciones
imgs = {}  # Diccionario de imágenes de las piezas


# Carga las imágenes de las piezas y las guarda en un diccionario.
def CargaImagen():
    # Los strings de la lista son los nombres de los archivos .png
    piezas = ["wR", "wN", "wB", "wQ", "wK", "wp", "bR", "bN", "bB", "bQ", "bK", "bp"]
    for pz in piezas:
        imgs[pz] = pg.transform.scale(pg.image.load("images/" + pz + ".png"), (dimCasilla, dimCasilla))


def main():
    pg.init()
    pantalla = pg.display.set_mode((ancho, altura))
    reloj = pg.time.Clock()
    pantalla.fill(pg.Color("white"))
    pg.display.set_caption('AjChess')
    partida = Motor.Partida()
    movimientos_legales = partida.movimientos_legales()
    for mm in movimientos_legales:
        print(mm.getNotacion(), end=' ')
    print()
    mov_sw = False
    CargaImagen()
    ejecutando = True
    CasillaSeleccionada = ()  # Guarda la casilla seleccionada por el usuario
    clicks = []  # Guarda los clicks del usuario
    while ejecutando:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                ejecutando = False
            elif e.type == pg.MOUSEBUTTONDOWN:  # Evento de click del mouse
                pos = pg.mouse.get_pos()  # Posición del mouse
                col = pos[0] // dimCasilla
                fila = pos[1] // dimCasilla
                if len(clicks) == 0 and partida.tablero.casillas[fila][col] is None:
                    CasillaSeleccionada = ()
                    clicks = []
                elif CasillaSeleccionada == (fila, col):
                    CasillaSeleccionada = ()
                    clicks = []
                else:
                    CasillaSeleccionada = (fila, col)
                    clicks.append(CasillaSeleccionada)  # Se guardan los dos clicks del usuario
                if len(clicks) == 2 and partida.tablero.casillas[clicks[0][0]][clicks[0][1]] is not None:
                    mov = Motor.Movimiento(clicks[0], clicks[1], partida.tablero)
                    for i in range(len(movimientos_legales)):
                        if mov == movimientos_legales[i]:
                            partida.Mover(movimientos_legales[i])
                            print(f'Movimiento realizado: {movimientos_legales[i].getNotacion()}')
                            mov_sw = True
                            CasillaSeleccionada = ()
                            clicks = []
                            print('Turno blancas' if partida.turnoBlanco else 'Turno negras')
                    if not mov_sw:
                        clicks = [CasillaSeleccionada]
            elif e.type == pg.KEYDOWN:  # Evento de tecla presionada
                if e.key == pg.K_z:  # Tecla z para deshacer el último movimiento
                    if len(partida.movimientos) != 0:
                        partida.Deshacer()
                        CasillaSeleccionada = ()
                        clicks = []
                        print('Turno blancas' if partida.turnoBlanco else 'Turno negras')
                        mov_sw = True
        if mov_sw:
            movimientos_legales = partida.movimientos_legales()
            for mm in movimientos_legales:
                print(mm.getNotacion(), end=' ')
            print()
            mov_sw = False
        MostrarPartida(pantalla, partida)
        reloj.tick(fps)
        pg.display.flip()
        if partida.jaqueMate:
            print('Jaque mate')
            ejecutando = False
        elif partida.tablas:
            print('Empate por ahogado')
            ejecutando = False


# Dibuja el tablero de ajedrez
def MostrarPartida(pantalla, partida):
    DibujarTablero(pantalla)  # Dibuja las casillas del tablero
    # Añadir otras funciones visuales
    DibujarPiezas(pantalla, partida.tablero)  # Dibuja las piezas del tablero


def DibujarTablero(pantalla):
    colores = [pg.Color("white"), pg.Color("gray")]
    for fila in range(dimension):
        for col in range(dimension):
            color = colores[((fila + col) % 2)]
            pg.draw.rect(pantalla, color, pg.Rect(col * dimCasilla, fila * dimCasilla, dimCasilla, dimCasilla))


def DibujarPiezas(pantalla, tablero):
    for fila in range(dimension):
        for col in range(dimension):
            pieza = tablero.casillas[fila][col]
            if pieza is not None:
                pantalla.blit(imgs[pieza.nombre], pg.Rect(col * dimCasilla, fila * dimCasilla, dimCasilla, dimCasilla))


if __name__ == "__main__":
    main()
