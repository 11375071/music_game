import pygame
from typing import Callable, Optional


class PyGame:
    def __init__(self, width: int, height: int) -> None:
        self.__size = width, height
        pygame.init()
        self.__surface = pygame.display.set_mode(self.__size)
        self.__alpha_surface = self.__surface.convert_alpha()
        self.__alpha_surface.fill([0, 0, 0, 0])
        self.clock = pygame.time.Clock()

    @property
    def size(self) -> tuple:
        return self.__size

    @property
    def screen(self) -> pygame.Surface:
        return self.__alpha_surface
    
    @property
    def it(self) -> pygame:
        return pygame
    
    def render_update(self):
        self.__surface.blit(self.__alpha_surface, (0, 0))
        pygame.display.flip()


class StateMachine:
    def __init__(self, init_state: str) -> None:
        self.state: str = init_state
        self.quit: bool = False
        self.sub_page_dict: dict = {}
        self.mother_render_dict: dict = {}

        # settings
        self.speed: int = 10
        self.offset: int = -40

    def __eq__(self, argument: str) -> bool:
        return self.state == argument

    @property
    def sub_page(self) -> str:
        return self.sub_page_dict.setdefault(self.state, None)
    
    @sub_page.setter
    def sub_page(self, sub_page_name: str):
        self.sub_page_dict[self.state] = sub_page_name
    
    @property
    def mother_render(self) -> Optional[Callable]:
        return self.mother_render_dict.setdefault(self.state, None)
    
    @mother_render.setter
    def mother_render(self, mother_render_func: Optional[Callable]):
        self.mother_render_dict[self.state] = mother_render_func

    def specify_mother_render(self, state_name: str) -> Optional[Callable]:
        return self.mother_render_dict.setdefault(state_name, None)
    
    def set_specify_mother_render(self, state_name: str, mother_render_func: str):
        self.mother_render_dict[state_name] = mother_render_func

    def specify_sub_page(self, state_name: str) -> str:
        return self.sub_page_dict.setdefault(state_name, None)
    
    def set_specify_sub_page(self, state_name: str, sub_page_name: str):
        self.sub_page_dict[state_name] = sub_page_name