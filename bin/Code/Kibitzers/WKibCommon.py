from PySide2 import QtCore, QtGui, QtWidgets

import FasterCode

import Code
from Code.Base import Game
from Code.Kibitzers import Kibitzers
from Code.QT import Piezas
from Code.Board import Board
from Code.QT import Delegados
from Code.QT import Voyager
from Code.QT import QTUtil
from Code.QT import QTVarios
from Code.QT import Iconos


class WKibCommon(QtWidgets.QDialog):
    def __init__(self, cpu, icon):
        QtWidgets.QDialog.__init__(self)
        self.setWindowTitle(cpu.titulo)
        self.setWindowIcon(icon)

        self.cpu = cpu
        self.siPlay = True
        self.kibitzer = cpu.kibitzer
        self.type = cpu.tipo
        self.dicVideo = self.cpu.dic_video
        if not self.dicVideo:
            self.dicVideo = {}
        self.game = None
        self.li_moves = []
        self.is_black = True
        self.is_white = True

        self.siTop = self.dicVideo.get("SITOP", True)
        self.show_board = self.dicVideo.get("SHOW_BOARD", True)
        self.nArrows = self.dicVideo.get("NARROWS", 1 if cpu.tipo == Kibitzers.KIB_THREATS else 2)

        self.setWindowFlags(
            QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.Dialog | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowMinimizeButtonHint
        )

        self.setBackgroundRole(QtGui.QPalette.Light)

        Code.configuration = cpu.configuration

        Code.todasPiezas = Piezas.TodasPiezas()
        config_board = cpu.configuration.config_board("kib" + cpu.kibitzer.huella, 24)
        self.board = Board.Board(self, config_board)
        self.board.crea()
        self.board.set_dispatcher(self.mensajero)
        Delegados.generaPM(self.board.piezas)
        if not self.show_board:
            self.board.hide()

        self.with_figurines = cpu.configuration.x_pgn_withfigurines

    def takeback(self):
        nmoves = len(self.game)
        if nmoves:
            self.game.shrink(nmoves - 2)
            self.reset()

    def save_video(self):
        dic = {}

        pos = self.pos()
        dic["_POSICION_"] = "%d,%d" % (pos.x(), pos.y())

        tam = self.size()
        dic["_SIZE_"] = "%d,%d" % (tam.width(), tam.height())

        dic["SHOW_BOARD"] = self.show_board
        dic["NARROWS"] = self.nArrows

        dic["SITOP"] = self.siTop

        if hasattr(self, "grid"):
            self.grid.save_video(dic)

        self.cpu.save_video(dic)

    def restore_video(self, dicVideo):
        if dicVideo:
            wE, hE = QTUtil.tamEscritorio()
            x, y = dicVideo["_POSICION_"].split(",")
            x = int(x)
            y = int(y)
            if not (0 <= x <= (wE - 50)):
                x = 0
            if not (0 <= y <= (hE - 50)):
                y = 0
            self.move(x, y)
            if not ("_SIZE_" in dicVideo):
                w, h = self.width(), self.height()
                for k in dicVideo:
                    if k.startswith("_TAMA"):
                        w, h = dicVideo[k].split(",")
            else:
                w, h = dicVideo["_SIZE_"].split(",")
            w = int(w)
            h = int(h)
            if w > wE:
                w = wE
            elif w < 20:
                w = 20
            if h > hE:
                h = hE
            elif h < 20:
                h = 20
            self.resize(w, h)

    def config_board(self):
        self.show_board = not self.show_board
        self.board.setVisible(self.show_board)
        self.save_video()

    def mensajero(self, from_sq, to_sq, promocion=""):
        if not promocion and self.game.last_position.siPeonCoronando(from_sq, to_sq):
            promocion = self.board.peonCoronando(self.game.last_position.is_white)
            if promocion is None:
                promocion = "q"
        FasterCode.set_fen(self.game.last_position.fen())
        if FasterCode.make_move(from_sq + to_sq + promocion):
            self.game.read_pv(from_sq + to_sq + promocion)
            self.reset()

    def ponFlags(self):
        flags = self.windowFlags()
        if self.siTop:
            flags |= QtCore.Qt.WindowStaysOnTopHint
        else:
            flags &= ~QtCore.Qt.WindowStaysOnTopHint
        flags |= QtCore.Qt.WindowCloseButtonHint
        self.setWindowFlags(flags)
        self.tb.setAccionVisible(self.windowTop, not self.siTop)
        self.tb.setAccionVisible(self.windowBottom, self.siTop)
        self.show()

    def windowTop(self):
        self.siTop = True
        self.ponFlags()

    def windowBottom(self):
        self.siTop = False
        self.ponFlags()

    def terminar(self):
        self.finalizar()
        self.accept()

    def pause(self):
        self.siPlay = False
        self.tb.setPosVisible(1, True)
        self.tb.setPosVisible(2, False)

    def play(self):
        self.siPlay = True
        self.tb.setPosVisible(1, False)
        self.tb.setPosVisible(2, True)
        self.orden_game(self.game)

    def closeEvent(self, event):
        self.finalizar()

    def finalizar(self):
        self.save_video()

    def set_position(self):
        resp = Voyager.voyager_position(self, self.game.last_position)
        if resp is not None:
            game = Game.Game(first_position=resp)
            self.orden_game(game)

    def color(self):
        menu = QTVarios.LCMenu(self)

        def ico(ok):
            return Iconos.Aceptar() if ok else Iconos.PuntoAmarillo()

        menu.opcion("blancas", _("White"), ico(self.is_white and not self.is_black))
        menu.opcion("negras", _("Black"), ico(not self.is_white and self.is_black))
        menu.opcion("blancasnegras", "%s + %s" % (_("White"), _("Black")), ico(self.is_white and self.is_black))
        resp = menu.lanza()
        if resp:
            self.is_black = True
            self.is_white = True
            if resp == "blancas":
                self.is_black = False
            elif resp == "negras":
                self.is_white = False
            self.reset()

    def reset(self):
        self.orden_game(self.game)
