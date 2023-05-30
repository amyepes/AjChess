""" Módulo que se encarga de dibujar el menú principal del juego."""

import pygame as pg
import Main

# Configuración de colores
COLOR_FONDO = (40, 40, 40)
COLOR_TITULO = (169, 50, 38)
COLOR_OPCIONES = (180, 180, 180)
COLOR_OPCION_SELECCIONADA = (255, 255, 255)

# Configuración de música
MUSICA_FONDO = "sounds/Lethal-Industry.mp3"
volumen_soundtrack = 0.2

# Dimensiones de la pantalla
ANCHO_PANTALLA = 705
ALTO_PANTALLA = 475

IMG_FONDO = pg.image.load("pictures/ajchess_logo.png")

JUGADOR1 = False
JUGADOR2 = False
TIEMPO_LIM = 900
DIFF = 3


class Menu:
    def __init__(self, opciones):
        self.opciones: list = opciones
        self.font_titulo = pg.font.Font(None, 80)
        self.font_opciones = pg.font.Font(None, 40)
        self.seleccionado = 0

    def mostrar_menu_principal(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP or event.key == pg.K_LEFT:
                        self.seleccionado = (self.seleccionado - 1) % len(self.opciones)
                    elif event.key == pg.K_DOWN or event.key == pg.K_RIGHT:
                        self.seleccionado = (self.seleccionado + 1) % len(self.opciones)
                    elif event.key == pg.K_RETURN:
                        if self.seleccionado == 0:
                            # Lógica para iniciar el juego
                            Main.main(j1=JUGADOR1, j2=JUGADOR2, tiempo_lim=TIEMPO_LIM, prof_ia=DIFF)
                            pg.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
                        elif self.seleccionado == 1:
                            opciones = ["Dificultad", "Modos", "Volumen", "Regresar"]
                            op = Menu(opciones)
                            op.mostrar_menu()
                            pass
                        elif self.seleccionado == 2:
                            # Lógica para ayuda
                            pass
                        elif self.seleccionado == 3:
                            pg.quit()
                            exit()

            pantalla.fill(COLOR_FONDO)
            pantalla.blit(IMG_FONDO, (0, 0))
            # self.mostrar_titulo()
            self.mostrar_opciones()
            pg.display.flip()

    def mostrar_menu(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP or event.key == pg.K_LEFT:
                        self.seleccionado = (self.seleccionado - 1) % len(self.opciones)
                    elif event.key == pg.K_DOWN or event.key == pg.K_RIGHT:
                        self.seleccionado = (self.seleccionado + 1) % len(self.opciones)
                    elif event.key == pg.K_RETURN:
                        if self.seleccionado == 0:
                            pass
                        elif self.seleccionado == 1:
                            pass
                        elif self.seleccionado == 2:
                            pass
                        elif self.seleccionado == 3:
                            op_menu = ["Jugar", "Opciones", "Ayuda", "Salir"]
                            menu = Menu(op_menu)
                            menu.mostrar_menu_principal()

            pantalla.fill(COLOR_FONDO)
            pantalla.blit(IMG_FONDO, (0, 0))
            # self.mostrar_titulo()
            self.mostrar_opciones()
            pg.display.flip()

    def mostrar_titulo(self):
        titulo = self.font_titulo.render("AjChess", True, COLOR_TITULO)
        pos_x = (ANCHO_PANTALLA - titulo.get_width()) // 2
        pos_y = 100
        pantalla.blit(titulo, (pos_x, pos_y))

    def mostrar_opciones(self):
        for i, opcion in enumerate(self.opciones):
            texto = self.font_opciones.render(opcion, True,
                                              COLOR_OPCION_SELECCIONADA if i == self.seleccionado else COLOR_OPCIONES)
            pos_x = 100  # (ANCHO_PANTALLA - texto.get_width()) // 2
            pos_y = 120 + i * 60
            pantalla.blit(texto, (pos_x, pos_y))


if __name__ == "__main__":
    pg.init()
    pantalla = pg.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pg.display.set_caption("AjChess - Menú")

    # pg.mixer.init()
    # pg.mixer.music.load(MUSICA_FONDO)
    # pg.mixer.music.set_volume(volumen_soundtrack)
    # pg.mixer.music.play(-1)

    opciones_menu = ["Jugar", "Opciones", "Ayuda", "Salir"]
    men = Menu(opciones_menu)
    men.mostrar_menu_principal()
