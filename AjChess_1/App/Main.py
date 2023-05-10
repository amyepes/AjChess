""" Driver principal de la aplicación, encargado de mostrar
y ejecutar la interfaz gráfica. """

import pygame as pg
import Motor

ancho = altura = 440  # Tamaño de la pantalla
dimension = 8  # El tablero tiene dimensión 8x8
dimCasilla = altura // dimension
fps = 15  # Fps para animaciones
imgs = {}  # Diccionario de imágenes de las piezas
colores = [pg.Color("white"), pg.Color("gray")]  # Colores de las casillas

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
    mov_sw = False  # Indica si se realizó un movimiento
    animar = False  # Indica si se debe animar un movimiento
    CargaImagen()
    ejecutando = True
    CasillaSeleccionada = ()  # Guarda la casilla seleccionada por el usuario
    clicks = []  # Guarda los clicks del usuario
    gameOver = False
    while ejecutando:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                ejecutando = False
            elif e.type == pg.MOUSEBUTTONDOWN:  # Evento de click del mouse
                if not gameOver:
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
                                animar = True
                                CasillaSeleccionada = ()
                                clicks = []
                        if not mov_sw:
                            clicks = [CasillaSeleccionada]
            elif e.type == pg.KEYDOWN:  # Evento de tecla presionada
                if e.key == pg.K_z:  # Tecla z para deshacer el último movimiento
                    if len(partida.movimientos) != 0:
                        partida.Deshacer()
                        CasillaSeleccionada = ()
                        clicks = []
                        mov_sw = True
                        animar = False
                if e.key == pg.K_r:  # Tecla r para reiniciar la partida
                    partida = Motor.Partida()
                    movimientos_legales = partida.movimientos_legales()
                    CasillaSeleccionada = ()
                    clicks = []
                    mov_sw = False
                    animar = False
        if mov_sw:
            if animar:
                Animar_Movimiento(pantalla, partida.movimientos[-1], partida.tablero, reloj)
            movimientos_legales = partida.movimientos_legales()
            mov_sw = False
        MostrarPartida(pantalla, partida, movimientos_legales, CasillaSeleccionada)

        if partida.jaquemate:
            gameOver = True
            if partida.turnoBlanco:
                dibujarTexto(pantalla, 'Jaque mate, ganan las negras')
            else:
                dibujarTexto(pantalla, 'Jaque mate, ganan las blancas')
        elif partida.tablas:
            gameOver = True
            dibujarTexto(pantalla, 'Tablas')

        reloj.tick(fps)
        pg.display.flip()


def SeleccionarCasillas(pantalla, partida, movs, casilla_seleccionada):
    if casilla_seleccionada != ():
        f, c = casilla_seleccionada
        if partida.tablero.casillas[f][c] is not None:
            if partida.tablero.casillas[f][c].color == ('w' if partida.turnoBlanco else 'b'):
                # Pintar un rectángulo azul en la casilla seleccionada
                s = pg.Surface((dimCasilla, dimCasilla))
                s.set_alpha(100)  # Transparencia, 0 es transparente y 255 es opaco
                s.fill(pg.Color('blue'))
                pantalla.blit(s, (c * dimCasilla, f * dimCasilla))
                # Pintar las casillas a las que se puede mover la pieza
                s.fill(pg.Color('yellow'))
                for mov in movs:
                    if mov.fil_inicio == f and mov.col_inicio == c:
                        pantalla.blit(s, (mov.col_fin * dimCasilla, mov.fil_fin * dimCasilla))


# Dibuja el tablero de ajedrez
def MostrarPartida(pantalla, partida, movs, casilla_seleccionada):
    DibujarTablero(pantalla)  # Dibuja las casillas del tablero
    SeleccionarCasillas(pantalla, partida, movs, casilla_seleccionada)
    DibujarPiezas(pantalla, partida.tablero)  # Dibuja las piezas del tablero


def DibujarTablero(pantalla):
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


def Animar_Movimiento(pantalla, mov, tablero, clock):
    df = mov.fil_fin - mov.fil_inicio
    dc = mov.col_fin - mov.col_inicio
    fps_cas = 10  # Velocidad de la animación
    set_frames = (abs(df) + abs(dc)) * fps_cas  # Número de frames de la animación
    for frame in range(set_frames + 1):
        f, c = (mov.fil_inicio + df * frame / set_frames, mov.col_inicio + dc * frame / set_frames)
        DibujarTablero(pantalla)
        DibujarPiezas(pantalla, tablero)
        color = colores[((mov.fil_fin + mov.col_fin) % 2)]
        casilla = pg.Rect(mov.col_fin * dimCasilla, mov.fil_fin * dimCasilla, dimCasilla, dimCasilla)
        pg.draw.rect(pantalla, color, casilla)
        if mov.piezaCapturada is not None:
            pantalla.blit(imgs[mov.piezaCapturada.nombre], casilla)
        pantalla.blit(imgs[mov.piezaMovida.nombre], pg.Rect(c * dimCasilla, f * dimCasilla, dimCasilla, dimCasilla))
        pg.display.flip()
        clock.tick(60)


def dibujarTexto(pantalla, texto):
    fuente = pg.font.SysFont('Times New Roman', 32, True, False)
    obj_texto = fuente.render(texto, 0, pg.Color('Black'))
    locacion_texto = pg.Rect(0, 0, ancho, altura).move(ancho / 2 - obj_texto.get_width() / 2, altura
                                                       / 2 - obj_texto.get_height() / 2)
    pantalla.blit(obj_texto, locacion_texto)
    # obj_texto = fuente.render(texto, 0, pg.Color('Gray'))
    # pantalla.blit(obj_texto, locacion_texto.move(2, 2))


if __name__ == "__main__":
    main()
