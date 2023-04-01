import bisect
from pygame import event
import utils.color as color
from utils.define import PyGame
from pygame.surface import Surface
from typing import Callable, Optional, Union, Tuple, List, Any
from obj.button import SimpleButton
from obj.property import ClickCheckProperty, PositionProperty, ImageProperty

class ScrollArea(PositionProperty):
    def __init__(
        self, game: PyGame,
        size: tuple, pos: tuple, align: str = "center",
    ) -> None:
        self.game = game
        self.size = size
        self.pos = pos
        self.align = align

        self.choices_list: List[SimpleButton] = []
        self.mouse_pos: tuple = None
        self.now_index: float = 0
        self.len = 1
        self.selected: SimpleButton = None
        self.align_position()
    
    def collide(self, pos: tuple):
        return self.rect.collidepoint(*pos)

    def append_choice(self, object: Any):
        self.choices_list.append(object)
        self.len = len(self.choices_list)

    def render(self):
        index = 0
        render_list: List[Tuple[SimpleButton, float]] = []

        for i in self.choices_list:
            if abs(index - self.now_index) > abs(index - self.now_index + self.len):
                difference = index - self.now_index + self.len
            elif abs(index - self.now_index) > abs(index - self.now_index - self.len):
                difference = index - self.now_index - self.len
            else:
                difference = index - self.now_index
            scale = 5 / (abs(difference) + 5)
            size = self.size[0] * scale, self.size[1] / 2  * scale
            pos = size[0] / 2 + self.pos[0], self.size[1] / 2 * (1 + difference / 2.2)
            i.resize(pos, size)
            i.change_image()

            def insert_sorted(my_list, element):
                my_list.insert(bisect.bisect_left([i[1] for i in my_list], element[1]), element)
            new_element = (i, abs(difference))
            insert_sorted(render_list, new_element)

            index += 1
        
        self.selected = render_list[0]
        render_list.reverse()
        for i in render_list:
            i[0].render()

    def control_check(self):
        if self.mouse_pos is not None:
            vertical_partial = (self.mouse_pos[1] - self.pos[1]) / self.size[1]
            if vertical_partial < 0.25:
                self.now_index -= (0.25 - vertical_partial) / 5 + 0.05
            elif vertical_partial <= 0.75:
                if abs(self.now_index - round(self.now_index)) > 0.0001:
                    self.now_index -= (self.now_index - round(self.now_index)) * 0.3
            else:
                self.now_index += (vertical_partial - 0.75) / 5 + 0.05
            while self.now_index < 0:
                self.now_index += self.len
            while self.now_index > self.len:
                self.now_index -= self.len
        else:
            if abs(self.now_index - round(self.now_index)) > 0.0001:
                self.now_index -= (self.now_index - round(self.now_index)) * 0.4

    def event_check(self, event):
        self.mouse_pos = self.game.it.mouse.get_pos()
        if not self.collide(self.mouse_pos):
            self.mouse_pos = None
    