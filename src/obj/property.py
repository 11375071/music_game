from pygame import event
from numpy import ndarray
from utils.define import PyGame
import matplotlib.image as mpimg
from pygame.surface import Surface
from typing import Callable, Optional, Union, Tuple


class KeyCheckProperty:
    """
    Add some methods and properties about keys and clicks

    Required Properties:
        `game` (PyGame): define.PyGame
        `click_func` (Callable): ... 
        `key` (int | None): ...
        `only_use_key` (bool): ...
        `activate_on_keydown` (bool): ...
        `press_update` (bool): ...

        `now_press_state` (str): just make it ""
        `long_press_frame` (int): just make it 0
        `long_press_max` (int): just make it 0
        `ready_to_click` (bool): just make it False
        `ready_to_key` (bool): just make it False
    
    Required Methods:
        `collide(pos) -> bool`: ...

    New Methods:
        `pre_event_check() -> tuple`: ...
        `event_check(event) -> bool`: ...
        `control_check() -> bool`: ...
    
    Changed Properties:
        `self.now_press_state` (str): "default", "hover", "click"
        `self.long_press_frame` (int): ...
        `self.long_press_max` (int): ...
        `self.ready_to_click` (bool): ...
        `self.ready_to_key` (bool): ...
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
        self.press_update: bool = None
        self.now_press_state: str = None
        self.long_press_frame: int = None
        self.long_press_max: int = None
        self.ready_to_click: bool = None
        self.ready_to_key: bool = None
        assert(False, "you cannot init KeyCheckProperty")

    def pre_event_check(self, event: event.Event) -> tuple:
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

    def event_check(self, event: event.Event) -> bool:

        activated = False

        if not self.only_use_key:
            # avoid get pos for 2 times
            pos = self.pre_event_check(event)
        else:
            pos = self.game.it.mouse.get_pos()

        if self.click_func is not None:

            if self.activate_on_keydown:
                if not self.only_use_key:
                    if event.type == self.game.it.MOUSEBUTTONDOWN and event.button == 1:
                        if self.collide(pos):
                            self.now_press_state = "click"
                            self.click_func()
                            activated = True
                        else:
                            self.now_press_state = "default"
                    elif event.type == self.game.it.MOUSEBUTTONUP and event.button == 1:
                        self.now_press_state = "default"
                if self.key is not None:
                    if event.type == self.game.it.KEYDOWN and event.key == self.key:
                        self.now_press_state = "click"
                        self.click_func()
                        activated = True
                    if event.type == self.game.it.KEYUP and event.key == self.key:
                        self.now_press_state = "default"

            else:  # activate_on_keyup
                if not self.only_use_key:
                    if event.type == self.game.it.MOUSEBUTTONDOWN and event.button == 1:
                        if self.collide(pos):
                            self.now_press_state = "click"
                            self.ready_to_click = True
                        else:
                            self.now_press_state = "default"
                            self.ready_to_click = False
                    if event.type == self.game.it.MOUSEBUTTONUP and event.button == 1:
                        if self.collide(pos):
                            self.now_press_state = "default"
                            if self.ready_to_click:
                                self.ready_to_click = False
                                self.click_func()
                                activated = True
                if self.key is not None:
                    if event.type == self.game.it.KEYDOWN:
                        if event.key == self.key:
                            self.now_press_state = "click"
                            self.ready_to_key = True
                        else:
                            self.now_press_state = "default"
                            self.ready_to_key = False
                    if event.type == self.game.it.KEYUP:
                        if event.key == self.key:
                            self.now_press_state = "default"
                            if self.ready_to_key:
                                self.ready_to_key = False
                                self.click_func()
                                activated = True
        return activated

    def control_check(self) -> bool:
        activated = False
        if self.click_func is not None:
            if self.activate_on_keydown and self.press_update:
                if self.now_press_state == "click":
                    self.long_press_frame += 1
                else:
                    self.long_press_max = 25
                    self.long_press_frame = 0
                if self.long_press_frame >= self.long_press_max:
                    self.long_press_max = 5
                    self.long_press_frame = 0
                    self.click_func()
                    activated = True
        return activated


class ImageProperty:
    """
    Add some methods and properties about image

    Required Properties:
        `game` (PyGame): define.PyGame
        `size` (tuple): (x_width, y_height), float number allowed
        `image` (Surface): pygame.surface.Surface (recommend to use ImageProperty to get it)
        `color` (tuple): (R, G, B), range in 0 ~ 255. Validate when `image` is None
        `alpha` (float): 0.0 ~ 1.0, 0.0 is transparent, 1.0 is opaque
        `image` (None | str | Surface | tuple): None (use solid color), str (picture path), Surface (pygame.surface.Surface), Tuple[Surface, ndarry] (mpimg.imread, see `collide_ignore_transparent`)
        `collide_ignore_transparent` (bool): if is True, `collide()` will dismiss area where picture's alpha == 0. If enabled, use Tuple[Surface, ndarry] as `image` will load faster
        `already_scaled` (bool): if is True, `change_image()` will not resize
    
    New Methods:
        `change_image()`: convert `self.image` (None | str | Surface | tuple) into `self.image` (Surface)
    
    New Properties:
        `self.collide_detect_used_image` (ndarray): in `change_image()` only if `collide_ignore_transparent` is True
    
    Changed Properties:
        `self.image` (Surface): in `change_image()`
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
        self.collide_ignore_transparent: bool = None
        self.already_scaled: bool = None
        assert(False, "you cannot init ImageProperty")

    def change_image(self) -> None:
        if type(self.image) is tuple:
            if self.collide_ignore_transparent:
                self.collide_detect_used_image = self.image[1]
            if self.already_scaled:
                self.image = self.image[0]
            else:
                self.image = self.game.it.transform.scale(
                    self.image[0], self.size
                )
        elif type(self.image) is Surface:
            if self.collide_ignore_transparent:
                assert(False, "Surface cannot support collide_ignore_transparent, try Tuple[Surface, ndarray] instead")
            if self.already_scaled:
                self.image = self.image
            else:
                self.image = self.game.it.transform.scale(
                    self.image, self.size
                )
        elif type(self.image) is str:
            if self.collide_ignore_transparent:
                self.collide_detect_used_image = mpimg.imread(self.image)
            self.image = self.game.it.image.load(self.image)
            if self.already_scaled:
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
    Add some methods and properties about position

    Required Properties:
        `game` (PyGame): define.PyGame
        `size` (tuple): (x_width, y_height), float number allowed
        `pos` (tuple): (x_pos, y_pos), float number allowed
        `align` (str): "center", "left-up", "left-down", "right-up", "right-down" to anchor with `pos`
        `image` (Surface): pygame.surface.Surface (recommend to use ImageProperty to get it)

        `original_image` (None): just make it None
    
    New Methods:
        `align_position()`: align self.image's position, generate self.collide_rect
        `resize(pos, size)`: change and align self.image and self.collide_rect's size and position
        `resize_collide_rect(pos, size)`: only change and align self.collide_rect's size and position
    
    New Properties:
        `self.pos_align` (tuple): in `align_position()`, `resize(pos, size)`
        `self.collide_rect` (Surface): in `align_position()`, `resize(pos, size)` and `resize_collide_rect(pos, size)`
    
    Changed Properties:
        `self.original_image` (Surface): in `resize(pos, size)`
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
        self.image: Surface = None
        self.original_image: Optional[Surface] = None
        assert(False, "you cannot init PositionProperty")

    def align_position(self) -> None:
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
        self.collide_rect = self.game.it.Rect(self.pos_align, self.size)

    def resize_collide_rect(self, pos: tuple, size: tuple) -> None:
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
        self.collide_rect = self.game.it.Rect(pos_align, size)
    
    def resize(self, pos: tuple, size: tuple) -> None:
        if self.original_image is None:
            self.original_image = self.image.copy()
        self.image = self.game.it.transform.scale(self.original_image, size)
        self.pos = pos
        self.size = size
        self.align_position()
