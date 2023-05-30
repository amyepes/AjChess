""" Guarda la información del estado actual de la partida,
determina movimientos legales y realiza los movimientos. """


class Partida:
    def __init__(self):
        self.tablero = Tablero()
        self.turnoBlanco: bool = True
        self.funcionesMovimiento = {"p": GeneradorMovimientos.getMovimientosPeon,
                                    "R": GeneradorMovimientos.getMovimientosTorre,
                                    "N": GeneradorMovimientos.getMovimientosCaballo,
                                    "B": GeneradorMovimientos.getMovimientosAlfil,
                                    "Q": GeneradorMovimientos.getMovimientosDama,
                                    "K": GeneradorMovimientos.getMovimientosRey}
        self.movimientos: list = []  # Lista de movimientos realizados en la partida
        self.casillaReyBlanco: tuple = (7, 4)
        self.casillaReyNegro: tuple = (0, 4)
        self.enJaque: bool = False
        self.clavadas = []  # Lista de piezas clavadas: (posición, dirección)
        self.jaques = []  # Lista de piezas que dan jaque: (posición, dirección)
        self.jaquemate: bool = False
        self.tablas: bool = False
        self.cas_enPassant = ()  # Casilla para captura en passant
        self.registro_cas_enPassant = [self.cas_enPassant]  # Registro de casillas en passant anteriores
        self.enroqueBlancoCorto = True
        self.enroqueBlancoLargo = True
        self.enroqueNegroCorto = True
        self.enroqueNegroLargo = True
        self.registroEnroquesPosibles = [EnroquesPosibles(self.enroqueBlancoCorto, self.enroqueNegroCorto,
                                                          self.enroqueBlancoLargo, self.enroqueNegroLargo)]

    def Mover(self, mvm):  # Realiza el movimiento
        self.tablero.casillas[mvm.fil_inicio][mvm.col_inicio] = None
        self.tablero.casillas[mvm.fil_fin][mvm.col_fin] = mvm.piezaMovida
        self.movimientos.append(mvm)  # Guarda el movimiento en la lista de movimientos
        self.turnoBlanco = not self.turnoBlanco  # Cambia el turno

        if mvm.piezaMovida.tipo == "K":  # Actualiza las posiciones del rey si se mueve
            if mvm.piezaMovida.color == "w":
                self.casillaReyBlanco = (mvm.fil_fin, mvm.col_fin)
            else:
                self.casillaReyNegro = (mvm.fil_fin, mvm.col_fin)

        if mvm.piezaMovida.tipo == "p" and abs(mvm.fil_inicio - mvm.fil_fin) == 2:  # Si el peón se mueve 2 casillas
            self.cas_enPassant = ((mvm.fil_inicio + mvm.fil_fin) // 2, mvm.col_inicio)
        else:  # Si no se mueve 2 casillas
            self.cas_enPassant = ()

        if mvm.enPassant:  # Si se captura en passant
            self.tablero.casillas[mvm.fil_inicio][mvm.col_fin] = None  # Elimina el peón capturado

        if mvm.coronacionPeon:  # Si el peón se corona
            print('Promoción!')  # Añadir a GUI, piezaPromovida
            self.tablero.casillas[mvm.fil_fin][mvm.col_fin] = Pieza(mvm.piezaMovida.color + "Q")

        if mvm.enroque:
            if mvm.col_fin - mvm.col_inicio == 2:  # Enroque corto
                self.tablero.casillas[mvm.fil_fin][mvm.col_fin - 1] = \
                    self.tablero.casillas[mvm.fil_fin][mvm.col_fin + 1]
                self.tablero.casillas[mvm.fil_fin][mvm.col_fin + 1] = None
            else:  # Enroque largo
                self.tablero.casillas[mvm.fil_fin][mvm.col_fin + 1] = \
                    self.tablero.casillas[mvm.fil_fin][mvm.col_fin - 2]
                self.tablero.casillas[mvm.fil_fin][mvm.col_fin - 2] = None

        self.registro_cas_enPassant.append(self.cas_enPassant)  # Guarda la casilla en passant en el registro
        self.actualizarEnroques(mvm)  # Actualiza los enroques posibles
        self.registroEnroquesPosibles.append(EnroquesPosibles(self.enroqueBlancoCorto, self.enroqueNegroCorto,
                                                              self.enroqueBlancoLargo, self.enroqueNegroLargo))

    def Deshacer(self):  # Deshace el último movimiento
        if len(self.movimientos) != 0:  # Ya se ha movido una pieza en la partida
            mvm = self.movimientos.pop()
            self.tablero.casillas[mvm.fil_inicio][mvm.col_inicio] = mvm.piezaMovida
            self.tablero.casillas[mvm.fil_fin][mvm.col_fin] = mvm.piezaCapturada
            self.turnoBlanco = not self.turnoBlanco
            self.jaquemate = False
            self.tablas = False
            if mvm.piezaMovida.tipo == "K":
                if mvm.piezaMovida.color == "w":
                    self.casillaReyBlanco = (mvm.fil_inicio, mvm.col_inicio)
                else:
                    self.casillaReyNegro = (mvm.fil_inicio, mvm.col_inicio)

            if mvm.enPassant:
                self.tablero.casillas[mvm.fil_fin][mvm.col_fin] = None
                self.tablero.casillas[mvm.fil_inicio][mvm.col_fin] = mvm.piezaCapturada

            self.registro_cas_enPassant.pop()
            self.cas_enPassant = self.registro_cas_enPassant[-1]

            self.registroEnroquesPosibles.pop()
            enroquesPosibles = self.registroEnroquesPosibles[-1]
            self.enroqueBlancoCorto = enroquesPosibles.eBC
            self.enroqueNegroCorto = enroquesPosibles.eNC
            self.enroqueBlancoLargo = enroquesPosibles.eBL
            self.enroqueNegroLargo = enroquesPosibles.eNL

            if mvm.enroque:
                if mvm.col_fin - mvm.col_inicio == 2:  # Enroque corto
                    self.tablero.casillas[mvm.fil_fin][mvm.col_fin + 1] = \
                        self.tablero.casillas[mvm.fil_fin][mvm.col_fin - 1]
                    self.tablero.casillas[mvm.fil_fin][mvm.col_fin - 1] = None
                else:  # Enroque largo
                    self.tablero.casillas[mvm.fil_fin][mvm.col_fin - 2] = \
                        self.tablero.casillas[mvm.fil_fin][mvm.col_fin + 1]
                    self.tablero.casillas[mvm.fil_fin][mvm.col_fin + 1] = None

    def movimientos_legales(self):
        movs = []
        self.enJaque, self.clavadas, self.jaques = self.Jaques_y_clavadas()
        if self.turnoBlanco:
            rey = self.casillaReyBlanco
        else:
            rey = self.casillaReyNegro
        if self.enJaque:
            if len(self.jaques) == 1:
                movs = self.movimientos_posibles()
                jaque = self.jaques[0]
                pieza = self.tablero.casillas[jaque[0]][jaque[1]]
                casillasLegales = []
                if pieza.tipo == "N":
                    casillasLegales = [(jaque[0], jaque[1])]
                else:
                    for i in range(1, 8):
                        casillaLegal = (rey[0] + jaque[2] * i, rey[1] + jaque[3] * i)
                        casillasLegales.append(casillaLegal)
                        if casillaLegal[0] == jaque[0] and casillaLegal[1] == jaque[1]:
                            break
                for i in range(len(movs) - 1, -1, -1):
                    if movs[i].piezaMovida.tipo != "K":
                        if not (movs[i].fil_fin, movs[i].col_fin) in casillasLegales:
                            movs.remove(movs[i])
            else:
                GeneradorMovimientos.getMovimientosRey(self, rey[0], rey[1], movs)
        else:
            movs = self.movimientos_posibles()
            if self.turnoBlanco:
                self.getEnroques(self.casillaReyBlanco[0], self.casillaReyBlanco[1], movs)
            else:
                self.getEnroques(self.casillaReyNegro[0], self.casillaReyNegro[1], movs)

        if len(movs) == 0:
            if self.enJaque:
                self.jaquemate = True
            else:
                self.tablas = True
        else:
            self.jaquemate = False
            self.tablas = False
        return movs

    def Jaques_y_clavadas(self):  # Revisa si el rey está en jaque o si hay piezas clavadas
        clavadas = []  # Guarda las piezas clavadas y la dirección de la pieza atacante
        jaques = []  # Guarda las casillas donde las fichas enemigas aplican el jaque
        enJaque = False
        if self.turnoBlanco:
            fila_rey = self.casillaReyBlanco[0]
            col_rey = self.casillaReyBlanco[1]
            enemigo = "b"
            aliado = "w"
        else:
            fila_rey = self.casillaReyNegro[0]
            col_rey = self.casillaReyNegro[1]
            enemigo = "w"
            aliado = "b"
        direcciones = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))  # Direcciones de ataque
        for j in range(len(direcciones)):
            d = direcciones[j]
            clavadasPosibles = ()
            for i in range(1, 8):
                fila = fila_rey + d[0] * i
                col = col_rey + d[1] * i
                if 0 <= fila <= 7 and 0 <= col <= 7:
                    cas_pieza = self.tablero.casillas[fila][col]
                    if cas_pieza is not None:
                        if cas_pieza.color == aliado and cas_pieza.tipo != "K":
                            if len(clavadasPosibles) == 0:  # clavadasPosibles == ()
                                clavadasPosibles = (fila, col, d[0], d[1])
                            else:  # Hay más de una pieza aliada en la misma dirección
                                break
                        elif cas_pieza.color == enemigo:
                            tipo = cas_pieza.tipo
                            if (0 <= j <= 3 and tipo == "R") or \
                                    (4 <= j <= 7 and tipo == "B") or \
                                    (i == 1 and tipo == "p" and ((enemigo == "w" and 6 <= j <= 7) or
                                                                 (enemigo == "b" and 4 <= j <= 5))) or \
                                    (tipo == "Q") or (i == 1 and tipo == "K"):
                                if len(clavadasPosibles) == 0:  # clavadasPosibles == ()
                                    enJaque = True
                                    jaques.append((fila, col, d[0], d[1]))
                                    break
                                else:
                                    clavadas.append(clavadasPosibles)
                                    break
                            else:  # Pieza enemiga que no aplica jaque
                                break
                else:  # Fuera del tablero
                    break
        drc_caballo = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))  # Ataques de caballo
        for drc in drc_caballo:
            fila = fila_rey + drc[0]
            col = col_rey + drc[1]
            if 0 <= fila <= 7 and 0 <= col <= 7:
                cas_pz = self.tablero.casillas[fila][col]
                if cas_pz is not None:
                    if cas_pz.color == enemigo and cas_pz.tipo == "N":
                        enJaque = True
                        jaques.append((fila, col, drc[0], drc[1]))
        return enJaque, clavadas, jaques

    def movimientos_posibles(self) -> list:
        movs = []
        for fila in range(len(self.tablero.casillas)):
            for col in range(len(self.tablero.casillas[fila])):
                pieza = self.tablero.casillas[fila][col]
                if pieza is not None:
                    if (pieza.color == "w" and self.turnoBlanco) or (pieza.color == "b" and not self.turnoBlanco):
                        self.funcionesMovimiento[pieza.tipo](self, fila, col, movs)  # Llama a la función adecuada
        return movs

    def getEnroques(self, fil, col, movs):
        if (self.turnoBlanco and self.registroEnroquesPosibles[-1].eBC) or (
                not self.turnoBlanco and self.registroEnroquesPosibles[-1].eNC):
            self.getEnroqueCorto(fil, col, movs)
        if (self.turnoBlanco and self.registroEnroquesPosibles[-1].eBL) or (
                not self.turnoBlanco and self.registroEnroquesPosibles[-1].eNL):
            self.getEnroqueLargo(fil, col, movs)

    def getEnroqueCorto(self, fil, col, movs):
        if self.tablero.casillas[fil][col + 1] is None and self.tablero.casillas[fil][col + 2] is None:
            if not GeneradorMovimientos.Casilla_Atacada(self, fil, col + 1) and \
                    not GeneradorMovimientos.Casilla_Atacada(self, fil, col + 2):
                movs.append(Movimiento((fil, col), (fil, col + 2), self.tablero, enroque=True))

    def getEnroqueLargo(self, fil, col, movs):
        if self.tablero.casillas[fil][col - 1] is None and self.tablero.casillas[fil][col - 2] is None \
                and self.tablero.casillas[fil][col - 3] is None:
            if not GeneradorMovimientos.Casilla_Atacada(self, fil, col - 1) and \
                    not GeneradorMovimientos.Casilla_Atacada(self, fil, col - 2) and \
                    not GeneradorMovimientos.Casilla_Atacada(self, fil, col - 3):
                movs.append(Movimiento((fil, col), (fil, col - 2), self.tablero, enroque=True))

    def actualizarEnroques(self, mvm):
        if mvm.piezaMovida.tipo == "K" and mvm.piezaMovida.color == "w":
            self.enroqueBlancoCorto = False
            self.enroqueBlancoLargo = False
        elif mvm.piezaMovida.tipo == "K" and mvm.piezaMovida.color == "b":
            self.enroqueNegroCorto = False
            self.enroqueNegroLargo = False
        elif mvm.piezaMovida.tipo == "R" and mvm.piezaMovida.color == "w":
            if mvm.fil_inicio == 7:
                if mvm.col_inicio == 7:
                    self.enroqueBlancoCorto = False
                elif mvm.col_inicio == 0:
                    self.enroqueBlancoLargo = False
        elif mvm.piezaMovida.tipo == "R" and mvm.piezaMovida.color == "b":
            if mvm.fil_inicio == 0:
                if mvm.col_inicio == 7:
                    self.enroqueNegroCorto = False
                elif mvm.col_inicio == 0:
                    self.enroqueNegroLargo = False

        if mvm.piezaCapturada is not None:
            if mvm.piezaCapturada.tipo == "R" and mvm.piezaCapturada.color == "w":
                if mvm.fil_fin == 7:
                    if mvm.col_fin == 7:
                        self.enroqueBlancoCorto = False
                    elif mvm.col_fin == 0:
                        self.enroqueBlancoLargo = False
            elif mvm.piezaCapturada.tipo == "R" and mvm.piezaCapturada.color == "b":
                if mvm.fil_fin == 0:
                    if mvm.col_fin == 7:
                        self.enroqueNegroCorto = False
                    elif mvm.col_fin == 0:
                        self.enroqueNegroLargo = False


# noinspection PyAttributeOutsideInit
class GeneradorMovimientos:
    def Casilla_Atacada(partida, fila, col) -> bool:
        partida.turnoBlanco = not partida.turnoBlanco
        movs_oponente = partida.movimientos_posibles()
        partida.turnoBlanco = not partida.turnoBlanco
        for m in movs_oponente:
            if m.fil_fin == fila and m.col_fin == col:
                return True
        return False

    def getMovimientosPeon(partida, fila, col, movs):
        piezaClavada = False
        drc_clavada = ()
        for i in range(len(partida.clavadas) - 1, -1, -1):
            if partida.clavadas[i][0] == fila and partida.clavadas[i][1] == col:
                piezaClavada = True
                drc_clavada = (partida.clavadas[i][2], partida.clavadas[i][3])
                partida.clavadas.remove(partida.clavadas[i])
                break

        if partida.turnoBlanco:
            mov_num = -1
            fil_inicio = 6
            enemigo = "b"
            fil_rey, col_rey = partida.casillaReyBlanco
        else:
            mov_num = 1
            fil_inicio = 1
            enemigo = "w"
            fil_rey, col_rey = partida.casillaReyNegro

        if partida.tablero.casillas[fila + mov_num][col] is None:  # Movimiento de una casilla
            if not piezaClavada or drc_clavada == (mov_num, 0):
                movs.append(Movimiento((fila, col), (fila + mov_num, col), partida.tablero))
                if fila == fil_inicio and partida.tablero.casillas[fila + 2 * mov_num][col] is None:
                    movs.append(Movimiento((fila, col), (fila + 2 * mov_num, col), partida.tablero))

        if col - 1 >= 0:  # Captura por izquierda
            if partida.tablero.casillas[fila + mov_num][col - 1] is not None:
                if not piezaClavada or drc_clavada == (mov_num, -1):
                    if partida.tablero.casillas[fila + mov_num][col - 1].color == enemigo:
                        movs.append(Movimiento((fila, col), (fila + mov_num, col - 1), partida.tablero))

            if len(partida.cas_enPassant) > 0 and (not piezaClavada or drc_clavada == (mov_num, -1)):
                if (fila + mov_num) == partida.cas_enPassant[0] and col - 1 == partida.cas_enPassant[1]:
                    piezaAtacante = piezaDefensora = False
                    if fil_rey == fila:
                        if col_rey < col:
                            rangointerior = range(col_rey + 1, col - 1)
                            rangoexterior = range(col + 1, 8)
                        else:
                            rangointerior = range(col_rey - 1, col, -1)
                            rangoexterior = range(col - 2, -1, -1)
                        for i in rangointerior:
                            if partida.tablero.casillas[fila][i] is not None:
                                piezaDefensora = True
                                break
                        for i in rangoexterior:
                            p = partida.tablero.casillas[fila][i]
                            if p is not None:
                                if p.color == enemigo and (p.tipo == "R" or p.tipo == "Q"):
                                    piezaAtacante = True
                                    break
                                else:
                                    piezaDefensora = True
                                    break
                    if not piezaAtacante or piezaDefensora:
                        movs.append(Movimiento((fila, col), (fila + mov_num, col - 1),
                                               partida.tablero, b_enpassant=True))

        if col + 1 <= 7:  # Captura por derecha
            if partida.tablero.casillas[fila + mov_num][col + 1] is not None:
                if not piezaClavada or drc_clavada == (mov_num, 1):
                    if partida.tablero.casillas[fila + mov_num][col + 1].color == enemigo:
                        movs.append(Movimiento((fila, col), (fila + mov_num, col + 1), partida.tablero))

            if len(partida.cas_enPassant) > 0 and (not piezaClavada or drc_clavada == (mov_num, -1)):
                if (fila + mov_num) == partida.cas_enPassant[0] and col + 1 == partida.cas_enPassant[1]:
                    piezaAtacante = piezaDefensora = False
                    if fil_rey == fila:
                        if col_rey < col:
                            rangointerior = range(col_rey + 1, col)
                            rangoexterior = range(col + 2, 8)
                        else:
                            rangointerior = range(col_rey - 1, col + 1, -1)
                            rangoexterior = range(col - 1, -1, -1)
                        for i in rangointerior:
                            if partida.tablero.casillas[fila][i] is not None:
                                piezaDefensora = True
                                break
                        for i in rangoexterior:
                            p = partida.tablero.casillas[fila][i]
                            if p is not None:
                                if p.color == enemigo and (p.tipo == "R" or p.tipo == "Q"):
                                    piezaAtacante = True
                                    break
                                else:
                                    piezaDefensora = True
                                    break
                    if not piezaAtacante or piezaDefensora:
                        movs.append(Movimiento((fila, col), (fila + mov_num, col + 1),
                                               partida.tablero, b_enpassant=True))

    def getMovimientosTorre(partida, fila, col, movs):
        piezaClavada = False
        drc_clavada = ()
        for i in range(len(partida.clavadas) - 1, -1, -1):
            if partida.clavadas[i][0] == fila and partida.clavadas[i][1] == col:
                piezaClavada = True
                drc_clavada = (partida.clavadas[i][2], partida.clavadas[i][3])
                if partida.tablero.casillas[fila][col].tipo != "Q":
                    partida.clavadas.remove(partida.clavadas[i])
                break
        direcciones = [(-1, 0), (0, -1), (1, 0), (0, 1)]  # Arriba, izquierda, abajo, derecha
        enemigo = "b" if partida.turnoBlanco else "w"
        for d in direcciones:
            for i in range(1, 8):
                nueva_fila = fila + d[0] * i
                nueva_col = col + d[1] * i
                if (0 <= nueva_fila < 8) and (0 <= nueva_col < 8):
                    if not piezaClavada or drc_clavada == d or drc_clavada == (-d[0], -d[1]):
                        if partida.tablero.casillas[nueva_fila][nueva_col] is None:
                            movs.append(Movimiento((fila, col), (nueva_fila, nueva_col), partida.tablero))
                        elif partida.tablero.casillas[nueva_fila][nueva_col].color == enemigo:
                            movs.append(Movimiento((fila, col), (nueva_fila, nueva_col), partida.tablero))
                            break
                        else:
                            break
                else:
                    break

    def getMovimientosCaballo(partida, fila, col, movs):
        piezaClavada = False
        for i in range(len(partida.clavadas) - 1, -1, -1):
            if partida.clavadas[i][0] == fila and partida.clavadas[i][1] == col:
                piezaClavada = True
                partida.clavadas.remove(partida.clavadas[i])
                break
        direcciones = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        aliado = "w" if partida.turnoBlanco else "b"
        for d in direcciones:
            nueva_fila = fila + d[0]
            nueva_col = col + d[1]
            if 0 <= nueva_fila <= 7 and 0 <= nueva_col <= 7:
                if not piezaClavada:
                    if partida.tablero.casillas[nueva_fila][nueva_col] is None:
                        movs.append(Movimiento((fila, col), (nueva_fila, nueva_col), partida.tablero))
                    elif partida.tablero.casillas[nueva_fila][nueva_col].color != aliado:
                        movs.append(Movimiento((fila, col), (nueva_fila, nueva_col), partida.tablero))

    def getMovimientosAlfil(partida, fila, col, movs):

        piezaClavada = False
        drc_clavada = ()
        for i in range(len(partida.clavadas) - 1, -1, -1):
            if partida.clavadas[i][0] == fila and partida.clavadas[i][1] == col:
                piezaClavada = True
                drc_clavada = (partida.clavadas[i][2], partida.clavadas[i][3])
                partida.clavadas.remove(partida.clavadas[i])
                break
        direcciones = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        enemigo = "b" if partida.turnoBlanco else "w"
        for d in direcciones:
            for i in range(1, 8):
                nueva_fila = fila + d[0] * i
                nueva_col = col + d[1] * i
                if 0 <= nueva_fila <= 7 and 0 <= nueva_col <= 7:
                    if not piezaClavada or drc_clavada == d or drc_clavada == (-d[0], -d[1]):
                        if partida.tablero.casillas[nueva_fila][nueva_col] is None:
                            movs.append(Movimiento((fila, col), (nueva_fila, nueva_col), partida.tablero))
                        elif partida.tablero.casillas[nueva_fila][nueva_col].color == enemigo:
                            movs.append(Movimiento((fila, col), (nueva_fila, nueva_col), partida.tablero))
                            break
                        else:
                            break  # Si hay una pieza aliada, no se puede seguir moviendo en esa dirección
                else:
                    break  # Movimiento fuera de tablero

    def getMovimientosDama(partida, fila, col, movs):
        GeneradorMovimientos.getMovimientosTorre(partida, fila, col, movs)
        GeneradorMovimientos.getMovimientosAlfil(partida, fila, col, movs)

    # noinspection PyAttributeOutsideInit
    def getMovimientosRey(partida, fila, col, movs):
        mov_fil = (-1, -1, -1, 0, 0, 1, 1, 1)
        mov_col = (-1, 0, 1, -1, 1, -1, 0, 1)
        aliado = "w" if partida.turnoBlanco else "b"
        for i in range(8):
            nueva_fila = fila + mov_fil[i]
            nueva_col = col + mov_col[i]
            if 0 <= nueva_fila <= 7 and 0 <= nueva_col <= 7:
                pz = partida.tablero.casillas[nueva_fila][nueva_col]
                if pz is None:
                    if aliado == "w":
                        partida.casillaReyBlanco = (nueva_fila, nueva_col)
                    else:
                        partida.casillaReyNegro = (nueva_fila, nueva_col)
                    enJaque, clavadas, jaques = partida.Jaques_y_clavadas()
                    if not enJaque:
                        movs.append(Movimiento((fila, col), (nueva_fila, nueva_col), partida.tablero))
                    if aliado == "w":
                        partida.casillaReyBlanco = (fila, col)
                    else:
                        partida.casillaReyNegro = (fila, col)
                elif pz.color != aliado:
                    if aliado == "w":
                        partida.casillaReyBlanco = (nueva_fila, nueva_col)
                    else:
                        partida.casillaReyNegro = (nueva_fila, nueva_col)
                    enJaque, clavadas, jaques = partida.Jaques_y_clavadas()
                    if not enJaque:
                        movs.append(Movimiento((fila, col), (nueva_fila, nueva_col), partida.tablero))
                    if aliado == "w":
                        partida.casillaReyBlanco = (fila, col)
                    else:
                        partida.casillaReyNegro = (fila, col)


class Tablero:
    def __init__(self):
        self.casillas = [
            [Pieza("bR"), Pieza("bN"), Pieza("bB"), Pieza("bQ"), Pieza("bK"), Pieza("bB"), Pieza("bN"), Pieza("bR")],
            [Pieza("bp") for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [None for _ in range(8)],
            [Pieza("wp") for _ in range(8)],
            [Pieza("wR"), Pieza("wN"), Pieza("wB"), Pieza("wQ"), Pieza("wK"), Pieza("wB"), Pieza("wN"), Pieza("wR")]]


class Pieza:
    def __init__(self, nombre):
        self.nombre = nombre
        self.color = nombre[0]
        self.tipo = nombre[1]
        # Las piezas utilizan una notación de dos caracteres en inglés: color y tipo


class EnroquesPosibles:
    def __init__(self, enroqueblancocorto, enroquenegrocorto, enroqueblancolargo, enroquenegrolargo):
        self.eBC = enroqueblancocorto
        self.eNC = enroquenegrocorto
        self.eBL = enroqueblancolargo
        self.eNL = enroquenegrolargo


class Movimiento:
    filas = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    filas_inv = {v: k for k, v in filas.items()}
    columnas = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    columnas_inv = {v: k for k, v in columnas.items()}

    def __init__(self, inicio, fin, tablero, b_enpassant=False, enroque=False):
        self.fil_inicio = inicio[0]
        self.col_inicio = inicio[1]
        self.fil_fin = fin[0]
        self.col_fin = fin[1]
        self.piezaMovida = tablero.casillas[self.fil_inicio][self.col_inicio]
        self.piezaCapturada = tablero.casillas[self.fil_fin][self.col_fin]
        # Coronación de peón
        if self.piezaMovida is not None:
            self.coronacionPeon = self.piezaMovida.tipo == "p" and (self.fil_fin == 0 or self.fil_fin == 7)
        # Enroque posible o no
        self.enroque = enroque
        # Posible realizar captura en passant
        self.enPassant = b_enpassant
        if self.enPassant:
            if self.piezaMovida.color == "w":
                self.piezaCapturada = Pieza("bp")
            else:
                self.piezaCapturada = Pieza("wp")
        self.ID = self.fil_inicio * 1000 + self.col_inicio * 100 + self.fil_fin * 10 + self.col_fin

    def __eq__(self, other) -> bool:
        if isinstance(other, Movimiento):
            return self.ID == other.ID
        return False

    def getNotacion(self) -> str:
        if self.enroque:
            return "0-0" if self.col_fin == 6 else "0-0-0"
        tipo = ''
        if self.piezaMovida is not None:
            tipo = self.piezaMovida.tipo if self.piezaMovida.tipo != 'p' else ''
        cap = 'x' if self.piezaCapturada is not None else ''
        col_cap = self.columnas_inv[self.col_inicio] if (self.piezaCapturada is not None
                                                         and not (self.piezaMovida.tipo == 'Q'
                                                                  or self.piezaMovida.tipo == 'K')) else ''
        fn = self.columnas_inv[self.col_fin] + self.filas_inv[self.fil_fin]
        return tipo + col_cap + cap + fn


class Jugador:
    def __init__(self, nombre='', humano=True) -> None:
        self.nombre = nombre
        self.humano = humano
