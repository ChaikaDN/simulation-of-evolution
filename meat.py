from object import Object


class Meat(Object):
    def __init__(self, position):
        super().__init__(position)
        self.color = (200, 0, 0)
