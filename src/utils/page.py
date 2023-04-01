from typing import Any
from pygame import event
from utils.define import PyGame, StateMachine


# wait for future use (refactor)
class Page:
    """
    inherit this.

    you may need to overload:
      init(), state_machine(), event_deal(event), control_flow()

    you may need to use inside:
      add_to_xxx(), del_xxx()

    you must use outside:
      show()
    """

    def __init__(self,  game: PyGame, state: StateMachine) -> None:
        self.game = game
        self.state = state
        self.inited = False
        self.stop = False
        self.__texture: list = []
        self.__bind: list = []

    def init(self):
        pass

    def state_machine(self):
        pass

    def event_deal(self, event: event.Event):
        pass

    def control_flow(self):
        pass

    def show(self):
        if not self.inited:
            self.__init()

        self.state_machine()

        if self.stop:
            return

        for event in self.game.it.event.get():
            if event.type == self.game.it.QUIT:
                self.state.quit = True
            for i in self.__bind:
                i.click_check(event)
            self.event_deal(event)

        self.control_flow()

        self.__render()

        self.game.render_update()
        self.game.clock.tick(60)

    def __init(self):
        self.__texture.clear()
        self.__bind.clear()
        self.init()
        self.inited = True

    def del_render_list(self, __object: Any) -> Any:
        self.__texture.remove(__object)

    def add_to_render_list(self, __object: Any) -> None:
        '''
        __object should have method .render()
        '''
        self.__texture.append(__object)

    def del_click_list(self, __object) -> Any:
        self.__bind.remove(__object)

    def add_to_click_list(self, __object) -> Any:
        '''
        __object should have method .click_check(event)
        '''
        self.__bind.append(__object)

    def __render(self):
        for i in self.__texture:
            i.render()
