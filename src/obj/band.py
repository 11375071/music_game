import math
import bisect
from pygame import event
import utils.color as color
from utils.define import PyGame
from pygame.surface import Surface
from typing import Callable, Optional, Union, Tuple, List, Any
from obj.button import SimpleButton
from obj.property import KeyCheckProperty, PositionProperty, ImageProperty

class ScrollArea(PositionProperty):
    def __init__(
        self, game: PyGame,
        size: tuple, pos: tuple, align: str = "center",
        band_size_ratio: tuple = (1, 0.5),
        band_density: float = 2.5,
        enable_mouse_wheel: bool = True,
        selected_activate_key: Optional[int] = None,
    ) -> None:
        """
        a scroll area
        """
        self.game = game
        self.size = size
        self.pos = pos
        self.align = align
        self.band_size_ratio = band_size_ratio
        self.band_density = band_density
        self.enable_mouse_wheel = enable_mouse_wheel
        self.selected_activate_key = selected_activate_key

        self.choices_list: List[SimpleButton] = []
        self.render_list: List[Tuple[SimpleButton, float]] = []
        self.mouse_pos: tuple = None
        self.now_index: float = 0
        self.len = 1
        self.selected: SimpleButton = None
        self.mouse_scroll_wait: float = 0
        self.align_position()
    
    def collide(self, pos: tuple) -> bool:
        return self.collide_rect.collidepoint(*pos)

    def append_choice(self, object: Any) -> None:
        self.choices_list.append(object)
        self.len = len(self.choices_list)

    def render(self) -> None:
        index = 0
        self.render_list.clear()

        for i in self.choices_list:
            if abs(index - self.now_index) > abs(index - self.now_index + self.len):
                difference = index - self.now_index + self.len
            elif abs(index - self.now_index) > abs(index - self.now_index - self.len):
                difference = index - self.now_index - self.len
            else:
                difference = index - self.now_index
            scale = 5 / (abs(difference) + 5)
            i.align = "center"
            size = self.size[0] * self.band_size_ratio[0] * scale, \
                self.size[1] * self.band_size_ratio[1] * scale
            pos = size[0] / 2 + self.pos[0], self.size[1] / 2 * (1 + difference / self.band_density * scale) + self.pos[1]
            i.resize(pos, size)
            i.change_image()

            def insert_sorted(my_list, element):
                my_list.insert(bisect.bisect_left([i[1] for i in my_list], element[1]), element)
            new_element = (i, abs(difference))
            insert_sorted(self.render_list, new_element)

            index += 1
        
        self.selected = self.render_list[0][0]
        self.render_list.reverse()
        for i in self.render_list:
            i[0].render()
        self.render_list.reverse()

    def event_check(self, event) -> bool:

        activated = False

        for i in self.render_list:
            if i[0].event_check(event):
                activated = True
                break  # do not activate the covered button

        self.mouse_pos = self.game.it.mouse.get_pos()
        if not self.collide(self.mouse_pos):
            self.mouse_pos = None
        
        if self.enable_mouse_wheel:
            if event.type == self.game.it.MOUSEBUTTONDOWN and event.button == 4:
                self.now_index -= 0.6
                self.mouse_scroll_wait = -0.08
            elif event.type == self.game.it.MOUSEBUTTONDOWN and event.button == 5:
                self.now_index += 0.6
                self.mouse_scroll_wait = 0.08
        
        if self.len >= 3:
            while self.now_index < 0:
                self.now_index += self.len
            while self.now_index > self.len - 1:
                self.now_index -= self.len
        else:
            if self.now_index < 0:
                self.now_index = 0
            elif self.now_index > self.len - 1:
                self.now_index = self.len - 1

        if self.selected_activate_key is not None and self.selected is not None and self.selected.click_func is not None:
            if event.type == self.game.it.KEYDOWN and event.key == self.selected_activate_key:
                self.selected.now_press_state = "click"
                self.selected.click_func()
                activated = True
            if event.type == self.game.it.KEYUP and event.key == self.selected_activate_key:
                self.selected.now_press_state = "default"

        return activated

    def control_check(self) -> bool:

        activated = False

        for i in self.render_list:
            if i[0].control_check():
                activated = True
                break  # do not activate the covered button

        if self.mouse_scroll_wait != 0:
            self.now_index += self.mouse_scroll_wait
            if abs(self.mouse_scroll_wait) > 0.01:
                self.mouse_scroll_wait /= 1.2
            else:
                self.mouse_scroll_wait = 0

        if self.mouse_pos is not None:
            vertical_partial = (self.mouse_pos[1] - self.pos[1]) / self.size[1]
            if vertical_partial < 0.28:
                self.now_index -= (0.28 - vertical_partial) / 5 + 0.05
            elif vertical_partial <= 0.72:
                if abs(self.now_index - round(self.now_index)) > 0.0001:
                    self.now_index -= (self.now_index - round(self.now_index)) * 0.3
            else:
                self.now_index += (vertical_partial - 0.72) / 5 + 0.05
            
        else:
            if abs(self.now_index - round(self.now_index)) > 0.0001:
                self.now_index -= (self.now_index - round(self.now_index)) * 0.4
        
        if self.len >= 3:
            while self.now_index < 0:
                self.now_index += self.len
            while self.now_index > self.len - 1:
                self.now_index -= self.len
        else:
            if self.now_index < 0:
                self.now_index = 0
            elif self.now_index > self.len - 1:
                self.now_index = self.len - 1
        
        return activated
