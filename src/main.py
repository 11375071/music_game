from utils.define import PyGame, StateMachine, StaticData
from pages.home import home
from pages.play import play
from pages.menu import menu
from pages.settings import settings
from pages.offset_guide import offset_guide

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
    state["normal"].setdefault("level", 1)

    home_page = home(game, state)
    menu_page = menu(game, state)
    settings_page = settings(game, state)

    while not state.quit:
        if state == "home": home_page.show()
        elif state == "menu": menu_page.show()
        elif state == "play": play(game, state)
        elif state == "settings": settings_page.show()
        elif state == "offset_guide": offset_guide(game, state)
    game.it.quit()


if __name__ == "__main__":
    main_game()
