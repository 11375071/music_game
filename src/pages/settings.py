from pygame import event
import utils.color as color
from utils.page import Page
from obj.button import Button, TextButton
from utils.define import PyGame, StateMachine


class setting_button_group:
    def __init__(
        self, game: PyGame, font_size: int = 30, pos: tuple = (0, 0),
        text: str = "", align: str = "left-up",
        default_value: int = 5, min_value: int = 1, max_value: int = 20
    ):
        self.game = game
        self.font_size = font_size
        self.pos = pos
        self.text = text
        self.num = default_value
        self.min_value = min_value
        self.max_value = max_value

        self.text = TextButton(
            game, text, pos,
            align=align, font_size=font_size,
            color=color.Red
        )
        x, y, _x, _y = self.text.rect
        self.left_rect = (x + _x, y, _x, _y)
        self.left = Button(
            game, size=(_y, _y), pos=(x + _x + 0.5 * _y, y),
            align=align, bg_color=color.Red, image=r"src/image/left_arrow.jpg",
            click_func=self.click_left
        )
        x, y, _x, _y = self.left.rect
        self.num_text = TextButton(
            game, str(self.num), pos=(x + _x + 0.5 * _y, y),
            align=align, font_size=font_size,
            color=color.Red
        )
        x, y, _x, _y = self.num_text.rect
        self.right = Button(
            game, size=(_y, _y), pos=(x + _x + 0.5 * _y, y),
            align=align, bg_color=color.Red, image=r"src/image/right_arrow.jpg",
            click_func=self.click_right
        )

        self.button_list = [self.text, self.left, self.num_text, self.right]

    def click_left(self):
        if self.num > self.min_value:
            self.num -= 1
        self.num_text.change_text(str(self.num))

    def click_right(self):
        if self.num < self.max_value:
            self.num += 1
        self.num_text.change_text(str(self.num))

    def render(self):
        for button in self.button_list:
            button.render()

    def click_check(self, event: event.Event):
        for button in self.button_list:
            button.click_check(event)


class settings(Page):
    def __init__(self, game: PyGame, state: StateMachine) -> None:
        super().__init__(game, state)

    # overload init
    def init(self):

        def home():
            self.state.state = "home"
        self.home_button = TextButton(
            self.game, "return home", (self.game.size[0] -
                                       10, self.game.size[1] - 10),
            align="right-down", font_size=30,
            color=color.Red3, bg_alpha=0,
            click_func=home
        )
        self.add_to_render_list(self.home_button)
        self.add_to_click_list(self.home_button)

        self.speed_ctrl = setting_button_group(
            self.game, pos=(100, 100),
            text="speed: ", default_value=self.state["normal"]["speed"]
        )
        self.add_to_render_list(self.speed_ctrl)
        self.add_to_click_list(self.speed_ctrl)

        self.offset_ctrl = setting_button_group(
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
            color=color.Blue3,
            bg_alpha=0.4, bg_color=color.Yellow3,
            click_func=offset_guide
        )
        self.add_to_render_list(self.offset_guide_button)
        self.add_to_click_list(self.offset_guide_button)

        self.lv_ctrl = setting_button_group(
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
