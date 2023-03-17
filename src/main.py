from define import PyGame, StateMachine
from pages.home import home
from pages.play import play
from pages.settings import settings


def main_game():

    screen_width = 640
    screen_height = 480
    game = PyGame(screen_width, screen_height)
    state = StateMachine("home")

    while not state.quit:
        if state == "home":
            home(game, state)
        elif state == "play":
            play(game, state)
        elif state == "settings":
            settings(game, state)

    game.it.quit()


if __name__ == "__main__":
    main_game()
