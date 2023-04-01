from typing import List
import os

class Song:
    def __init__(
        self, song_name, level, dir, song_file, note_file
    ) -> None:
        self.dir = dir
        self.level = level
        self.song_name = song_name
        self.song_file = song_file
        self.note_file = note_file

    @property
    def string(self) -> str:
        return self.song_name + "  LV:" + str(self.level)

    @property
    def song_path(self):
        return os.path.join(self.dir, self.song_file)

    @property
    def note_path(self):
        return os.path.join(self.dir, self.note_file)

song_list: List[Song] = [
    Song("Vacuum", 1, "src/songs/Lv.1/vacuum", "Mujinku-Vacuum Track#ADD8E6-.ogg", "Mujinku-Vacuum Track#ADD8E6- (4K Beginner).mc"),
    Song("Sterelogue", 2, "src/songs/Lv.2/sterelogue", "VeetaCrush - Sterelogue.ogg", "Sterelogue (4ky_normal).mc"),
    Song("Bad Apple", 3, "src/songs/Lv.3/bad apple", "Bad Apple!! feat. nomico.ogg", "1594123299.mc"),
    Song("Erika", 3, "src/songs/Lv.3/erika", "Amamiya Erika - Ikitoshi ikerumono.ogg", "Various Artists - Malody 4K Regular Dan v3-Starter.mc"),
    Song("White Eternity", 4, "src/songs/Lv.4/white", "Nitta Emi - White Eternity.ogg", "Various Artists - Malody 4K Regular Dan v3-Starter(1).mc"),
    Song("KING", 5, "src/songs/Lv.5/king", "Tsunomaki Watame - KING.ogg", "Various Artists - Malody 4K Regular Dan v3-Starter (Reg-1 Map-4).mc"),
    Song("Stargazer", 6, "src/songs/Lv.6/stargazer", "Lime - Stargazer.ogg", "Various Artists - Malody 4K Regular Dan v3-Starter (Reg-2 Map-1).mc"),
    Song("Adjudicatorz", 6, "src/songs/Lv.6/adjudicatorz", "Nyankon - Adjudicatorz-Danzai-.ogg", "1584371562.mc"),
    Song("Mermaid Girl", 6, "src/songs/Lv.6/mermaid girl", "DJ Command - Mermaid Girl.ogg", "Various Artists - Malody 4K Regular Dan v3-Starter (Reg-2 Map-4).mc"),
]