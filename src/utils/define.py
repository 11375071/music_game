import os
import yaml
import pygame
from yaml.loader import SafeLoader
from typing import Callable, Optional, Dict, Any


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


class StaticData:
    def __init__(self, root: str, save_name: str) -> None:
        self.root = root
        if not os.path.exists(root):
            os.makedirs(root)
        self.save_name = save_name
        self.path = os.path.join(root, save_name)
        self.dict = {}
    
    def __setitem__(self, key: str, value):
        self.dict[key] = value
        self.save()

    def setdefault(self, key: str, default = None):
        res = self.dict.setdefault(key, default)
        self.save()
        return res
    
    def __getitem__(self, name: str):
        return self.setdefault(name)

    def save(self, specify_path: str = None):
        file_name = self.path if specify_path is None else specify_path
        with open(file_name, 'w') as outfile:
            yaml.dump(self.dict, outfile, default_flow_style=False, allow_unicode=True)
    
    def load(self, specify_path: str = None):
        file_name = self.path if specify_path is None else specify_path
        if os.path.isfile(file_name):
            with open(file_name, 'r') as outfile:
                self.dict = yaml.load(outfile, Loader=SafeLoader)
                if type(self.dict) is not dict:
                    self.dict = {}
        else:
            self.dict = {}



class StateMachine:
    def __init__(self, init_state: str) -> None:
        self.state: str = init_state
        self.quit: bool = False
        self.__data_dict: Dict[str, StaticData] = {}

    def __setitem__(self, name: str, data: StaticData):
        self.__data_dict[name] = data

    def __getitem__(self, name: str) -> StaticData:
        return self.__data_dict[name]

    def __eq__(self, argument: str) -> bool:
        return self.state == argument
