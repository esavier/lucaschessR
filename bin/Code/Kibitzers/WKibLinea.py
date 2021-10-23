import struct

import psutil
from PySide2 import QtCore, QtGui, QtWidgets

import Code
from Code.Base import Game
from Code.Engines import EngineRun
from Code.Kibitzers import WindowKibitzers
from Code.QT import Colocacion
from Code.QT import Controles
from Code.QT import Iconos
from Code.QT import QTUtil
from Code.QT import QTVarios


class EDP(Controles.ED):
    def ponHtml(self, txt):
        self.setText(txt)
        self.setCursorPosition(0)
        return self

    def html(self):
        return self.text()


class WKibLinea(QtWidgets.QDialog):
    siMover: bool

    def __init__(self, cpu):
        QtWidgets.QDialog.__init__(self)

        self.cpu = cpu
        self.kibitzer = cpu.kibitzer

        dicVideo = self.cpu.dic_video
        if not dicVideo:
            dicVideo = {}

        self.siTop = dicVideo.get("SITOP", True)

        self.game = None

        self.setWindowTitle(cpu.titulo)
        self.setWindowIcon(Iconos.Kibitzer())

        self.flags = {
            True: QtCore.Qt.Dialog | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowStaysOnTopHint,
            False: QtCore.Qt.Dialog | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint,
        }

        self.setWindowFlags(self.flags[False])

        self.setBackgroundRole(QtGui.QPalette.Light)

        Code.configuration = cpu.configuration

        self.setStyleSheet(
            """QLineEdit {
    color: rgb(127, 0, 63);
    selection-color: white;
    border: 1px groove gray;
    border-radius: 2px;
    padding: 2px 4px;
}"""
        )

        li_acciones = (
            (_("Quit"), Iconos.Kibitzer_Close(), self.terminar),
            (_("Continue"), Iconos.Kibitzer_Play(), self.play),
            (_("Pause"), Iconos.Kibitzer_Pause(), self.pause),
            (_("Analyze only color"), Iconos.Kibitzer_Side(), self.color),
            (_("Change window position"), Iconos.ResizeBoard(), self.mover),
            (_("Options"), Iconos.Opciones(), self.changeOptions),
        )
        self.tb = Controles.TBrutina(self, li_acciones, with_text=False, icon_size=24)
        self.tb.setFixedSize(180, 32)
        self.tb.setPosVisible(1, False)
        self.em = EDP(self)
        self.em.ponTipoLetra(peso=75, puntos=10)
        self.em.setReadOnly(True)

        layout = Colocacion.H().control(self.em).control(self.tb).margen(2)

        self.setLayout(layout)

        self.lanzaMotor()

        self.siPlay = True
        self.is_white = True
        self.is_black = True

        self.siMover = False

        self.restore_video(dicVideo)

        self.engine = self.lanzaMotor()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.compruebaInput)
        self.timer.start(200)
        self.depth = 0
        self.veces = 0

    def compruebaInput(self):
        if not self.engine:
            return
        self.veces += 1
        if self.veces == 3:
            self.veces = 0
            if self.valid_to_play():
                mrm = self.engine.ac_estado()
                rm = mrm.rmBest()
                if rm and rm.depth > self.depth:
                    self.depth = rm.depth
                    game = Game.Game(first_position=self.game.last_position)
                    game.read_pv(rm.pv)
                    if len(game):
                        self.em.ponHtml("[%02d] %s | %s" % (rm.depth, rm.abrTexto(), game.pgnBaseRAW()))
            else:
                self.em.ponHtml("")

                QTUtil.refresh_gui()

        self.cpu.compruebaInput()

    def changeOptions(self):
        self.pause()
        w = WindowKibitzers.WKibitzerLive(self, self.cpu.configuration, self.cpu.numkibitzer)
        if w.exec_():
            xprioridad = w.result_xprioridad
            if xprioridad is not None:
                pid = self.engine.pid()
                if Code.is_windows:
                    hp, ht, pid, dt = struct.unpack("PPII", pid.asstring(16))
                p = psutil.Process(pid)
                p.nice(xprioridad)
            if w.result_opciones:
                for opcion, valor in w.result_opciones:
                    if valor is None:
                        orden = "setoption name %s" % opcion
                    else:
                        if type(valor) == bool:
                            valor = str(valor).lower()
                        orden = "setoption name %s value %s" % (opcion, valor)
                    self.escribe(orden)
        self.play()

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
        self.stop()

    def play(self):
        self.siPlay = True
        self.tb.setPosVisible(1, False)
        self.tb.setPosVisible(2, True)
        self.reset()

    def stop(self):
        self.siPlay = False
        self.engine.ac_final(0)

    def lanzaMotor(self):
        self.nom_engine = self.kibitzer.name
        exe = self.kibitzer.path_exe
        args = self.kibitzer.args
        li_uci = self.kibitzer.liUCI
        self.numMultiPV = 0
        return EngineRun.RunEngine(self.nom_engine, exe, li_uci, self.numMultiPV, priority=self.cpu.prioridad, args=args)

    def closeEvent(self, event):
        self.finalizar()

    def if_to_analyze(self):
        siW = self.game.last_position.is_white
        if not self.siPlay or (siW and (not self.is_white)) or ((not siW) and (not self.is_black)):
            return False
        return True

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
            self.orden_game(self.game)

    def finalizar(self):
        self.save_video()
        if self.engine:
            self.engine.ac_final(0)
            self.engine.close()
            self.engine = None
            self.siPlay = False

    def save_video(self):
        dic = {}

        pos = self.pos()
        dic["_POSICION_"] = "%d,%d" % (pos.x(), pos.y())

        tam = self.size()
        dic["_SIZE_"] = "%d,%d" % (tam.width(), tam.height())

        dic["SITOP"] = self.siTop

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

    def orden_game(self, game: Game.Game):
        posicion = game.last_position

        self.siW = posicion.is_white

        self.escribe("stop")

        self.game = game
        self.depth = 0

        if self.valid_to_play():
            self.engine.ac_inicio(game)
        else:
            self.em.setText("")

    def valid_to_play(self):
        siw = self.game.last_position.is_white
        if not self.siPlay or (siw and not self.is_white) or (not siw and not self.is_black):
            return False
        return True

    def escribe(self, linea):
        self.engine.put_line(linea)

    def mover(self):
        w = self.width()
        self.siMover = not self.siMover
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | self.flags[self.siMover])
        self.show()
        QTUtil.refresh_gui()
        self.resize(w, self.height())

    def reset(self):
        self.orden_game(self.game)
