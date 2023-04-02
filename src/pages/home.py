import preload.img as img
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
            (0, 0), "left-up", image = img.homepage_surface,
        )
        self.add_to_render_list(self.background)


        def menu():
            self.play_button.now_press_state = "default"
            self.state.state = "menu"
        play_origin = SimpleRect(
            self.game, (self.game.size[0], self.game.size[1]),
            (0, 0), "left-up", image = img.homepage_play_button_tuple_1,
            collide_ignore_transparent = True,
        )
        play_selected = SimpleRect(
            self.game, (self.game.size[0], self.game.size[1]),
            (0, 0), "left-up", image = img.homepage_play_button_tuple_2,
            collide_ignore_transparent = True,
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
            self.setting_button.now_press_state = "default"
            self.state.state = "settings"
        setting_origin = SimpleRect(
            self.game, (self.game.size[0], self.game.size[1]),
            (0, 0), "left-up", image = img.homepage_settings_button_tuple_1,
            collide_ignore_transparent = True,
        )
        setting_selected = SimpleRect(
            self.game, (self.game.size[0], self.game.size[1]),
            (0, 0), "left-up", image = img.homepage_settings_button_tuple_2,
            collide_ignore_transparent = True,
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
