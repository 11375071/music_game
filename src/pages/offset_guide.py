from typing import List
from utils.define import PyGame, StateMachine
from utils.load import load_music, load_note_from_txt, track_to_destination
import utils.color as color
from obj.button import Button, TextButton
from obj.note import Note

home_button: TextButton = None
confirm_button: TextButton = None
offset_text: TextButton = None
rank_text: TextButton = None
play_button_list: List[Button] = []
play_inited: bool = False

# must be in the time order
notes: List[Note] = []
offset_list: List[int] = []

# todo: add an appear_notes list to only record the notes on screen

def play_init(game: PyGame, state: StateMachine):

    global home_button, confirm_button, rank_text, offset_text, \
        play_button_list, play_inited, notes

    def home():
        global play_inited, offset_list
        game.it.mixer.music.unload()
        play_inited = False
        offset_list = []
        state.state = "home"

    def confirm():
        global play_inited, offset_list
        play_inited = False
        if len(offset_list):
            state.offset += int(sum(offset_list) / len(offset_list))
        offset_list = []
        state.state = "settings"

    home_button = TextButton(
        game, "return home", (game.size[0] - 10, game.size[1] - 10),
        align="right-down", font_size=30,
        color=color.Red3, bg_alpha=0,
        click_func=home
    )

    confirm_button = TextButton(
        game, "", (game.size[0] / 2, game.size[1] / 2),
        align="center", font_size=35,
        color=color.Red3, bg_alpha=0.4,
        click_func=confirm
    )

    offset_text = TextButton(
        game, pos=(50, 60),
        align="left-up", text="average offset: " + "%.2f"%(0),
        font_size=30, color=color.Red, 
        bg_color=color.White, bg_alpha=0,
        click_func=None
    )

    def key_press(destination):
        for note in notes:
            if note.destination != destination:
                continue
            if note.time < 0.15:
                notes.remove(note)
                note.resolved()
                offset_list.append(int(note.time * 1000))
                rank_text.change_text(str(int(note.time * 1000)))
                return
            else:
                return
            
    def key_press_0():
        return key_press(track_to_destination(game, 0))
    def key_press_1():
        return key_press(track_to_destination(game, 1))
    def key_press_2():
        return key_press(track_to_destination(game, 2))
    def key_press_3():
        return key_press(track_to_destination(game, 3))
    key_press_func_list = [key_press_0, key_press_1, key_press_2, key_press_3]
    key_list = [game.it.K_z, game.it.K_x, game.it.K_PERIOD, game.it.K_SLASH]
    key_list_text = ['z', 'x', '.', '/']

    # clear and create notes
    notes = []
    notes = load_note_from_txt(game, r"src/songs/Lv.0/offset_guide/offset_guide.txt")
    for note in notes:
        note.speed = state.speed

    # create button

    for i in range(4):
        play_button_list.append(
            Button(
                game, size=(50, 10), pos=track_to_destination(game, i),
                align="center",
                bg_color=color.Red, click_func=key_press_func_list[i],
                key=key_list[i], only_use_key=True
            )
        )
        play_button_list.append(
            TextButton(
                game, pos=track_to_destination(game, i),
                align="center", font_size=10,
                font_family="Arial",
                text=key_list_text[i],
                bg_alpha=0, color=color.White,
            )
        )
    
    rank_text = TextButton(
        game, pos=(game.size[0] / 2, game.size[1] / 3 * 2 + 30),
        align="center", text="0",
        font_size=30, color=color.Red, 
        bg_color=color.White, bg_alpha=0,
        click_func=None
    )

    # other
    load_music(game, r"src/songs/Lv.0/offset_guide/Bad Apple!! feat. nomico.ogg")
    play_inited = True

def render():
    for button in play_button_list:
        button.render()
    for note in notes:
        note.render()
    rank_text.render()
    offset_text.render()
    home_button.render()
    confirm_button.render()


def offset_guide(game: PyGame, state: StateMachine):

    # init
    if not play_inited:
        play_init(game, state)

    # input
    for event in game.it.event.get():
        if event.type == game.it.QUIT:
            state.quit = True
        home_button.click_check(event)
        confirm_button.click_check(event)
        for i in play_button_list:
            i.click_check(event)

    # control flow and calculate here
    if game.it.mixer.music.get_pos() > 9000:
        game.it.mixer.music.unload()
        confirm_button.change_text("confirm")

    duration = game.it.mixer.music.get_pos() + state.offset

    for note in notes:
        note.time = note.init_time - duration * 0.001
        if note.time < -0.3:
            notes.remove(note)
            note.resolved()
            note.rank("miss")

    if len(offset_list):
        offset_text.change_text("average offset: " + "%.2f"%(sum(offset_list) / len(offset_list)))

    # render
    game.screen.fill(color.white)
    render()
    game.render_update()
    game.clock.tick(60)
