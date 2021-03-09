import os

from PySide2.QtCore import Qt

from Code import Manager
from Code import FNSLine
from Code.Base import Game, Move
from Code.QT import WCompetitionWithTutor
from Code.QT import Iconos
from Code.QT import QTUtil
from Code.QT import QTUtil2
from Code import TrListas
from Code import Tutor
from Code import Util
from Code.SQL import UtilSQL
import Code
from Code.Base.Constantes import *


class ManagerEntPos(Manager.Manager):
    line_fns: FNSLine.FNSLine
    pos_obj: int
    game_obj: Game.Game

    def set_training(self, entreno):
        # Guarda el ultimo entrenamiento en el db de entrenos
        self.entreno = entreno

    def save_pos(self, pos_training):
        db = UtilSQL.DictSQL(self.configuration.ficheroTrainings)
        data = db[self.entreno]
        if data is None:
            data = {}
        data["POSULTIMO"] = pos_training
        db[self.entreno] = data
        db.close()

    def start(self, pos_training, num_trainings, title_training, li_trainings, is_tutor_enabled=None, is_automatic_jump=False):
        if hasattr(self, "reiniciando"):
            if self.reiniciando:
                return
        self.reiniciando = True

        if is_tutor_enabled is None:
            is_tutor_enabled = (Code.dgtDispatch is None) and self.configuration.x_default_tutor_active

        self.pos_training = pos_training
        self.save_pos(pos_training)
        self.num_trainings = num_trainings
        self.title_training = title_training
        self.li_trainings = li_trainings
        self.is_automatic_jump = is_automatic_jump

        self.li_histo = [self.pos_training]

        self.hints = 99999

        self.line_fns = FNSLine.FNSLine(self.li_trainings[self.pos_training - 1])

        self.game_obj = self.line_fns.game_obj
        self.pos_obj = 0

        self.is_rival_thinking = False

        cp = self.line_fns.position

        is_white = cp.is_white

        if self.line_fns.with_game_original():
            self.game = self.line_fns.game_original
        else:
            self.game.set_position(cp)
            if self.game_obj:
                self.game.set_first_comment(self.game_obj.first_comment, True)

        self.game.pending_opening = False

        self.game_type = GT_POSITIONS

        self.human_is_playing = False
        self.state = ST_PLAYING
        self.plays_instead_of_me_option = True

        self.human_side = is_white
        self.is_engine_side_white = not is_white

        self.rm_rival = None

        self.is_tutor_enabled = is_tutor_enabled
        self.main_window.set_activate_tutor(self.is_tutor_enabled)

        self.ayudas_iniciales = 0

        li_options = [TB_CLOSE, TB_CHANGE, TB_REINIT, TB_TAKEBACK]
        li_options.append(TB_PGN_LABELS)
        li_options.extend((TB_CONFIG, TB_UTILITIES))
        if self.num_trainings > 1:
            li_options.extend((TB_PREVIOUS, TB_NEXT))
        self.li_options_toolbar = li_options
        self.main_window.pon_toolbar(li_options)

        self.main_window.activaJuego(True, False, siAyudas=False)
        self.main_window.remove_hints(False, False)
        self.set_dispatcher(self.player_has_moved)
        self.set_position(self.game.last_position)
        self.show_side_indicator(True)
        self.put_pieces_bottom(is_white)
        titulo = "<b>%s</b>" % TrListas.dicTraining().get(self.title_training, self.title_training)
        if self.line_fns.label:
            titulo += "<br>%s" % self.line_fns.label
        self.set_label1(titulo)
        self.set_label2("%d / %d" % (pos_training, num_trainings))
        self.pgnRefresh(True)
        QTUtil.refresh_gui()

        if self.xrival is None:
            self.xrival = self.procesador.creaManagerMotor(self.configuration.tutor, self.configuration.x_tutor_mstime, self.configuration.x_tutor_depth)

        player = self.configuration.nom_player()
        other = _("the engine")
        w, b = (player, other) if self.human_side else (other, player)
        self.game.set_tag("White", w)
        self.game.set_tag("Black", b)

        self.is_analyzed_by_tutor = False
        self.continueTt = not self.configuration.x_engine_notbackground

        self.check_boards_setposition()

        if self.line_fns.with_game_original():
            self.repiteUltimaJugada()

        self.reiniciando = False
        self.is_rival_thinking = False
        self.play_next_move()

    def run_action(self, key):
        if key == TB_CLOSE:
            self.end_game()

        elif key == TB_TAKEBACK:
            self.atras()

        elif key == TB_REINIT:
            self.reiniciar()

        elif key == TB_CONFIG:
            self.configurar(siSonidos=True, siCambioTutor=True)

        elif key == TB_CHANGE:
            self.ent_otro()

        elif key == TB_UTILITIES:
            if "/Tactics/" in self.entreno:
                liMasOpciones = []
            else:
                liMasOpciones = [("tactics", _("Create tactics training"), Iconos.Tacticas()), (None, None, None)]

            resp = self.utilidades(liMasOpciones)
            if resp == "tactics":
                self.create_tactics()

        elif key == TB_PGN_LABELS:
            self.pgnInformacionMenu()

        elif key in (TB_NEXT, TB_PREVIOUS):
            self.ent_siguiente(key)

        elif key == TB_CONTINUE:
            self.sigue()

        elif key in self.procesador.li_opciones_inicio:
            self.procesador.run_action(key)

        else:
            Manager.Manager.rutinaAccionDef(self, key)

    def reiniciar(self):
        if self.is_rival_thinking:
            self.xrival.stop()
        if self.is_analyzing:
            self.xtutor.stop()
        self.start(self.pos_training, self.num_trainings, self.title_training, self.li_trainings, self.is_tutor_enabled, self.is_automatic_jump)

    def ent_siguiente(self, tipo):
        if not (self.human_is_playing or self.state == ST_ENDGAME):
            return
        pos = self.pos_training + (+1 if tipo == TB_NEXT else -1)
        if pos > self.num_trainings:
            pos = 1
        elif pos == 0:
            pos = self.num_trainings
        self.start(pos, self.num_trainings, self.title_training, self.li_trainings, self.is_tutor_enabled, self.is_automatic_jump)

    def control_teclado(self, nkey):
        if nkey in (Qt.Key_Plus, Qt.Key_PageDown):
            self.ent_siguiente(TB_NEXT)
        elif nkey in (Qt.Key_Minus, Qt.Key_PageUp):
            self.ent_siguiente(TB_PREVIOUS)
        elif nkey == ord("T"):
            li = self.line_fns.line.split("|")
            li[2] = self.game.pgnBaseRAW()
            self.saveSelectedPosition("|".join(li))

    def listHelpTeclado(self):
        return [("+/%s" % _("Page Down"), _("Next position")), ("-/%s" % _("Page Up"), _("Previous position")), ("T", _("Save position in 'Selected positions' file"))]

    def end_game(self):
        self.procesador.start()

    def final_x(self):
        self.end_game()
        return False

    def atras(self):
        if self.is_rival_thinking:
            return
        if len(self.game):
            self.game.anulaUltimoMovimiento(self.human_side)
            self.goto_end()
            self.is_analyzed_by_tutor = False
            self.state = ST_PLAYING
            self.refresh()
            self.play_next_move()

    def play_next_move(self):
        if self.state == ST_ENDGAME:
            if self.game_obj and self.is_automatic_jump:
                self.ent_siguiente(TB_NEXT)
            return

        self.state = ST_PLAYING

        self.human_is_playing = False
        self.put_view()

        is_white = self.game.last_position.is_white

        if self.game.is_finished():
            self.pon_resultado()
            return

        self.set_side_indicator(is_white)
        self.refresh()

        siRival = is_white == self.is_engine_side_white

        if siRival:

            self.piensa_rival()

        else:

            self.piensa_humano(is_white)

    def piensa_humano(self, is_white):
        if self.game_obj and self.pos_obj == len(self.game_obj):
            self.lineaTerminadaOpciones()
            return

        self.human_is_playing = True
        self.activate_side(is_white)
        self.analizaInicio()

    def piensa_rival(self):
        self.human_is_playing = False
        self.is_rival_thinking = True
        self.disable_all()

        if self.is_playing_gameobj():
            if self.game_obj and self.pos_obj == len(self.game_obj):
                self.is_rival_thinking = False
                self.lineaTerminadaOpciones()
                return
            move = self.game_obj.move(self.pos_obj)
            self.pos_obj += 1
            from_sq, to_sq, promotion = move.from_sq, move.to_sq, move.promotion

        else:
            self.thinking(True)
            self.rm_rival = self.xrival.juega()
            self.thinking(False)
            from_sq, to_sq, promotion = (self.rm_rival.from_sq, self.rm_rival.to_sq, self.rm_rival.promotion)

        self.is_rival_thinking = False
        ok, mens, move = Move.get_game_move(self.game, self.game.last_position, from_sq, to_sq, promotion)
        self.is_analyzed_by_tutor = False
        is_obj = self.is_playing_gameobj()

        self.move_the_pieces(move.liMovs, True)
        self.add_move(move, False)

        if is_obj:
            self.lineaTerminadaOpciones()
        self.play_next_move()

    def analizaInicio(self):
        if not self.is_tutor_enabled:
            return

        self.is_analyzing = False
        self.is_analyzed_by_tutor = False
        if self.continueTt:
            if not self.is_finished():
                self.xtutor.ac_inicio(self.game)
                self.is_analyzing = True
        else:
            mrm = self.analizaTutor()
            self.is_analyzed_by_tutor = True

    def analizaFinal(self, is_mate=False):
        if not self.is_tutor_enabled:
            if self.is_analyzing:
                self.xtutor.stop()
            return
        if is_mate:
            if self.is_analyzing:
                self.xtutor.stop()
            return
        if not self.is_tutor_enabled:
            if self.is_analyzing:
                self.xtutor.stop()
            return
        estado = self.is_analyzing
        self.is_analyzing = False
        if self.is_analyzed_by_tutor:
            return
        if self.continueTt and estado:
            self.main_window.pensando_tutor(True)
            self.mrmTutor = self.xtutor.ac_final(self.xtutor.motorTiempoJugada)
            self.main_window.pensando_tutor(False)
        else:
            self.mrmTutor = self.analizaTutor()
        self.is_analyzed_by_tutor = True

    def sigue(self):
        self.state = ST_PLAYING
        if TB_CONTINUE in self.li_options_toolbar:
            del self.li_options_toolbar[self.li_options_toolbar.index(TB_CONTINUE)]
            self.main_window.pon_toolbar(self.li_options_toolbar)
        self.play_next_move()

    def lineaTerminadaOpciones(self):
        self.state = ST_ENDGAME
        if self.is_automatic_jump:
            self.ent_siguiente(TB_NEXT)
            return False
        else:
            QTUtil2.mensajeTemporal(self.main_window, _("This line training is completed."), 0.9, fixedSize=None)
            if not self.is_finished():
                if not (TB_CONTINUE in self.li_options_toolbar):
                    self.li_options_toolbar.insert(4, TB_CONTINUE)
                    self.main_window.pon_toolbar(self.li_options_toolbar)
            return False

    def is_playing_gameobj(self):
        if self.game_obj:
            move = self.game_obj.move(self.pos_obj)
            return move.position_before == self.game.last_position
        return False

    def player_has_moved(self, from_sq, to_sq, promotion=""):
        move = self.check_human_move(from_sq, to_sq, promotion)
        if not move:
            return False

        a1h8 = move.movimiento()
        ok = False
        if self.is_playing_gameobj():
            move_obj = self.game_obj.move(self.pos_obj)
            is_main, is_var = move_obj.test_a1h8(a1h8)
            if is_main:
                ok = True
                self.pos_obj += 1
            elif is_var:
                li_movs = [(move_obj.from_sq, move_obj.to_sq, True)]
                for a1h8_m in move.variations.list_movimientos():
                    li_movs.append((a1h8_m[:2], a1h8[2:4], False))
                self.board.ponFlechasTmp(li_movs)
            else:
                if a1h8[:2] != move_obj.from_sq:
                    self.board.markPosition(move_obj.from_sq)
                else:
                    self.board.ponFlechasTmp(([move_obj.from_sq, move_obj.to_sq, True],))
            if not ok:
                self.sigueHumano()
                return False

        if not ok:
            is_mate = move.is_mate
            self.analizaFinal(is_mate)  # tiene que acabar siempre
            if self.is_tutor_enabled:
                if not self.is_analyzed_by_tutor:
                    self.analizaTutor(True)
                if self.mrmTutor.mejorMovQue(a1h8):
                    if not move.is_mate:
                        tutor = Tutor.Tutor(self, move, from_sq, to_sq, False)

                        if tutor.elegir(True):
                            self.set_piece_again(from_sq)
                            from_sq = tutor.from_sq
                            to_sq = tutor.to_sq
                            promotion = tutor.promotion
                            si_bien, mens, move_tutor = Move.get_game_move(self.game, self.game.last_position, from_sq, to_sq, promotion)
                            if si_bien:
                                move = move_tutor

                        del tutor
            self.mrmTutor = None

        self.move_the_pieces(move.liMovs)
        self.add_move(move, True)

        if self.game_obj and self.pos_obj >= len(self.game_obj):
            self.lineaTerminadaOpciones()

        self.play_next_move()
        return True

    def add_move(self, move, siNuestra):
        self.game.add_move(move)

        self.put_arrow_sc(move.from_sq, move.to_sq)
        self.beepExtendido(siNuestra)

        self.pgnRefresh(self.game.last_position.is_white)
        self.refresh()

        self.check_boards_setposition()

    def pon_resultado(self):
        mensaje, beep, player_win = self.game.label_resultado_player(self.human_side)

        QTUtil.refresh_gui()
        QTUtil2.message(self.main_window, mensaje)

        self.state = ST_ENDGAME
        self.disable_all()
        self.human_is_playing = False
        self.disable_all()
        self.refresh()

    def ent_otro(self):
        pos = WCompetitionWithTutor.edit_training_position(self.main_window, self.title_training, self.num_trainings, pos=self.pos_training)
        if pos is not None:
            self.pos_training = pos
            self.reiniciar()

    def create_tactics(self):
        name_tactic = os.path.basename(self.entreno)[:-4]

        nom_dir = os.path.join(self.configuration.folder_tactics(), name_tactic)
        if os.path.isdir(nom_dir):
            nom = nom_dir + "-%d"
            n = 1
            while os.path.isdir(nom % n):
                n += 1
            nom_dir = nom % n
        nom_ini = os.path.join(nom_dir, "Config.ini")
        nom_tactic = "TACTIC1"
        nom_dir_tac = self.configuration.folder_tactics()
        Util.create_folder(nom_dir)
        nom_fns = os.path.join(nom_dir, "Puzzles.fns")

        # Se leen todos los fens
        with open(self.entreno, "rt", errors="ignore") as f:
            liBase = [linea.strip() for linea in f if linea.strip()]

        # Se crea el file con los puzzles
        nregs = len(liBase)
        tmpBP = QTUtil2.BarraProgreso(self.main_window, name_tactic, _("Working..."), nregs)
        tmpBP.mostrar()
        with open(nom_fns, "wt", encoding="utf-8", errors="ignore") as q:
            for n in range(nregs):

                if tmpBP.is_canceled():
                    break

                tmpBP.pon(n + 1)

                linea = liBase[n]
                li = linea.split("|")
                fen = li[0]
                if len(li) < 3 or not li[2]:
                    # tutor a trabajar
                    mrm = self.xrival.analiza(fen)
                    if not mrm.li_rm:
                        continue
                    rm = mrm.li_rm[0]
                    p = Game.Game(fen=fen)
                    p.read_pv(rm.pv)
                    pts = rm.centipawns_abs()
                    move = p.move(0)
                    for pos, rm1 in enumerate(mrm.li_rm):
                        if pos:
                            if rm1.centipawns_abs() == pts:
                                p1 = Game.Game(fen=fen)
                                p1.read_pv(rm1.pv)
                                move.add_variation(p1)
                            else:
                                break

                    num_moves = p.pgnBaseRAW()
                    txt = fen + "||%s\n" % num_moves
                else:
                    txt = linea

                q.write(txt + "\n")

        tmpBP.cerrar()

        # Se crea el file de control
        dicIni = {}
        dicIni[nom_tactic] = d = {}
        d["MENU"] = name_tactic
        d["FILESW"] = "%s:100" % os.path.basename(nom_fns)

        nom_dir = Util.relative_path(os.path.realpath(nom_dir))

        Util.dic2ini(nom_ini, dicIni)

        name = os.path.basename(nom_dir)

        QTUtil2.message(
            self.main_window, _("Tactic training %s created.") % nom_dir, explanation=_X(_("You can access this training from menu Train - Learn tactics by repetition - %1"), name)
        )

        self.procesador.entrenamientos.rehaz()
