from Code import Manager
from Code.Base import Move
from Code.QT import Iconos
from Code.Base.Constantes import *


class ManagerVariations(Manager.Manager):
    def inicio(self, game, is_white_bottom, with_engine_active, is_competitive):

        self.pensando(True)

        self.kibitzers_manager = self.procesador.kibitzers_manager

        self.siAceptado = False

        self.is_competitive = is_competitive

        self.game = game

        self.game_type = GT_ALONE

        self.human_is_playing = True
        self.plays_instead_of_me_option = True
        self.dicRival = {}

        self.play_against_engine = False

        self.state = ST_PLAYING

        self.main_window.pon_toolbar((TB_ACCEPT, TB_CANCEL, TB_TAKEBACK, TB_REINIT, TB_CONFIG, TB_UTILITIES))

        self.is_human_side_white = is_white_bottom
        self.main_window.activaJuego(True, False, siAyudas=False)
        self.quitaAyudas(True, False)
        self.main_window.set_label1(None)
        self.main_window.set_label2(None)
        self.show_side_indicator(True)
        self.ponPiezasAbajo(self.is_human_side_white)
        self.set_dispatcher(self.player_has_moved)
        self.pgnRefresh(True)
        self.ponCapInfoPorDefecto()

        self.refresh()

        if len(self.game):
            self.mueveJugada(GO_START)
            move = self.game.move(0)
            self.put_arrow_sc(move.from_sq, move.to_sq)
            self.disable_all()
        else:
            self.set_position(self.game.last_position)

        self.pensando(False)

        is_white = self.game.last_position.is_white
        self.is_human_side_white = is_white
        self.human_is_playing = True

        if with_engine_active and not is_competitive:
            self.activeEngine()

        if not len(self.game):
            self.siguiente_jugada()

    def run_action(self, key):
        if key == TB_ACCEPT:
            self.siAceptado = True
            # self.resultado =
            self.procesador.pararMotores()
            self.main_window.accept()

        elif key == TB_CANCEL:
            self.procesador.pararMotores()
            self.main_window.reject()

        elif key == TB_TAKEBACK:
            self.atras()

        elif key == TB_REINIT:
            self.reiniciar()

        elif key == TB_CONFIG:
            self.configurar()

        elif key == TB_UTILITIES:
            liMasOpciones = (("libros", _("Consult a book"), Iconos.Libros()),)
            resp = self.utilidades(liMasOpciones)
            if resp == "libros":
                liMovs = self.librosConsulta(True)
                if liMovs:
                    for x in range(len(liMovs) - 1, -1, -1):
                        from_sq, to_sq, promotion = liMovs[x]
                        self.player_has_moved(from_sq, to_sq, promotion)

        else:
            Manager.Manager.rutinaAccionDef(self, key)

    def valor(self):
        if self.siAceptado:
            return self.game
        else:
            return None

    def final_x(self):
        self.procesador.pararMotores()
        return True

    def atras(self):
        if len(self.game):
            self.game.anulaSoloUltimoMovimiento()
            if not self.fen:
                self.game.assign_opening()
            self.goto_end()
            self.refresh()
            self.siguiente_jugada()

    def siguiente_jugada(self):
        if self.state == ST_ENDGAME:
            return

        self.state = ST_PLAYING

        self.put_view()

        is_white = self.game.last_position.is_white
        self.is_human_side_white = is_white
        self.human_is_playing = True

        if self.game.is_finished():
            return

        self.set_side_indicator(is_white)

        self.activate_side(is_white)
        self.refresh()

    def player_has_moved(self, from_sq, to_sq, promotion=""):
        move = self.check_human_move(from_sq, to_sq, promotion)
        if not move:
            return False
        self.move_the_pieces(move.liMovs)

        self.add_move(move)
        if self.play_against_engine:
            self.play_against_engine = False
            self.disable_all()
            self.juegaRival()
            self.play_against_engine = True  # Como juega por mi pasa por aqui, para que no se meta en un bucle infinito

        self.siguiente_jugada()
        return True

    def add_move(self, move):

        self.beepExtendido(True)

        self.changed = True

        self.game.add_move(move)

        self.put_arrow_sc(move.from_sq, move.to_sq)

        self.pgnRefresh(self.game.last_position.is_white)
        self.refresh()

    def reiniciar(self):
        self.inicio(self.fen, self.lineaPGN, self.okMasOpciones, self.is_human_side_white)

    def configurar(self):

        mt = _("Engine").lower()
        mt = _X(_("Disable %1"), mt) if self.play_against_engine else _X(_("Enable %1"), mt)

        if not self.is_competitive:
            liMasOpciones = (("engine", mt, Iconos.Motores()),)
        else:
            liMasOpciones = []

        resp = Manager.Manager.configurar(self, liMasOpciones, siCambioTutor=not self.is_competitive)

        if resp == "engine":
            self.set_label1("")
            if self.play_against_engine:
                self.xrival.terminar()
                self.xrival = None
                self.play_against_engine = False
            else:
                self.cambioRival()

    def juegaRival(self):
        if not self.is_finished():
            self.pensando(True)
            rm = self.xrival.juega(nAjustado=self.xrival.nAjustarFuerza)
            if rm.from_sq:
                ok, self.error, move = Move.get_game_move(
                    self.game, self.game.last_position, rm.from_sq, rm.to_sq, rm.promotion
                )
                self.add_move(move)
                self.move_the_pieces(move.liMovs)
            self.pensando(False)

    def activeEngine(self):
        dicBase = self.configuration.leeVariables("ENG_VARIANTES")
        if dicBase:
            self.ponRival(dicBase)
        else:
            self.cambioRival()

    def cambioRival(self):

        if self.dicRival:
            dicBase = self.dicRival
        else:
            dicBase = self.configuration.leeVariables("ENG_VARIANTES")

        import Code.PlayAgainstEngine.PlayAgainstEngine as WindowEntMaq

        dic = self.dicRival = WindowEntMaq.cambioRival(
            self.main_window, self.configuration, dicBase, siManagerSolo=True
        )

        if dic:
            self.ponRival(dic)

    def ponRival(self, dic):
        dr = dic["RIVAL"]
        rival = dr["CM"]
        r_t = dr["TIME"] * 100  # Se guarda en decimas -> milesimas
        r_p = dr["PROFUNDIDAD"]
        if r_t <= 0:
            r_t = None
        if r_p <= 0:
            r_p = None
        if r_t is None and r_p is None and not dic["SITIEMPO"]:
            r_t = 1000

        nAjustarFuerza = dic["AJUSTAR"]
        self.xrival = self.procesador.creaManagerMotor(rival, r_t, r_p, nAjustarFuerza != ADJUST_BETTER)
        self.xrival.nAjustarFuerza = nAjustarFuerza

        dic["ROTULO1"] = _("Opponent") + ": <b>" + self.xrival.name
        self.set_label1(dic["ROTULO1"])
        self.play_against_engine = True
        self.configuration.escVariables("ENG_VARIANTES", dic)
