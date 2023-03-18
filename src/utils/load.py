from define import PyGame, StateMachine


def load_music(game: PyGame, music_path):
    game.it.mixer.music.load(music_path)
    game.it.mixer.music.play()
