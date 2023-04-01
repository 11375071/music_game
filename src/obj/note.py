import preload.img as img
import utils.color as color
from utils.define import PyGame
from typing import Union, Optional
from pygame.surface import Surface
from obj.property import ImageProperty


# todo: load_notes, notes, resolved notes all gathered here.
class Notes:
    def __init__():
        pass


class Note(ImageProperty):

    def __init__(
        self, game: PyGame,
        size: tuple = (50, 10), destination: tuple = (100, 100), align: str = "center",
        color: tuple = color.AliceBlue, alpha: float = 1,
        image: Optional[Union[str, Surface]] = img.note_surface_scaled,
        speed: float = 11, init_time: float = 1, time: float = 1,
    ) -> None:
        self.game = game
        self.size = size
        self.destination = destination
        self.align = align
        self.color = color
        self.alpha = alpha
        self.image = image
        self.speed = speed
        self.init_time = init_time
        self.time = time

        self.rank_type = "none"
        self.appear = False
        self.strip_alpha = False
        self.scaled = True

        self.change_image()
        self.align_destination()

    def align_destination(self):
        if self.align == "center":
            self.destination_align = self.destination[0] - self.size[0] / 2, \
                self.destination[1] - self.size[1] / 2
        elif self.align == "right-up":
            self.destination_align = self.destination[0] - self.size[0], \
                self.destination[1]
        elif self.align == "right-down":
            self.destination_align = self.destination[0] - self.size[0], \
                self.destination[1] - self.size[1]
        elif self.align == "left-down":
            self.destination_align = self.destination[0], self.destination[1] - self.size[1]
        else: 
            self.destination_align = self.destination[0], self.destination[1]

    def rank(self, rank_type: str):
        self.rank_type = rank_type
        self.resolved()

    @property
    def score(self) -> int:
        if self.rank_type == "perfect":
            return 1000
        if self.rank_type == "great":
            return 750
        if self.rank_type == "good":
            return 400
        return 0

    @property
    def max_score(self) -> int:
        return 1000

    def resolved(self):
        self.appear = False

    def render(self):
        if not self.appear:
            return
        self.pos = (
            self.destination_align[0],
            self.destination_align[1] - 50 * self.time * self.speed
        )
        self.game.screen.blit(self.image, self.pos)
