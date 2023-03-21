from utils.define import PyGame, StateMachine
from obj.note import Note
import utils.color as color

def track_to_destination(game, track):
    track = 3 - track
    return (game.size[0] / 2 - 100 * track + 150, game.size[1] / 3 * 2)

def load_music(game: PyGame, music_path: str):
    game.it.mixer.music.load(music_path)
    game.it.mixer.music.play()

def load_note_from_txt(game: PyGame, note_path: str):
    bpm: float = 0
    notes: list = []
    f = open(note_path, 'r')
    try:
        while True:
            line = f.readline()
            if line:
                if line[-1] == '\n':
                    line = line[:-1]
                if bpm == 0:
                    bpm = int(line)
                    continue
                line = line.split()
                track = int(line[0][:-1])
                line = line[1:]
                for t in line:
                    new_note = Note(
                        game, time=float(t) / bpm * 60, color=color.Blue,
                        destination=track_to_destination(game, track)
                    )
                    notes.append(new_note)
            else:
                break
    finally:
        f.close()

    return notes