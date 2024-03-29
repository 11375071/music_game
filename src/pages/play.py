from typing import List
import preload.img as img
from obj.note import Note
import utils.color as color
from utils.page import Page
from pages.play_pause import play_pause
from utils.define import PyGame, StateMachine
from utils.load import load_music, load_note
from obj.button import SimpleRect, SimpleButton, TextRect, TextButton, RichButton


class play(Page):

    # overload init
    def init(self):
        
        self.score = 0
        self.max_score = 0

        def track_to_destination(track: int):
            track = 3 - track
            return (self.game.size[0] / 2 - 100 * track + 150, self.game.size[1] / 5 * 4)


        self.back_layer = SimpleRect(
            self.game, (self.game.size[0], self.game.size[1]),
            (0, 0), align="left-up", image=img.play_surface
        )
        self.add_to_render_list(self.back_layer)


        self.notes: List[Note] = []
        self.resolved_notes: List[Note] = []
        self.notes = load_note(
            self.game,
            self.state.song.note_path,
            track_to_destination
        )
        for note in self.notes:
            note.speed = self.state["normal"]["speed"]
            self.add_to_render_list(note)


        self.pause_page = play_pause(self.game, self.state, self, True)
        def pause():
            self.game.it.mixer.music.pause()
            self.pause_page.enter()
        self.pause_button = TextButton(
            self.game, "PAUSE", (self.game.size[0] - 10, 10),
            align="right-up", font_size=int(min(*self.game.size) / 20),
            fr_color=color.WhiteSmoke, bg_alpha=0,
            click_func=pause, key=self.game.it.K_SPACE,
            activate_on_keydown=True
        )
        self.add_to_render_list(self.pause_button)
        self.add_to_check_list(self.pause_button)
        self.pause_page.del_from_mother_visible(self.pause_button)


        def key_press(destination):
            for note in self.notes:
                if note.destination != destination:
                    continue
                if abs(note.time) < 0.044:
                    self.notes.remove(note)
                    self.del_from_render_list(note)
                    self.resolved_notes.append(note)
                    note.rank("perfect")
                    self.rank_text.change_text("perfect")
                    self.score += note.score
                    self.max_score += note.max_score
                    return
                elif abs(note.time) < 0.084:
                    self.notes.remove(note)
                    self.del_from_render_list(note)
                    self.resolved_notes.append(note)
                    note.rank("great")
                    self.rank_text.change_text("great")
                    self.score += note.score
                    self.max_score += note.max_score
                    return
                elif abs(note.time) < 0.118:
                    self.notes.remove(note)
                    self.del_from_render_list(note)
                    self.resolved_notes.append(note)
                    note.rank("good")
                    self.rank_text.change_text("good")
                    self.score += note.score
                    self.max_score += note.max_score
                    return
                elif note.time < 0.15:
                    self.notes.remove(note)
                    self.del_from_render_list(note)
                    self.resolved_notes.append(note)
                    note.rank("miss")
                    self.rank_text.change_text("miss")
                    self.score += note.score
                    self.max_score += note.max_score
                    return
                else:
                    return

        key_list = [self.game.it.K_z, self.game.it.K_x, self.game.it.K_PERIOD, self.game.it.K_SLASH]
        key_list_text = ['z', 'x', '.', '/']
        for i in range(4):
            play_button_d = SimpleRect(
                self.game, size=(50, 10), pos=track_to_destination(i),
                align="center",
                color=color.IndianRed1,
            )
            play_button_h = SimpleRect(
                self.game, size=(50, 10), pos=track_to_destination(i),
                align="center",
                color=color.Green3,
            )
            play_button = RichButton(
                self.game,
                play_button_d, play_button_h, None,
                # if not add a lambda scope, all function will be the same as the last function
                click_func=(lambda x: lambda: key_press(track_to_destination(x)))(i),
                key=key_list[i], only_use_key=True, activate_on_keydown=True,
            )
            self.add_to_check_list(play_button)
            self.add_to_render_list(play_button)

        for i in range(4):
            play_text = TextRect(
                self.game, pos=track_to_destination(i),
                align="center", font_size=15,
                text=key_list_text[i],
                fr_alpha=1, fr_color=color.White,
            )
            self.add_to_render_list(play_text)
        

        self.rank_text = TextRect(
            self.game, pos=(self.game.size[0] / 2, self.game.size[1] / 3 * 2 + 30),
            align="center", text="",
            font_size=30, fr_color=color.Red, 
            bg_color=color.White, bg_alpha=0,
        )
        self.add_to_render_list(self.rank_text)


        self.score_text = TextRect(
            self.game, pos=(50, 60),
            align="left-up", text="",
            font_size=30, fr_color=color.Red, 
            bg_color=color.White, bg_alpha=0,
        )
        self.add_to_render_list(self.score_text)


        self.percentage_text = TextRect(
            self.game, pos=(50, 100),
            align="left-up", text="",
            font_size=30, fr_color=color.Red, 
            bg_color=color.White, bg_alpha=0,
        )
        self.add_to_render_list(self.percentage_text)


        load_music(self.game, self.state.song.song_path)


    # overload controlflow
    def control_flow(self):
        self.duration = self.game.it.mixer.music.get_pos() + self.state["normal"]["offset"]

        for note in self.notes:
            note.time = note.init_time - self.duration * 0.001
            note.appear = True
            if note.time < -0.3:
                self.notes.remove(note)
                self.del_from_render_list(note)
                self.resolved_notes.append(note)
                note.rank("miss")
                self.rank_text.change_text("miss")
                self.score += note.score
                self.max_score += note.max_score
            # no more
            if note.time >= 5:
                break

        if self.max_score == 0:
            pct = 0
        else:
            pct = self.score / self.max_score
        
        self.score_text.change_text("score: " + str(self.score))
        self.percentage_text.change_text("acc: " + "%.2f"%(pct * 100) + "%")

    # DONE! These's nothing else need to do!
