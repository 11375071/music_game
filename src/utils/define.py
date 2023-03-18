import pygame


class PyGame:
    def __init__(self, width: int, height: int) -> None:
        self.size = width, height
        pygame.init()
        self.surface = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

    @property
    def screen(self) -> pygame.Surface:
        return self.surface

    @property
    def it(self) -> pygame:
        return pygame


class StateMachine:
    def __init__(self, init_state) -> None:
        self.state = init_state
        self.quit = False

    def __eq__(self, argument) -> bool:
        return self.state == argument
