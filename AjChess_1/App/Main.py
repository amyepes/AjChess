""" Driver principal de la aplicación, encargado de mostrar
y ejecutar la interfaz gráfica. """

import time
import pygame as pg
import Motor
import MovimientosIA
from multiprocessing import Process, Queue

ANCHO_T = ALTURA_T = 440  # Tamaño del tablero
ANCHO_MOV = 240  # Ancho de la barra de movimientos
ALTURA_MOV = ALTURA_T  # Altura de la barra de movimientos
DIMENSION = 8  # El tablero tiene dimensión 8x8
TAM_CASILLA = ALTURA_T // DIMENSION
FPS = 15  # Fps para animaciones
imgs = {}  # Diccionario de imágenes de las piezas
colores = [pg.Color("white"), pg.Color("gray")]  # Colores de las casillas
inv_pos_cas = [i for i in range(7, -1, -1)]
tablero_invertido = False  # Indica si el tablero está invertido
ventana_coronacion = False  # Indica si se está mostrando la ventana de coronación
PROF_IA = 3  # Profundidad de la IA

ANC_RELOJ = 100  # Ancho del reloj
ALT_RELOJ = 50  # Altura del reloj
TIEMPO_LIM = 845  # Tiempo límite por jugador en segundos


# Carga las imágenes de las piezas y las guarda en un diccionario.
def CargaImagen():
    # Los strings de la lista son los nombres de los archivos .png
    piezas = ["wR", "wN", "wB", "wQ", "wK", "wp", "bR", "bN", "bB", "bQ", "bK", "bp"]
    for pz in piezas:
        imgs[pz] = pg.transform.scale(pg.image.load("images/" + pz + ".png"), (TAM_CASILLA, TAM_CASILLA))


def main(j1=False, j2=True, tiempo_lim=TIEMPO_LIM, prof_ia=PROF_IA):
    global tablero_invertido
    pg.init()
    pg.mixer.init()
    pantalla = pg.display.set_mode((ANCHO_T + ANCHO_MOV, ALTURA_T))
    reloj = pg.time.Clock()
    pantalla.fill(pg.Color("white"))
    pg.display.set_caption('AjChess')

    fx_captura = pg.mixer.Sound("sounds/captura.mp3")
    fx_jaque = pg.mixer.Sound("sounds/jaque.wav")
    fx_movimiento = pg.mixer.Sound("sounds/movimiento.wav")
    fx_jaquemate = pg.mixer.Sound("sounds/jaque_mate.wav")
    fx_coronacion = pg.mixer.Sound("sounds/coronar.wav")
    fx = [fx_captura, fx_jaque, fx_movimiento, fx_jaquemate, fx_coronacion]
    sw_fx_jaquemate = False

    partida = Motor.Partida()
    movimientos_legales = partida.movimientos_legales()
    mov_sw = False  # Indica si se realizó un movimiento
    CargaImagen()

    fuente_movimientos = pg.font.SysFont("Arial", 14, False, False)
    fuente_reloj = pg.font.SysFont("Times New Roman", 32, False, False)  # Fuente del reloj

    ejecutando = True
    CasillaSeleccionada = ()  # Guarda la casilla seleccionada por el usuario
    clicks = []  # Guarda los clicks del usuario

    gameOver = False
    ejecutandoAI = False
    procesoAI = None
    mov_deshecho = False

    jugador1 = Motor.Jugador(humano=j1)
    jugador2 = Motor.Jugador(humano=j2)

    tiempo_inicio_b = tiempo_inicio_n = time.time()
    tb_lim = tn_lim = tiempo_lim  # Tiempo límite para las blancas en segundos
    tb = tb_lim
    tn = tn_lim
    sw_tiempo = 0

    while ejecutando:
        turno_humano = (partida.turnoBlanco and jugador1.humano) or (not partida.turnoBlanco and jugador2.humano)
        for e in pg.event.get():
            if e.type == pg.QUIT:
                ejecutando = False
            elif e.type == pg.MOUSEBUTTONDOWN:  # Evento de click del mouse

                if not gameOver:
                    pos = pg.mouse.get_pos()  # Posición del mouse
                    col = pos[0] // TAM_CASILLA
                    fila = pos[1] // TAM_CASILLA
                    if tablero_invertido and col <= 7 and fila <= 7:
                        col = inv_pos_cas[col]
                        fila = inv_pos_cas[fila]
                    if CasillaSeleccionada == (fila, col) or col >= 8:  # Click en la misma casilla o fuera del tablero
                        CasillaSeleccionada = ()
                        clicks = []
                    elif len(clicks) == 0 and partida.tablero.casillas[fila][col] is None:
                        CasillaSeleccionada = ()
                        clicks = []
                    else:
                        CasillaSeleccionada = (fila, col)
                        clicks.append(CasillaSeleccionada)  # Se guardan los dos clicks del usuario
                    if len(clicks) == 2 and turno_humano:  # partida.tablero.casillas[clicks[0][0]][clicks[0][1]]
                        mov = Motor.Movimiento(clicks[0], clicks[1], partida.tablero)
                        for i in range(len(movimientos_legales)):
                            if mov == movimientos_legales[i]:
                                partida.Mover(movimientos_legales[i])
                                mov_sw = True
                                CasillaSeleccionada = ()
                                clicks = []
                                ReproducirSonido(movimientos_legales[i], fx)
                                sw_tiempo += 1
                        if not mov_sw:
                            clicks = [CasillaSeleccionada]

            elif e.type == pg.KEYDOWN:  # Evento de tecla presionada

                if e.key == pg.K_z:  # Tecla z para deshacer el último movimiento
                    partida.Deshacer()
                    CasillaSeleccionada = ()
                    clicks = []
                    mov_sw = True
                    if not jugador1.humano or not jugador2.humano:
                        turno_humano = not turno_humano
                    gameOver = False
                    if ejecutandoAI:
                        procesoAI.terminate()
                        ejecutandoAI = False
                    mov_deshecho = True

                if e.key == pg.K_r:  # Tecla r para reiniciar la partida
                    partida = Motor.Partida()
                    movimientos_legales = partida.movimientos_legales()
                    CasillaSeleccionada = ()
                    clicks = []
                    mov_sw = False
                    gameOver = False
                    sw_tiempo = 0
                    tiempo_inicio_n = tiempo_inicio_b = time.time()
                    tb_lim = tn_lim = tiempo_lim
                    tb = tb_lim
                    tn = tn_lim
                    if ejecutandoAI:
                        procesoAI.terminate()
                        ejecutandoAI = False
                    mov_deshecho = False

                if e.key == pg.K_t:  # Tecla t para invertir el tablero
                    tablero_invertido = not tablero_invertido

        if not gameOver and not turno_humano and not mov_deshecho:
            if not ejecutandoAI:
                ejecutandoAI = True
                print("Calculando...")
                cola = Queue()
                procesoAI = Process(target=MovimientosIA.getMejorMovimiento,
                                    args=(partida, movimientos_legales, prof_ia, cola))
                procesoAI.start()  # Se invoca la función de obtener un movimiento en un proceso aparte

            if not procesoAI.is_alive():
                mov_ia = cola.get()
                print("Movimiento calculado")
                if mov_ia is None:
                    mov_ia = MovimientosIA.getMovimientoAleatorio(movimientos_legales)
                partida.Mover(mov_ia)
                ReproducirSonido(mov_ia, fx)
                mov_sw = True
                ejecutandoAI = False

        if mov_sw:
            movimientos_legales = partida.movimientos_legales()
            mov_sw = False
            mov_deshecho = False

        MostrarPartida(pantalla, partida, movimientos_legales, CasillaSeleccionada, fuente_movimientos)

        if sw_tiempo == 1:
            tiempo_inicio_n = time.time()

        if not gameOver:
            if partida.turnoBlanco:
                tiempo_transcurrido = int(time.time() - tiempo_inicio_b)
                tb = max(tb_lim - tiempo_transcurrido, 0)  # Calcular el tiempo restante para las blancas
            else:
                tiempo_transcurrido = int(time.time() - tiempo_inicio_n)
                tn = max(tn_lim - tiempo_transcurrido, 0)  # Calcular el tiempo restante para las negras
            Reloj(pantalla, fuente_reloj, tb, (ANCHO_T + ANCHO_MOV - 45, ALTURA_T - 60), (0, 0, 0), (255, 255, 255))
            Reloj(pantalla, fuente_reloj, tn, (ANCHO_T + ANCHO_MOV - 45, ALTURA_T - 20), (255, 255, 255), (0, 0, 0))

        if partida.jaquemate or partida.tablas:
            gameOver = True
            if partida.tablas:
                texto = '0-0'
            else:
                if not sw_fx_jaquemate:
                    pg.mixer.Sound.play(fx_jaquemate)
                    sw_fx_jaquemate = True
                texto = "1-0" if not partida.turnoBlanco else "0-1"
            dibujarTextoFinal(pantalla, texto)

        reloj.tick(FPS)
        pg.display.flip()


def Reloj(pantalla, fuente, tiempo, pos, color_texto, color_fondo):
    ad_min = "0" if tiempo // 60 < 10 else ""
    ad_seg = "0" if tiempo % 60 < 10 else ""
    txt = "{}:{}".format(ad_min + str(tiempo // 60), ad_seg + str(tiempo % 60))
    texto = fuente.render(txt, True, color_texto, color_fondo)
    rect = texto.get_rect(center=pos)
    pantalla.blit(texto, rect)


def ReproducirSonido(mov, fx):  # fx = [fx_captura, fx_jaque, fx_movimiento, fx_jaquemate, fx_coronacion]
    if mov.coronacionPeon:
        sound = fx[4]
    elif mov.piezaCapturada is not None:
        sound = fx[0]
    else:
        sound = fx[2]
    pg.mixer.Sound.play(sound)


# Dibuja el tablero de ajedrez
def MostrarPartida(pantalla, partida, movs, casilla_seleccionada, fuente_movimientos):
    global tablero_invertido
    if not tablero_invertido:
        DibujarTablero(pantalla)  # Dibuja las casillas del tablero
        DibujarPiezas(pantalla, partida.tablero)  # Dibuja las piezas del tablero
        SeleccionarCasillas(pantalla, partida, movs, casilla_seleccionada)  # Dibuja las casillas seleccionadas
    else:
        DibujarTableroReverso(pantalla)  # Dibuja las casillas del tablero
        DibujarPiezasReverso(pantalla, partida.tablero)  # Dibuja las piezas del tablero
        SeleccionarCasillasReverso(pantalla, partida, movs, casilla_seleccionada)  # Dibuja las casillas seleccionadas
    DibujarMovimientos(pantalla, partida, fuente_movimientos)  # Dibuja los movimientos de la partida


def DibujarTablero(pantalla):
    for fila in range(DIMENSION):
        for col in range(DIMENSION):
            color = colores[((fila + col) % 2)]
            pg.draw.rect(pantalla, color, pg.Rect(col * TAM_CASILLA, fila * TAM_CASILLA, TAM_CASILLA, TAM_CASILLA))


def DibujarTableroReverso(pantalla):
    for fila in reversed(range(DIMENSION)):
        for col in reversed(range(DIMENSION)):
            color = colores[((fila + col) % 2)]
            pg.draw.rect(pantalla, color, pg.Rect(inv_pos_cas[col] * TAM_CASILLA, inv_pos_cas[fila] * TAM_CASILLA,
                                                  TAM_CASILLA, TAM_CASILLA))


def SeleccionarCasillas(pantalla, partida, movs, casilla_seleccionada):
    if casilla_seleccionada != ():
        f, c = casilla_seleccionada
        if partida.tablero.casillas[f][c] is not None:
            if partida.tablero.casillas[f][c].color == ('w' if partida.turnoBlanco else 'b'):
                # Pintar un rectángulo azul en la casilla seleccionada
                s = pg.Surface((TAM_CASILLA, TAM_CASILLA))
                s.set_alpha(100)  # Transparencia, 0 es transparente y 255 es opaco
                s.fill(pg.Color('blue'))
                pantalla.blit(s, (c * TAM_CASILLA, f * TAM_CASILLA))
                # Pintar las casillas a las que se puede mover la pieza
                s.fill(pg.Color('yellow'))
                for mov in movs:
                    if mov.fil_inicio == f and mov.col_inicio == c:
                        pantalla.blit(s, (mov.col_fin * TAM_CASILLA, mov.fil_fin * TAM_CASILLA))


def SeleccionarCasillasReverso(pantalla, partida, movs, casilla_seleccionada):
    if casilla_seleccionada != ():
        f, c = casilla_seleccionada
        if partida.tablero.casillas[f][c] is not None:
            if partida.tablero.casillas[f][c].color == ('w' if partida.turnoBlanco else 'b'):
                # Pintar un rectángulo azul en la casilla seleccionada
                s = pg.Surface((TAM_CASILLA, TAM_CASILLA))
                s.set_alpha(100)  # Transparencia, 0 es transparente y 255 es opaco
                s.fill(pg.Color('blue'))
                pantalla.blit(s, (inv_pos_cas[c] * TAM_CASILLA, inv_pos_cas[f] * TAM_CASILLA))
                # Pintar las casillas a las que se puede mover la pieza
                s.fill(pg.Color('yellow'))
                for mov in movs:
                    if mov.fil_inicio == f and mov.col_inicio == c:
                        pantalla.blit(s, (inv_pos_cas[mov.col_fin] * TAM_CASILLA,
                                          inv_pos_cas[mov.fil_fin] * TAM_CASILLA))


def DibujarPiezas(pantalla, tablero):
    for fila in range(DIMENSION):
        for col in range(DIMENSION):
            pieza = tablero.casillas[fila][col]
            if pieza is not None:
                pantalla.blit(imgs[pieza.nombre],
                              pg.Rect(col * TAM_CASILLA, fila * TAM_CASILLA, TAM_CASILLA, TAM_CASILLA))


def DibujarPiezasReverso(pantalla, tablero):
    for fila in reversed(range(DIMENSION)):
        for col in reversed(range(DIMENSION)):
            pieza = tablero.casillas[fila][col]
            if pieza is not None:
                pantalla.blit(imgs[pieza.nombre],
                              pg.Rect(inv_pos_cas[col] * TAM_CASILLA, inv_pos_cas[fila] * TAM_CASILLA,
                                      TAM_CASILLA, TAM_CASILLA))


def DibujarMovimientos(pantalla, partida, fuente):
    rectMov = pg.Rect(ANCHO_T, 0, ANCHO_MOV, ALTURA_MOV)
    pg.draw.rect(pantalla, pg.Color('black'), rectMov)
    lista_movs = partida.movimientos
    texto_movs = []  # Lista de notaciones de los movimientos

    for i in range(0, len(lista_movs), 2):
        strMov = str(i // 2 + 1) + '. ' + lista_movs[i].getNotacion() + ' '
        if i + 1 < len(lista_movs):  # Si hay un movimiento siguiente
            strMov += lista_movs[i + 1].getNotacion() + '  '
        texto_movs.append(strMov)

    mv_x_fila = 3  # Número de movimientos por fila
    fill = 5  # Espacio entre el borde y el texto
    espacio_linea = 3  # Espacio entre cada texto
    dif_y = fill  # Diferencia en altura entre cada texto

    for i in range(0, len(texto_movs), mv_x_fila):
        txt = ''
        for j in range(mv_x_fila):
            if i + j < len(texto_movs):
                txt += texto_movs[i + j]
        obj_texto = fuente.render(txt, True, pg.Color('white'))
        ubc_texto = rectMov.move(fill, dif_y)
        pantalla.blit(obj_texto, ubc_texto)
        dif_y += obj_texto.get_height() + espacio_linea


def Animar_Movimiento(pantalla, mov, tablero, clock):
    df = mov.fil_fin - mov.fil_inicio
    dc = mov.col_fin - mov.col_inicio
    fps_cas = 11  # Velocidad de la animación
    set_frames = (abs(df) + abs(dc)) * fps_cas  # Número de frames de la animación
    for frame in range(set_frames + 1):
        f, c = (mov.fil_inicio + df * frame / set_frames, mov.col_inicio + dc * frame / set_frames)
        DibujarTablero(pantalla)
        DibujarPiezas(pantalla, tablero)
        color = colores[((mov.fil_fin + mov.col_fin) % 2)]
        casilla = pg.Rect(mov.col_fin * TAM_CASILLA, mov.fil_fin * TAM_CASILLA, TAM_CASILLA, TAM_CASILLA)
        pg.draw.rect(pantalla, color, casilla)
        if mov.piezaCapturada is not None:
            if mov.enPassant:
                enPassant_fil = mov.fil_fin + 1 if mov.piezaCapturada.color == 'b' else mov.fil_fin - 1
                casilla = pg.Rect(mov.col_fin * TAM_CASILLA, enPassant_fil * TAM_CASILLA, TAM_CASILLA, TAM_CASILLA)
            pantalla.blit(imgs[mov.piezaCapturada.nombre], casilla)
        pantalla.blit(imgs[mov.piezaMovida.nombre], pg.Rect(c * TAM_CASILLA, f * TAM_CASILLA, TAM_CASILLA, TAM_CASILLA))
        pg.display.flip()
        clock.tick(60)


def Animar_MovimientoReverso(pantalla, mov, tablero, clock):
    df = mov.fil_fin - mov.fil_inicio
    dc = mov.col_fin - mov.col_inicio
    fps_cas = 11  # Velocidad de la animación
    set_frames = (abs(df) + abs(dc)) * fps_cas  # Número de frames de la animación
    for frame in range(set_frames + 1):
        f, c = (mov.fil_inicio + df * frame / set_frames, mov.col_inicio + dc * frame / set_frames)
        DibujarTableroReverso(pantalla)
        DibujarPiezasReverso(pantalla, tablero)
        color = colores[((mov.fil_fin + mov.col_fin) % 2)]
        casilla = pg.Rect(inv_pos_cas[mov.col_fin] * TAM_CASILLA, inv_pos_cas[mov.fil_fin] * TAM_CASILLA,
                          TAM_CASILLA, TAM_CASILLA)
        pg.draw.rect(pantalla, color, casilla)
        if mov.piezaCapturada is not None:
            if mov.enPassant:
                enPassant_fil = mov.fil_fin + 1 if mov.piezaCapturada.color == 'b' else mov.fil_fin - 1
                casilla = pg.Rect(inv_pos_cas[mov.col_fin] * TAM_CASILLA, inv_pos_cas[enPassant_fil] * TAM_CASILLA,
                                  TAM_CASILLA, TAM_CASILLA)
            pantalla.blit(imgs[mov.piezaCapturada.nombre], casilla)
        pantalla.blit(imgs[mov.piezaMovida.nombre], pg.Rect(c * TAM_CASILLA, f * TAM_CASILLA,
                                                            TAM_CASILLA, TAM_CASILLA))
        pg.display.flip()
        clock.tick(60)


def dibujarTextoFinal(pantalla, texto):
    fuente = pg.font.SysFont('Times New Roman', 40, True, False)
    obj_texto = fuente.render(texto, 0, pg.Color('Black'))
    locacion_texto = pg.Rect(0, 0, ANCHO_T, ALTURA_T).move(ANCHO_T / 2 - obj_texto.get_width() / 2, ALTURA_T
                                                           / 2 - obj_texto.get_height() / 2)
    pantalla.blit(obj_texto, locacion_texto)
    # obj_texto = fuente.render(texto, 0, pg.Color('Gray'))
    # pantalla.blit(obj_texto, locacion_texto.move(2, 2))


if __name__ == "__main__":
    main()

# UI improvements:
# -Menu to select AI/Human
# -Flip board options (display from black perspective)
# -Change color of board/pieces - different piece skins
# -Mouse click/drag for pieces
#
# Engine improvements:
# -Add 50 move draw and 3 move repeating draw rule
# -Move ordering - look at checks, captures and threats first, prioritize castling/king safety, look at pawn moves
#   last (this will improve alpha-beta pruning). Also start with moves that previously
#   scored higher (will also improve pruning).
# -Calculate both players moves given a position
# -Change move calculation to make it more efficient. Instead of recalculating all moves, start with moves
#   from previous board and change based on last move made
# -Use a numpy array instead of 2d list of strings or store the board differently
# -Hash board positions already visited to improve computation time for transpositions.
# -If move is a capture move, even at max depth, continue evaluating until no captures remain
