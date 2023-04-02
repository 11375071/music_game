from typing import List
import preload.img as img
from obj.note import Note
import utils.color as color
from utils.page import Page, SubPage
from utils.define import PyGame, StateMachine
from utils.load import load_music, load_note_from_txt
from obj.button import SimpleRect, TextRect, TextButton, RichButton


class offset_guide(SubPage):

    # overload init
    def init(self):
        
        def track_to_destination(track: int):
            track = 3 - track
            return (self.game.size[0] / 2 - 100 * track + 150, self.game.size[1] / 5 * 4)

        self.offset_list = []

        self.back_layer = SimpleRect(
            self.game, (self.game.size[0], self.game.size[1]),
            (0, 0), align="left-up", image=img.play_surface
        )
        self.add_to_render_list(self.back_layer)

        def quit():
            self.game.it.mixer.music.unload()
            self.inited = False
            self.quit()
        quit_button = TextButton(
            self.game, "quit",
            (self.game.size[0] - 10, self.game.size[1] - 10),
            align="right-down", font_size=30,
            fr_color=color.Red3, bg_alpha=0,
            click_func=quit
        )
        self.add_to_render_list(quit_button)
        self.add_to_check_list(quit_button)
        
        def confirm():
            self.inited = False
            if len(self.offset_list):
                self.state["normal"]["offset"] += int(sum(self.offset_list) / len(self.offset_list))
            self.quit()
        self.confirm_button = TextButton(
            self.game, "",
            (self.game.size[0] / 2, self.game.size[1] / 2),
            align="center", font_size=35,
            fr_color=color.Red3, bg_alpha=0.4,
            click_func=confirm
        )
        self.add_to_render_list(self.confirm_button)
        self.add_to_check_list(self.confirm_button)

        self.offset_text = TextRect(
            self.game, pos=(50, 60),
            align="left-up", text="average offset: " + "%.2f"%(0),
            font_size=30, fr_color=color.Red, 
            bg_color=color.White, bg_alpha=0
        )
        self.add_to_render_list(self.offset_text)


        self.notes: List[Note] = []
        self.notes = load_note_from_txt(
            self.game,
            "src/songs/Lv.0/offset_guide/offset_guide.txt",
            track_to_destination
        )
        for note in self.notes:
            note.speed = self.state["normal"]["speed"]
            self.add_to_render_list(note)


        def key_press(destination):
            for note in self.notes:
                if note.destination != destination:
                    continue
                if note.time < 0.15:
                    self.del_from_render_list(note)
                    self.notes.remove(note)
                    note.resolved()
                    self.offset_list.append(int(note.time * 1000))
                    self.rank_text.change_text(str(int(note.time * 1000)))
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


        load_music(self.game, "src/songs/Lv.0/offset_guide/Bad Apple!! feat. nomico.ogg")


    # overload controlflow
    def control_flow(self):
        if self.game.it.mixer.music.get_pos() > 9000:
            self.game.it.mixer.music.unload()
            self.confirm_button.change_text("confirm")

        duration = self.game.it.mixer.music.get_pos() + self.state["normal"]["offset"]

        for note in self.notes:
            note.time = note.init_time - duration * 0.001
            note.appear = True
            if note.time < -0.5:
                self.del_from_render_list(note)
                self.notes.remove(note)
                note.rank("miss")

        if len(self.offset_list):
            self.offset_text.change_text("average offset: " + "%.2f"%(sum(self.offset_list) / len(self.offset_list)))

    # DONE! These's nothing else need to do!
