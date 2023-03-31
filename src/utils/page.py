from utils.define import PyGame, StateMachine
from typing import Any

# wait for future use (refactor)
class Page:
    """
    inherit this.

    you need to overload:
      init(), control_flow()

    you may need to use inside:
      add_to_xxx(), del_xxx()
    
    you must use outside:
      show()
    """
    
    def __init__(self,  game: PyGame, state: StateMachine) -> None:
        self.game = game
        self.state = state
        self.__inited = False
        self.__texture: list = []
        self.__bind: list = []
    
    def init(self):
        pass

    def control_flow(self):
        pass

    def show(self):
        if not self.__inited:
            self.__init()
        
        for event in self.game.it.event.get():
            if event.type == self.game.it.QUIT:
                self.state.quit = True
            for i in self.__bind:
                i.click_check(event)

        self.control_flow()

        self.__render()

        self.game.render_update()
        self.game.clock.tick(60)

    def __init(self):
        self.__inited = True
        self.init()

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
