from utils.define import PyGame, StateMachine
import utils.color as color
from obj.button import TextButton
import matplotlib.image as mpimg

home_inited: bool = False
play_img, setting_img = None, None
background, play_origin, play_selected, setting_origin, setting_selected = None, None, None, None, None
play: bool = False
setting: bool = False

def home_init(game: PyGame, state: StateMachine):
    
    global home_inited, play_img, setting_img, \
        background, play_origin, play_selected, setting_origin, setting_selected, \
        play, setting

    play_img = mpimg.imread("src/image/play_origin.png")
    setting_img = mpimg.imread("src/image/setting_origin.png")

    background = game.it.image.load("src/image/home_page.png")
    background = game.it.transform.scale(
        background, (game.size[0], game.size[1])
    )
    background.convert_alpha()

    play_origin = game.it.image.load("src/image/play_origin.png")
    play_origin = game.it.transform.scale(
        play_origin, (game.size[0], game.size[1])
    )
    play_origin.convert_alpha()

    play_selected = game.it.image.load("src/image/play_selected.png")
    play_selected = game.it.transform.scale(
        play_selected, (game.size[0], game.size[1])
    )   
    play_selected.convert_alpha()

    setting_origin = game.it.image.load("src/image/setting_origin.png")
    setting_origin = game.it.transform.scale(
        setting_origin, (game.size[0], game.size[1])
    )
    setting_origin.convert_alpha()

    setting_selected = game.it.image.load("src/image/setting_selected.png")
    setting_selected = game.it.transform.scale(
        setting_selected, (game.size[0], game.size[1])
    )
    setting_selected.convert_alpha()

    play = False
    setting = False
    home_inited = True

def check_image_click(x, y, img):
    x, y = int(y / 500 * img.shape[0]), int(x / 1000 * img.shape[1])
    return img[x][y][-1]

def home(game: PyGame, state: StateMachine):

    if not home_inited:
        home_init(game, state)

    global play, setting
    # input
    for event in game.it.event.get():
        if event.type == game.it.QUIT:
            state.quit = True
        if event.type == game.it.MOUSEMOTION:
            if check_image_click(event.pos[0], event.pos[1], play_img):
                play = True
            else:
                play = False
            if check_image_click(event.pos[0], event.pos[1], setting_img):
                setting = True
            else:
                setting = False
        if event.type == game.it.MOUSEBUTTONDOWN:
            if play:
                state.state = "play"
            if setting:
                state.state = "settings"

    # control flow and calculate here
    pass

    # render

    game.screen.blit(background, (0, 0))

    if play:
        game.screen.blit(play_selected, (0, 0))
    else:
        game.screen.blit(play_origin, (0, 0))

    if setting:
        game.screen.blit(setting_selected, (0, 0))
    else:
        game.screen.blit(setting_origin, (0, 0))

    game.render_update()
    game.clock.tick(60)
