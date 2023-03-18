from utils.define import PyGame, StateMachine
import utils.color as color
from obj.button import TextButton

clock = None
home_button = None
play_inited = False


def play_init(game: PyGame, state: StateMachine):

    def home():
        state.state = "home"

    global clock, home_button, play_inited
    clock = game.it.time.Clock()
    home_button = TextButton(
        game, "RETURN HOME", (game.size[0] - 10, game.size[1] - 10),
        align="right-down", font_size=int(min(*game.size) / 10),
        color=color.Blue2, bg_alpha=0,
        click_func=home
    )
    play_button = TextButton(
        game, "", (game.size[0] / 2, game.size[1] / 2),
        align="center", font_size=int(min(*game.size) / 10),
        color=color.Blue2, bg_alpha=0,
        click_func=home
    )
    play_inited = True


def play(game: PyGame, state: StateMachine):

    print("now page: play")

    if not play_inited:
        play_init(game, state)

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

    game.it.display.flip()
    clock.tick(60)
