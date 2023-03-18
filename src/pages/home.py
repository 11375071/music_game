from utils.define import PyGame, StateMachine
import utils.color as color
from obj.button import TextButton

clock = None
play_button = None
settings_button = None
home_inited = False


def home_init(game: PyGame, state: StateMachine):

    def play():
        state.state = "play"

    def settings():
        state.state = "settings"

    global clock, play_button, settings_button, home_inited
    clock = game.it.time.Clock()
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

    print("now page: home")

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

    game.it.display.flip()
    clock.tick(60)
