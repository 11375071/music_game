from utils.define import PyGame, StateMachine
import utils.color as color
from obj.button import TextButton

home_button: TextButton = None
settings_inited: bool = False


def settings_init(game: PyGame, state: StateMachine):

    def home():
        state.state = "home"

    global home_button, settings_inited
    home_button = TextButton(
        game, "RETURN HOME", (game.size[0] - 10, game.size[1] - 10),
        align="right-down", font_size=int(min(*game.size) / 10),
        color=color.Pink3, bg_alpha=0,
        click_func=home
    )
    settings_inited = True


def settings(game: PyGame, state: StateMachine):

    if not settings_inited:
        settings_init(game, state)

    # input
    for event in game.it.event.get():
        if event.type == game.it.QUIT:
            state.quit = True
        home_button.click_check(event)

    # control flow and calculate here
    pass

    # render
    game.screen.fill(color.white)
    home_button.render()

    game.render_update()
    game.clock.tick(60)
