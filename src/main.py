from utils.define import PyGame, StateMachine, StaticData
from pages.home import home
from pages.play import play
from pages.menu import menu
from pages.settings import settings


def main_game():

    screen_width = 1000
    screen_height = 500
    game = PyGame(screen_width, screen_height)
    state = StateMachine("home")
    
    state["normal"] = StaticData("data", "normal.yaml")
    state["score"] = StaticData("data", "score.yaml")
    state["normal"].load()
    state["score"].load()

    state["normal"].setdefault("speed", 10)
    state["normal"].setdefault("offset", -40)

    home_page = home(game, state)
    menu_page = menu(game, state, 240)
    settings_page = settings(game, state)
    play_page = play(game, state, 120)

    while not state.quit:
        if state == "home": home_page.show()
        elif state == "menu": menu_page.show()
        elif state == "play": play_page.show()
        elif state == "settings": settings_page.show()
    game.it.quit()


if __name__ == "__main__":
    main_game()
