import utils.color as color
from utils.page import Page, SubPage
from utils.define import PyGame, StateMachine
from obj.button import SimpleRect, TextButton


class play_pause(SubPage):
    def __init__(
            self, game: PyGame,
            state: StateMachine, mother_page: Page,
            need_mother_texture: bool = True
        ) -> None:
        super().__init__(game, state, mother_page, need_mother_texture)
    
    def init(self):
        def menu():
            self.game.it.mixer.music.unload()
            self.mother_page.inited = False
            self.state.state = "menu"
            self.quit()
        
        def replay():
            self.game.it.mixer.music.play()
            self.mother_page.inited = False
            self.quit()
        
        def resume():
            self.game.it.mixer.music.unpause()
            self.quit()

        back_layer = SimpleRect(
            self.game, (self.game.size[0] / 3 * 2, self.game.size[1] / 3 * 2),
            (self.game.size[0] / 2, self.game.size[1] / 2),
            align="center", alpha=0.85
        )
        self.add_to_render_list(back_layer)

        resume_button = TextButton(
            self.game, "RESUME", (self.game.size[0] / 2, self.game.size[1] / 6 * 2),
            align="center", font_size=int(min(*self.game.size) / 15),
            fr_color=color.Blue2, bg_alpha=0,
            click_func=resume, key=self.game.it.K_SPACE
        )
        self.add_to_render_list(resume_button)
        self.add_to_check_list(resume_button)

        replay_button = TextButton(
            self.game, "REPLAY", (self.game.size[0] / 2, self.game.size[1] / 6 * 3),
            align="center", font_size=int(min(*self.game.size) / 15),
            fr_color=color.Blue2, bg_alpha=0,
            click_func=replay
        )
        self.add_to_render_list(replay_button)
        self.add_to_check_list(replay_button)

        menu_button = TextButton(
            self.game, "RETURN MENU", (self.game.size[0] / 2, self.game.size[1] / 6 * 4),
            align="center", font_size=int(min(*self.game.size) / 15),
            fr_color=color.Blue2, bg_alpha=0,
            click_func=menu
        )
        self.add_to_render_list(menu_button)
        self.add_to_check_list(menu_button)
