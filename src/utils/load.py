from utils.define import PyGame, StateMachine
from obj.note import Note
import utils.color as color

def track_to_destination(game: PyGame, track: int):
    track = 3 - track
    return (game.size[0] / 2 - 100 * track + 150, game.size[1] / 5 * 4)

def load_music(game: PyGame, music_path: str):
    game.it.mixer.music.load(music_path)
    game.it.mixer.music.set_volume(0.15)
    game.it.mixer.music.play()

def load_note_from_txt(game: PyGame, note_path: str):
    cnt: int = 0
    notes: list = []
    f = open(note_path, 'r')
    try:
        while True:
            line = f.readline()
            if line:
                if line[-1] == '\n':
                    line = line[:-1]
                cnt += 1
                if cnt == 1:
                    bpm = int(line)
                    continue
                if cnt == 2:
                    offset = int(line)
                    continue
                line = line.split()
                track = int(line[0][:-1])
                line = line[1:]
                for t in line:
                    new_note = Note(
                        game, init_time=float(t) / bpm * 60 - 0.001 * offset, color=color.Blue,
                        destination=track_to_destination(game, track)
                    )
                    notes.append(new_note)
            else:
                break
    finally:
        f.close()

    return notes

def load_note(game: PyGame, note_path: str):
    bpm: float = 0
    notes: list = []
    f = open(note_path, 'r')
    try:
        while True:
            line = f.readline()
            if line:
                dct = eval(line)
                bpm = dct['time'][-1]['bpm']
                note_list = dct['note']
                offset = 0
                for i in note_list:
                    if 'offset' in i.keys():
                        offset = i['offset']

                for i in note_list:
                    if 'column' in i.keys():
                        t = i['beat'][0] + i['beat'][1] / i['beat'][2]
                        new_note = Note(
                            game, init_time= t / bpm * 60 - 0.001 * offset, color=color.Blue,
                            destination=track_to_destination(game, i['column'])
                        )
                        notes.append(new_note)
            else:
                break
    finally:
        f.close()

    return notes