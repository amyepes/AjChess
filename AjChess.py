class ficha:
    def __int__(self):
        self.tipo = None
        self.posición = None
        self.color = None


class Tablero:
    def __int__(self):
        self.id = None
        self.posPieza = None

    def MoverPieza(self):
        pass

    def VerEstadoJuego(self):
        pass

    def ValidarMovimiento(self):
        pass


class Jugador:
    def __int__(self):
        self.nombre = None
        self.puntuación = None
        self.piezasCapt = None
        self.turnoActual = None
        self.MovimientosPosibles = None


class Partida:
    def __int__(self):
        self.jugador1 = None
        self.jugador2 = None
        self.estadoJuego = None
        self.movimientosJugados = None

    def Iniciar(self):
        pass

    def Parar(self):
        pass

    def Guardar(self):
        pass
