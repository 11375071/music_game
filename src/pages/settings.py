from define import PyGame, StateMachine
import resource.color as color


def settings(game: PyGame, state: StateMachine):
    for event in game.it.event.get():
        if event.type == game.it.QUIT:
            state.quit = True
    game.screen.fill(color.white)
    game.it.display.flip()
