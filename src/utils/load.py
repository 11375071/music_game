from utils.define import PyGame, StateMachine
from obj.note import Note
import utils.color as color
from typing import Callable

def load_music(game: PyGame, music_path: str):
    game.it.mixer.music.load(music_path)
    game.it.mixer.music.set_volume(0.15)
    game.it.mixer.music.play()

def load_note_from_txt(game: PyGame, note_path: str, dest_func: Callable):
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
                        destination=dest_func(track)
                    )
                    notes.append(new_note)
            else:
                break
    finally:
        f.close()

    return notes

def load_note(game: PyGame, note_path: str, dest_func: Callable):
    bpm: float = 0
    notes: list = []
    f = open(note_path, 'r')
    try:
        while True:
            lines = f.readlines()
            line = ""
            for i in lines:
                line = line + i
            if lines:
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
                            destination=dest_func(i['column'])
                        )
                        notes.append(new_note)
            else:
                break
    finally:
        f.close()

    return notes

def level_to_song_path(lv):
    if lv == 1:
        return r"src/songs/Lv.1/vacuum/Mujinku-Vacuum Track#ADD8E6-.ogg", r"src/songs/Lv.1/vacuum/Mujinku-Vacuum Track#ADD8E6- (4K Beginner).mc"
    if lv == 2:
        return r"src/songs/Lv.2/sterelogue/VeetaCrush - Sterelogue.ogg", r"src/songs/Lv.2/sterelogue/Sterelogue (4ky_normal).mc"
    if lv == 3:
        return r"src/songs/Lv.3/bad apple/Bad Apple!! feat. nomico.ogg", r"src/songs/Lv.3/bad apple/1594123299.mc"
    if lv == 4:
        return r"src/songs/Lv.4/white/Nitta Emi - White Eternity.ogg", r"src/songs/Lv.4/white/Various Artists - Malody 4K Regular Dan v3-Starter(1).mc"
    if lv == 5:
        return r"src/songs/Lv.5/king/Tsunomaki Watame - KING.ogg", r"src/songs/Lv.5/king/Various Artists - Malody 4K Regular Dan v3-Starter (Reg-1 Map-4).mc"
    if lv == 6:
        return r"src/songs/Lv.6/stargazer/Lime - Stargazer.ogg", r"src/songs/Lv.6/stargazer/Various Artists - Malody 4K Regular Dan v3-Starter (Reg-2 Map-1).mc"