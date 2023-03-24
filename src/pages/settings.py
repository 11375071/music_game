from pygame import event
from utils.define import PyGame, StateMachine
import utils.color as color
from obj.button import Button, TextButton

class setting_button_group:
    def __init__(self, game:PyGame, font_size: int = 30, pos: tuple = (0, 0), 
                 text: str = "", align: str = "left-up", 
                 default_value:int = 5, min_value: int = 1, max_value: int = 20):
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

home_button: TextButton = None
settings_inited: bool = False
speed_ctrl: setting_button_group = None
offset_ctrl: setting_button_group = None
offset_guide_button: Button = None
lv_ctrl: setting_button_group = None

def settings_init(game: PyGame, state: StateMachine):

    def home():
        state.state = "home"

    def offset_guide():
        global settings_inited
        settings_inited = False
        state.state = "offset_guide"

    global home_button, settings_inited, speed_ctrl, offset_ctrl, offset_guide_button, lv_ctrl
    home_button = TextButton(
        game, "return home", (game.size[0] - 10, game.size[1] - 10),
        align="right-down", font_size=30,
        color=color.Red3, bg_alpha=0,
        click_func=home
    )
    speed_ctrl = setting_button_group(
        game, pos=(100, 100),
        text="speed: ", default_value=state["normal"]["speed"]
    )
    offset_ctrl = setting_button_group(
        game, pos=(100, 200),
        text="offset: ", default_value=state["normal"]["offset"], 
        min_value=-1000, max_value=1000
    )
    offset_guide_button = TextButton(
        game, "offset guide", pos=(100, 250),
        align="left-up", font_size=30,
        color=color.Blue3, 
        bg_alpha=0.4, bg_color=color.Yellow3,
        click_func=offset_guide
    )
    lv_ctrl = setting_button_group(game, pos=(100, 350),
                                      text="song lv: ", default_value=state["normal"]["level"], 
                                      min_value=1, max_value=6)

    settings_inited = True


def settings(game: PyGame, state: StateMachine):

    if not settings_inited:
        settings_init(game, state)

    # input
    for event in game.it.event.get():
        if event.type == game.it.QUIT:
            state.quit = True
        home_button.click_check(event)
        speed_ctrl.click_check(event)
        offset_ctrl.click_check(event)
        offset_guide_button.click_check(event)
        lv_ctrl.click_check(event)

    # control flow and calculate here
    state["normal"]["speed"] = speed_ctrl.num
    state["normal"]["offset"] = offset_ctrl.num
    state["normal"]["level"] = lv_ctrl.num

    # render
    game.screen.fill(color.white)
    home_button.render()
    speed_ctrl.render()
    offset_ctrl.render()
    offset_guide_button.render()
    lv_ctrl.render()

    game.render_update()
    game.clock.tick(60)
