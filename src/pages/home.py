from utils.define import PyGame, StateMachine
import utils.color as color
from obj.button import TextButton

play_button: TextButton = None
settings_button: TextButton = None
home_inited: bool = False


def home_init(game: PyGame, state: StateMachine):

    def play():
        state.state = "play"

    def settings():
        state.state = "settings"

    global play_button, settings_button, home_inited
    play_button = TextButton(
        game, "PLAY", (game.size[0] / 2, game.size[1] / 3),
        font_size=int(min(*game.size) / 5),
        color=color.Blue2, bg_alpha=0,
        click_func=play
    )
    settings_button = TextButton(
        game, "SETTINGS", (game.size[0] / 2, game.size[1] / 3 * 2),
        font_size=int(min(*game.size) / 5.5),
        color=color.Blue2, bg_alpha=0,
        click_func=settings
    )
    home_inited = True


def home(game: PyGame, state: StateMachine):

    if not home_inited:
        home_init(game, state)

    # input
    for event in game.it.event.get():
        if event.type == game.it.QUIT:
            state.quit = True
        play_button.click_check(event)
        settings_button.click_check(event)

    # control flow and calculate here
    pass

    # render
    game.screen.fill(color.AntiqueWhite2)
    play_button.render()
    settings_button.render()

    game.render_update()
    game.clock.tick(60)
