from typing import List
from utils.define import PyGame, StateMachine
from utils.load import load_music, load_note, track_to_destination, level_to_song_path
import utils.color as color
from obj.button import Button, TextButton
from obj.note import Note
from pages.play_pause import play_pause

back_layer: Button = None
pause_button: TextButton = None
rank_text: TextButton = None
score_text: TextButton = None
percentage_text: TextButton = None
play_button_list: List[Button] = []
play_inited: bool = False

# must be in the time order
notes: List[Note] = []
resolved_notes: List[Note] = []

# todo: add an appear_notes list to only record the notes on screen


def play_init(game: PyGame, state: StateMachine):

    global back_layer, \
        pause_button, rank_text, score_text, percentage_text, \
        play_button_list, play_inited, notes, resolved_notes


    # functions
    def pause():
        game.it.mixer.music.pause()
        state.sub_page = "pause"

    def key_press(destination):
        for note in notes:
            if note.destination != destination:
                continue
            if abs(note.time) < 0.044:
                notes.remove(note)
                resolved_notes.append(note)
                note.resolved()
                note.rank("perfect")
                rank_text.change_text("perfect")
                return
            elif abs(note.time) < 0.084:
                notes.remove(note)
                resolved_notes.append(note)
                note.resolved()
                note.rank("great")
                rank_text.change_text("great")
                return
            elif abs(note.time) < 0.118:
                notes.remove(note)
                resolved_notes.append(note)
                note.resolved()
                note.rank("good")
                rank_text.change_text("good")
                return
            elif note.time < 0.15:
                notes.remove(note)
                resolved_notes.append(note)
                note.resolved()
                note.rank("miss")
                rank_text.change_text("miss")
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
    resolved_notes = []
    notes = load_note(game, level_to_song_path(state.lv)[1])
    for note in notes:
        note.speed = state.speed


    # create button
    back_layer = Button(
        game, (game.size[0], game.size[1]), (0, 0),
        bg_color=color.White, align="left-up", bg_alpha=1
    )

    pause_button = TextButton(
        game, "PAUSE", (game.size[0] - 10, 10),
        align="right-up", font_size=int(min(*game.size) / 20),
        color=color.Blue2, bg_alpha=0,
        click_func=pause, key=game.it.K_SPACE
    )

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
        align="center", text="hello_world",
        font_size=30, color=color.Red, 
        bg_color=color.White, bg_alpha=0,
        click_func=None
    )

    score_text = TextButton(
        game, pos=(50, 60),
        align="left-up", text="hello_world",
        font_size=30, color=color.Red, 
        bg_color=color.White, bg_alpha=0,
        click_func=None
    )

    percentage_text = TextButton(
        game, pos=(50, 100),
        align="left-up", text="hello_world",
        font_size=30, color=color.Red, 
        bg_color=color.White, bg_alpha=0,
        click_func=None
    )


    # other
    load_music(game, level_to_song_path(state.lv)[0])
    play_inited = True

def render(for_pause: bool = False):
    back_layer.render()
    for button in play_button_list:
        button.render()
    for note in notes:
        note.render()
    if not for_pause:
        pause_button.render()
    rank_text.render()
    score_text.render()
    percentage_text.render()


def play(game: PyGame, state: StateMachine):

    # init
    if not play_inited:
        play_init(game, state)

    # state machine
    if state.sub_page is not None:
        state.mother_render = render
        if state.sub_page == "pause":
            play_pause(game, state)
        if state.sub_page == "replay":
            state.sub_page = None
            play_init(game, state)
        return

    # input
    for event in game.it.event.get():
        if event.type == game.it.QUIT:
            state.quit = True
        pause_button.click_check(event)
        for i in play_button_list:
            i.click_check(event)

    # control flow and calculate here
    duration = game.it.mixer.music.get_pos() + state.offset

    for note in notes:
        note.time = note.init_time - duration * 0.001
        if note.time < -0.3:
            notes.remove(note)
            resolved_notes.append(note)
            note.resolved()
            note.rank("miss")
            rank_text.change_text("miss")

    score = 0
    max_score = 0
    for note in resolved_notes:
        max_score += 1000
        if note.rank_type == "perfect":
            score += 1000
        if note.rank_type == "great":
            score += 750
        if note.rank_type == "good":
            score += 400

    if max_score == 0:
        pct = 0
    else:
        pct = score / max_score

    score_text.change_text("score: " + str(score))
    percentage_text.change_text("acc: " + "%.2f"%(pct * 100) + "%")

    # render
    render()
    game.render_update()
    game.clock.tick(60)
