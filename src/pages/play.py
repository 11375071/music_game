from typing import List
from utils.define import PyGame, StateMachine
import utils.color as color
from obj.button import Button, TextButton
from obj.note import Note

start_time: int = None
home_button: TextButton = None
visible_play_button: Button = None
play_button: Button = None
play_inited: bool = False
notes: List[Note] = []


def play_init(game: PyGame, state: StateMachine):

    global start_time, home_button, visible_play_button, play_button, play_inited, notes
    start_time = game.it.time.get_ticks()

    def home():
        state.state = "home"

    def key_press():
        for note in notes:
            if note.valid == False:
                continue
            if abs(note.time) < 0.06:
                note.resolved()
                print("perfect")
                return
            if abs(note.time) < 0.1:
                note.resolved()
                print("good")
                return
            if note.time < 0.15:
                note.valid = False
                note.resolved()
                print("miss")
                return

    # create notes
    for i in range(30):
        new_note = Note(
            game, time=i + 1, color=color.Blue,
            destination=(game.size[0] / 2, game.size[1] / 3 * 2)
        )
        notes.append(new_note)

    # create button
    home_button = TextButton(
        game, "RETURN HOME", (game.size[0] - 10, game.size[1] - 10),
        align="right-down", font_size=int(min(*game.size) / 10),
        color=color.Blue2, bg_alpha=0,
        click_func=home
    )
    visible_play_button = Button(
        game, size=(50, 10), pos=(game.size[0] / 2, game.size[1] / 3 * 2),
        align="center",
        bg_color=color.Red, click_func=None
    )
    play_button = Button(
        game, size=(50, game.size[1]), pos=(game.size[0] / 2, game.size[1] / 3 * 2),
        align="center", bg_alpha=0,
        bg_color=color.White, click_func=key_press
    )
    play_inited = True


def play(game: PyGame, state: StateMachine):

    if not play_inited:
        play_init(game, state)

    # input
    for event in game.it.event.get():
        if event.type == game.it.QUIT:
            state.quit = True
        home_button.click_check(event)
        play_button.click_check(event)

    # control flow and calculate here
    global start_time
    duration = game.it.time.get_ticks() - start_time
    start_time = game.it.time.get_ticks()

    for note in notes:
        note.time = note.time - duration * 0.001
        if note.time < -0.3:
            note.valid = False

    # render
    game.screen.fill(color.white)
    home_button.render()
    visible_play_button.render()
    play_button.render()
    for note in notes:
        if note.valid:
            note.render()

    game.it.display.flip()
    game.clock.tick(60)
