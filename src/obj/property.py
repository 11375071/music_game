from pygame import event
from numpy import ndarray
from utils.define import PyGame
import matplotlib.image as mpimg
from pygame.surface import Surface
from typing import Callable, Optional, Union, Tuple


class ClickCheckProperty:
    """
    `pre_click_check(event)`, `click_check(event)`, `control_check()`
    """

    def __init__(self) -> None:
        """
        DO NOT INIT THIS
        this is just for typing comment
        """
        self.game: PyGame = None
        self.click_func: Callable = None
        self.key: Optional[int] = None
        self.only_use_key: bool = None
        self.activate_on_keydown: bool = None
        self.long_update: bool = None
        self.now_press_state: str = None
        self.long_press_frame: int = None
        self.long_press_max: int = None
        self._ready_to_click: bool = None
        self._ready_to_key: bool = None
        assert(False, "you cannot init ClickCheckProperty")

    def pre_click_check(self, event: event.Event):
        pos = self.game.it.mouse.get_pos()
        if event.type == self.game.it.MOUSEMOTION:
            if self.collide(pos):
                if self.game.it.mouse.get_pressed()[0]:
                    self.now_press_state = "click"
                else:
                    self.now_press_state = "hover"
            else:
                self.now_press_state = "default"
        return pos

    def click_check(self, event: event.Event):

        if not self.only_use_key:
            # avoid get pos for 2 times
            pos = self.pre_click_check(event)
        else:
            pos = self.game.it.mouse.get_pos()

        if self.click_func is not None:

            if self.activate_on_keydown:
                if not self.only_use_key:
                    if event.type == self.game.it.MOUSEBUTTONDOWN:
                        if self.collide(pos):
                            self.now_press_state = "click"
                            self.click_func()
                        else:
                            self.now_press_state = "default"
                    elif event.type == self.game.it.MOUSEBUTTONUP:
                        self.now_press_state = "default"
                if self.key is not None:
                    if event.type == self.game.it.KEYDOWN and event.key == self.key:
                        self.now_press_state = "click"
                        self.click_func()
                    if event.type == self.game.it.KEYUP and event.key == self.key:
                        self.now_press_state = "default"

            else:  # activate_on_keyup
                if not self.only_use_key:
                    if event.type == self.game.it.MOUSEBUTTONDOWN:
                        if self.collide(pos):
                            self.now_press_state = "click"
                            self._ready_to_click = True
                        else:
                            self.now_press_state = "default"
                            self._ready_to_click = False
                    if event.type == self.game.it.MOUSEBUTTONUP:
                        if self.collide(pos):
                            self.now_press_state = "default"
                            if self._ready_to_click:
                                self._ready_to_click = False
                                self.click_func()
                if self.key is not None:
                    if event.type == self.game.it.KEYDOWN:
                        if event.key == self.key:
                            self.now_press_state = "click"
                            self._ready_to_key = True
                        else:
                            self.now_press_state = "default"
                            self._ready_to_key = False
                    if event.type == self.game.it.KEYUP:
                        if event.key == self.key:
                            self.now_press_state = "default"
                            if self._ready_to_key:
                                self._ready_to_key = False
                                self.click_func()

    def control_check(self):
        if self.click_func is not None:
            if self.activate_on_keydown and self.long_update:
                if self.now_press_state == "click":
                    self.long_press_frame += 1
                else:
                    self.long_press_max = 25
                    self.long_press_frame = 0
                if self.long_press_frame >= self.long_press_max:
                    self.long_press_max = 5
                    self.long_press_frame = 0
                    self.click_func()


class ImageProperty:
    """
    `change_image()`
    """
    
    def __init__(self) -> None:
        """
        DO NOT INIT THIS
        this is just for typing comment
        """
        self.game: PyGame = None
        self.size: tuple = None
        self.color: tuple = None
        self.alpha: float = None
        self.image: Optional[Union[str, Surface, Tuple[Surface, ndarray]]] = None
        self.strip_alpha: bool = None
        self.scaled: bool = None
        assert(False, "you cannot init ImageProperty")

    def change_image(self):
        if type(self.image) is tuple:
            if self.strip_alpha:
                self.load_image = self.image[1]
            if self.scaled:
                self.image = self.image[0]
            else:
                self.image = self.game.it.transform.scale(
                    self.image[0], self.size
                )
        elif type(self.image) is Surface:
            if self.strip_alpha:
                assert(False, "Surface cannot support strip_alpha, try Tuple[Surface, ndarray] instead")
            if self.scaled:
                self.image = self.image
            else:
                self.image = self.game.it.transform.scale(
                    self.image, self.size
                )
        elif type(self.image) is str:
            if self.strip_alpha:
                self.load_image = mpimg.imread(self.image)
            self.image = self.game.it.image.load(self.image)
            if self.scaled:
                self.image = self.image
            else:
                self.image = self.game.it.transform.scale(
                    self.image, self.size
                )
        else:
            self.image = self.game.it.Surface(self.size)
            self.image.fill(self.color)
            self.image.set_alpha(int(256 * self.alpha))


class PositionProperty:
    """
    `align_position()`, `change_position(pos, size)`
    """
    
    def __init__(self) -> None:
        """
        DO NOT INIT THIS
        this is just for typing comment
        """
        self.game: PyGame = None
        self.size: tuple = None
        self.pos: tuple = None
        self.align: str = None
        assert(False, "you cannot init PositionProperty")
    
    def align_position(self):
        if self.align == "center":
            self.pos_align = self.pos[0] - self.size[0] / 2, \
                self.pos[1] - self.size[1] / 2
        elif self.align == "right-up":
            self.pos_align = self.pos[0] - self.size[0], self.pos[1]
        elif self.align == "right-down":
            self.pos_align = self.pos[0] - \
                self.size[0], self.pos[1] - self.size[1]
        elif self.align == "left-down":
            self.pos_align = self.pos[0], self.pos[1] - self.size[1]
        else:  # "left-up"
            self.pos_align = self.pos
        self.rect = self.game.it.Rect(self.pos_align, self.size)

    def change_position(self, pos: tuple, size: tuple):
        if self.align == "center":
            pos_align = pos[0] - size[0] / 2, \
                pos[1] - size[1] / 2
        elif self.align == "right-up":
            pos_align = pos[0] - size[0], pos[1]
        elif self.align == "right-down":
            pos_align = pos[0] - \
                size[0], pos[1] - size[1]
        elif self.align == "left-down":
            pos_align = pos[0], pos[1] - size[1]
        else:  # "left-up"
            pos_align = pos
        self.rect = self.game.it.Rect(pos_align, size)
