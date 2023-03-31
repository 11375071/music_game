from pygame import event
import utils.color as color
from utils.page import Page
from obj.button import ButtonGroup, TextButton
from utils.define import PyGame, StateMachine


class settings(Page):
    def __init__(self, game: PyGame, state: StateMachine) -> None:
        super().__init__(game, state)


    # overload init
    def init(self):

        def home():
            self.state.state = "home"
        self.home_button = TextButton(
            self.game, "return home",
            (self.game.size[0] - 10, self.game.size[1] - 10),
            align="right-down", font_size=30,
            fr_color=color.Red3, bg_alpha=0,
            click_func=home
        )
        self.add_to_render_list(self.home_button)
        self.add_to_click_list(self.home_button)


        self.speed_ctrl = ButtonGroup(
            self.game, pos=(100, 100),
            text="speed: ", default_value=self.state["normal"]["speed"]
        )
        self.add_to_render_list(self.speed_ctrl)
        self.add_to_click_list(self.speed_ctrl)


        self.offset_ctrl = ButtonGroup(
            self.game, pos=(100, 200),
            text="offset: ", default_value=self.state["normal"]["offset"],
            min_value=-1000, max_value=1000
        )
        self.add_to_render_list(self.offset_ctrl)
        self.add_to_click_list(self.offset_ctrl)


        def offset_guide():
            # self.__inited = False
            self.state.state = "offset_guide"
        self.offset_guide_button = TextButton(
            self.game, "offset guide", pos=(100, 250),
            align="left-up", font_size=30,
            fr_color=color.Blue3,
            bg_alpha=0.4, bg_color=color.Yellow3,
            click_func=offset_guide
        )
        self.add_to_render_list(self.offset_guide_button)
        self.add_to_click_list(self.offset_guide_button)


        self.lv_ctrl = ButtonGroup(
            self.game, pos=(100, 350),
            text="song lv: ", default_value=self.state["normal"]["level"],
            min_value=1, max_value=6
        )
        self.add_to_render_list(self.lv_ctrl)
        self.add_to_click_list(self.lv_ctrl)


    # overload controlflow
    def control_flow(self):
        self.state["normal"]["speed"] = self.speed_ctrl.num
        self.state["normal"]["offset"] = self.offset_ctrl.num
        self.state["normal"]["level"] = self.lv_ctrl.num
        self.game.screen.fill(color.white)


    # DONE! These's nothing else need to do!
