import utils.color as color
from utils.page import Page
from obj.button import Button, TextButton
from utils.define import PyGame, StateMachine

class menu(Page):
    def __init__(self, game: PyGame, state: StateMachine) -> None:
        super().__init__(game, state)

    # overload init
    def init(self):

        def home():
            self.state.state = "home"
        home_button =  TextButton(
            self.game, "return home", (self.game.size[0] - 10, self.game.size[1] - 10),
            align="right-down", font_size=30,
            color=color.Red3, bg_alpha=0,
            click_func=home
        )
        self.add_to_render_list(home_button)
        self.add_to_click_list(home_button)

        def play():
            self.state.state = "play"
        play_button =  TextButton(
            self.game, "play", (self.game.size[0] - 10, 10),
            align="right-up", font_size=30,
            color=color.Red3, bg_alpha=0,
            click_func=play
        )
        self.add_to_render_list(play_button)
        self.add_to_click_list(play_button)

    # overload controlflow
    def control_flow(self):
        pass
        self.game.screen.fill(color.white)

    # DONE! These's nothing else need to do!
