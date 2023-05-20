import pygame as pg
import Main

# Configuración de colores
COLOR_FONDO = (40, 40, 40)
COLOR_TITULO = (180, 255, 180)
COLOR_OPCIONES = (180, 180, 180)
COLOR_OPCION_SELECCIONADA = (255, 255, 255)

# Configuración de música
MUSICA_FONDO = "Lethal-Industry.mp3"
volumen_soundtrack = 0.4

# Dimensiones de la pantalla
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600


class Menu:
    def __init__(self, opciones):
        self.opciones = opciones
        self.font_titulo = pg.font.Font(None, 80)
        self.font_opciones = pg.font.Font(None, 40)
        self.seleccionado = 0

    def mostrar_menu(self):
        pg.mixer.music.load(MUSICA_FONDO)
        pg.mixer.music.set_volume(volumen_soundtrack)
        pg.mixer.music.play(-1)

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        self.seleccionado = (self.seleccionado - 1) % len(self.opciones)
                    elif event.key == pg.K_DOWN:
                        self.seleccionado = (self.seleccionado + 1) % len(self.opciones)
                    elif event.key == pg.K_RETURN:
                        if self.seleccionado == 0:
                            # Lógica para iniciar el juego
                            Main.main(j1=False, j2=False)
                            pg.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
                        elif self.seleccionado == 1:
                            # Lógica para opciones
                            pass
                        elif self.seleccionado == 2:
                            # Lógica para ayuda
                            pass
                        elif self.seleccionado == 3:
                            pg.quit()
                            exit()

            pantalla.fill(COLOR_FONDO)
            self.mostrar_titulo()
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
            pos_x = (ANCHO_PANTALLA - texto.get_width()) // 2
            pos_y = 250 + i * 60
            pantalla.blit(texto, (pos_x, pos_y))


if __name__ == "__main__":
    pg.init()
    pantalla = pg.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pg.display.set_caption("AjChess")
    pg.mixer.init()

    opciones_menu = ["Jugar", "Opciones", "Ayuda", "Salir"]
    men = Menu(opciones_menu)
    men.mostrar_menu()
