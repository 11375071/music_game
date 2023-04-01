import random
import preload.songs as songs
import utils.color as color
from utils.page import Page
from obj.band import ScrollArea
from obj.button import TextButton, TextRect, MultipleTextButton
from utils.define import PyGame, StateMachine


class menu(Page):
    def __init__(self, game: PyGame, state: StateMachine) -> None:
        super().__init__(game, state)

    # overload init
    def init(self):

        def choose_song(song: songs.Song):
            # print(song.song_name)
            self.state.song = song
            self.state.state = "play"
        menu_scroll_area = ScrollArea(
            self.game, (600, 500), (0, 0), align = "left-up"
        )
        for i in songs.song_list:
            a = MultipleTextButton(
                self.game, (600, 250), (0, 0), align = "center",
                color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)),
                # if not add a lambda scope, all function will be the same as the last function
                click_func = (lambda what: lambda: choose_song(what))(i)
            )
            a_text = TextRect(
                self.game, i.string, (300, 125),
                font_size = 50,
                fr_color = color.Black, bg_alpha = 0
            )
            a.append_text(a_text)
            menu_scroll_area.append_choice(a)
        self.add_to_render_list(menu_scroll_area)
        self.add_to_click_list(menu_scroll_area)


        def home():
            self.state.state = "home"
        home_button = TextButton(
            self.game, "return home",
            (self.game.size[0] - 10, self.game.size[1] - 10),
            align="right-down", font_size=30,
            fr_color=color.Red3, bg_alpha=0,
            click_func=home
        )
        self.add_to_render_list(home_button)
        self.add_to_click_list(home_button)


        def play():
            if self.state.song is None:
                return
            self.state.state = "play"
        play_button = TextButton(
            self.game, "play last choosen",
            (self.game.size[0] - 10, 10),
            align="right-up", font_size=30,
            fr_color=color.Red3, bg_alpha=0,
            click_func=play
        )
        self.add_to_render_list(play_button)
        self.add_to_click_list(play_button)


    # overload controlflow
    def control_flow(self):
        pass
        self.game.screen.fill(color.white)

    # DONE! These's nothing else need to do!
