import utils.color as color
from utils.page import Page
from pages.offset_guide import offset_guide
from utils.define import PyGame, StateMachine
from obj.button import ButtonAjustGroup, TextButton



class settings(Page):

    # overload init
    def init(self):

        def home():
            self.inited = False
            self.state.state = "home"
        self.home_button = TextButton(
            self.game, "return home",
            (self.game.size[0] - 10, self.game.size[1] - 10),
            align="right-down", font_size=30,
            fr_color=color.Red3, bg_alpha=0,
            click_func=home
        )
        self.add_to_render_list(self.home_button)
        self.add_to_check_list(self.home_button)


        def get_speed():
            self.state["normal"]["speed"] = self.speed_ctrl.num
        self.speed_ctrl = ButtonAjustGroup(
            self.game, pos=(100, 100),
            text="speed: ", default_value=self.state["normal"]["speed"],
            click_func=get_speed
        )
        self.add_to_render_list(self.speed_ctrl)
        self.add_to_check_list(self.speed_ctrl)


        def get_offset():
            self.state["normal"]["offset"] = self.offset_ctrl.num
        self.offset_ctrl = ButtonAjustGroup(
            self.game, pos=(100, 200),
            text="offset: ", default_value=self.state["normal"]["offset"],
            min_value=-1000, max_value=1000,
            click_func=get_offset
        )
        self.add_to_render_list(self.offset_ctrl)
        self.add_to_check_list(self.offset_ctrl)


        offset_guide_page = offset_guide(self.game, self.state, self, fps = 120)
        def offset_guide_func():
            self.inited = False
            offset_guide_page.enter()
        self.offset_guide_button = TextButton(
            self.game, "offset guide", pos=(100, 250),
            align="left-up", font_size=30,
            fr_color=color.Blue3,
            bg_alpha=0.4, bg_color=color.Yellow3,
            click_func=offset_guide_func
        )
        self.add_to_render_list(self.offset_guide_button)
        self.add_to_check_list(self.offset_guide_button)


        def get_TBD():
            self.state["normal"]["TBD"] = self.TBD_ctrl.num
        self.TBD_ctrl = ButtonAjustGroup(
            self.game, pos=(100, 350),
            text="TBD: ", default_value=self.state["normal"]["TBD"],
            min_value=-1000, max_value=1000,
            click_func=get_TBD
        )
        self.add_to_render_list(self.TBD_ctrl)
        self.add_to_check_list(self.TBD_ctrl)


    # overload controlflow
    def control_flow(self):
        self.game.screen.fill(color.white)


    # DONE! These's nothing else need to do!
