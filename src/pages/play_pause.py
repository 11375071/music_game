from utils.define import PyGame, StateMachine
from obj.button import Button, TextButton
import utils.color as color

back_layer: Button = None
home_button: TextButton = None
replay_button: TextButton = None
resume_button: TextButton = None
play_pause_inited: bool = False

def play_pause_init(game: PyGame, state: StateMachine):
    global back_layer, home_button, replay_button, resume_button, play_pause_inited

    def home():
        state.sub_page = "replay"
        state.state = "home"
    
    def replay():
        state.sub_page = "replay"
    
    def resume():
        state.sub_page = None

    back_layer = Button(
        game, (game.size[0] / 3 * 2, game.size[1] / 3 * 2),
        (game.size[0] / 2, game.size[1] / 2),
        align="center", bg_alpha=0.85
    )
    resume_button = TextButton(
        game, "RESUME", (game.size[0] / 2, game.size[1] / 6 * 2),
        align="center", font_size=int(min(*game.size) / 15),
        color=color.Blue2, bg_alpha=0,
        click_func=resume
    )
    replay_button = TextButton(
        game, "REPLAY", (game.size[0] / 2, game.size[1] / 6 * 3),
        align="center", font_size=int(min(*game.size) / 15),
        color=color.Blue2, bg_alpha=0,
        click_func=replay
    )
    home_button = TextButton(
        game, "RETURN HOME", (game.size[0] / 2, game.size[1] / 6 * 4),
        align="center", font_size=int(min(*game.size) / 15),
        color=color.Blue2, bg_alpha=0,
        click_func=home
    )

    play_pause_inited = True

def play_pause(game: PyGame, state: StateMachine):

    if not play_pause_inited:
        play_pause_init(game, state)
    
    for event in game.it.event.get():
        if event.type == game.it.QUIT:
            state.quit = True
        home_button.click_check(event)
        replay_button.click_check(event)
        resume_button.click_check(event)
    
    # 不加 mother 的话就没法透明了（透明似乎基于前面 render 的计算）
    # 同时这里使用 specify 是因为这一步之前 state.state 可能已经变成 home 了
    state.specify_mother_render("play")(for_pause = True)
    back_layer.render()
    resume_button.render()
    replay_button.render()
    home_button.render()

    game.render_update()
    game.clock.tick(60)
