from utils.page import Page
from obj.button import SimpleRect, RichButton
from utils.define import PyGame, StateMachine


class home(Page):
    def __init__(self, game: PyGame, state: StateMachine) -> None:
        super().__init__(game, state)


    # overload init
    def init(self):
        

        self.background = SimpleRect(
            self.game, (self.game.size[0], self.game.size[1]),
            (0, 0), "left-up", image = "src/image/home_page.png"
        )
        self.add_to_render_list(self.background)


        def menu():
            self.play_button.now_visible = "default"
            self.state.state = "menu"
        play_origin = SimpleRect(
            self.game, (self.game.size[0], self.game.size[1]),
            (0, 0), "left-up", image = "src/image/play_origin.png",
            strip_alpha = True,
        )
        play_selected = SimpleRect(
            self.game, (self.game.size[0], self.game.size[1]),
            (0, 0), "left-up", image = "src/image/play_selected.png",
            strip_alpha = True,
        )
        self.play_button = RichButton(
            self.game,
            play_origin, play_selected, None,
            collide_using_target = "default",
            click_func = menu,
            key = self.game.it.K_RETURN
        )
        self.add_to_render_list(self.play_button)
        self.add_to_click_list(self.play_button)


        def settings():
            self.setting_button.now_visible = "default"
            self.state.state = "settings"
        setting_origin = SimpleRect(
            self.game, (self.game.size[0], self.game.size[1]),
            (0, 0), "left-up", image = "src/image/setting_origin.png",
            strip_alpha = True,
        )
        setting_selected = SimpleRect(
            self.game, (self.game.size[0], self.game.size[1]),
            (0, 0), "left-up", image = "src/image/setting_selected.png",
            strip_alpha = True,
        )
        self.setting_button = RichButton(
            self.game,
            setting_origin, setting_selected, None,
            collide_using_target = "default",
            click_func = settings,
        )
        self.add_to_render_list(self.setting_button)
        self.add_to_click_list(self.setting_button)


    # overload controlflow
    def control_flow(self):
        pass


    # DONE! These's nothing else need to do!
