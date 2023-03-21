from typing import List
from utils.define import PyGame, StateMachine
import utils.color as color
from obj.button import Button, TextButton
from obj.note import Note

start_time: int = None
home_button: TextButton = None
rank_text: Button = None
score_text: Button = None
percentage_text: Button = None
play_button: Button = None
play_inited: bool = False

# must be in the time order
notes: List[Note] = []
resolved_notes: List[Note] = []



# todo: add an appear_notes list to only record the notes on screen


def play_init(game: PyGame, state: StateMachine):

    global start_time, \
        home_button, rank_text, score_text, percentage_text, play_button, play_inited, \
        notes, resolved_notes
    
    start_time = game.it.time.get_ticks()

    def home():
        state.state = "home"
        

    def key_press():
        for note in notes:
            if abs(note.time) < 0.06:
                notes.remove(note)
                resolved_notes.append(note)
                note.resolved()
                note.rank("perfect")
                rank_text.change_text("perfect")
                return
            elif abs(note.time) < 0.1:
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
        align="right-down", font_size=int(min(*game.size) / 25),
        color=color.Blue2, bg_alpha=0,
        click_func=home
    )
    play_button = Button(
        game, size=(50, 10), pos=(game.size[0] / 2, game.size[1] / 3 * 2),
        align="center",
        bg_color=color.Red, click_func=key_press, key=game.it.K_LEFT
    )
    rank_text = TextButton(
        game, pos=(game.size[0] / 2, game.size[1] / 3 * 2 + 30),
        align="center", text="hello_world",
        font_size=30, color=color.Red, 
        bg_color=color.White, click_func=None
    )
    score_text = TextButton(
        game, pos=(50, 60),
        align="left_up", text="hello_world",
        font_size=30, color=color.Red, 
        bg_color=color.White, click_func=None
    )
    percentage_text = TextButton(
        game, pos=(50, 100),
        align="left_up", text="hello_world",
        font_size=30, color=color.Red, 
        bg_color=color.White, click_func=None
    )

    play_inited = True


def play(game: PyGame, state: StateMachine):

    global start_time, notes

    if not play_inited:
        play_init(game, state)

    # input
    for event in game.it.event.get():
        if event.type == game.it.QUIT:
            state.quit = True
        home_button.click_check(event)
        play_button.click_check(event)

    # control flow and calculate here
    duration = game.it.time.get_ticks() - start_time
    start_time = game.it.time.get_ticks()

    for note in notes:
        note.time = note.time - duration * 0.001
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
        if note.rank_type == "good":
            score += 600

    if max_score == 0:
        pct = 0
    else:
        pct = score / max_score

    score_text.change_text("score: " + str(score))
    percentage_text.change_text("acc: " + "%.2f"%(pct * 100) + "%")

    # render
    game.screen.fill(color.white)
    home_button.render()
    rank_text.render()
    score_text.render()
    percentage_text.render()
    play_button.render()
    for note in notes:
        note.render()

    game.it.display.flip()
    game.clock.tick(60)
