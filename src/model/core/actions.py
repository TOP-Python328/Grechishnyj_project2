__all__ = [
    'Feed', 
    'TeaseHead', 
    'ChaseTail', 
]


from pathlib import Path
from abc import ABC, abstractmethod
from core.parameters import Parameters, Creature


class Action(ABC):
    """Выполнение действия."""
    name: str

    def __init__(self, creature: 'Creature' = None):
        self.creature = creature

    def __hash__(self):
        return hash(self.name)

    @abstractmethod
    def do(self) -> None:
        pass


class PlayerAction(Action):
    """Выполнение действия игроком."""
    image: Path


class Feed(PlayerAction):
    """Выполнение действия игроком - покормить питомца."""
    name: str = 'Покормить'
    image: Path = Path() # 'path/image/feed'

    def __init__(
            self,
            amount: float,
            creature: Creature = None
    ):
        self.amount = amount
        super().__init__(creature)

    def do(self) -> None:
        """Выполненить действие - покормить."""
        self.creature.parameters[Parameters.Satiety].value += self.amount


class TeaseHead(PlayerAction):
    """Выполнение действия игроком - почесать голову питомцу."""
    name: str = 'Почесать голову'
    image: Path = Path() # 'path/image/feed'

    def do(self) -> None:
        """Выполненить действие - почесать голову питомцу."""
        ...


class CreatureAction(Action):
    """Выполнение действия питомцем."""

    def __init__(
            self, 
            rand_coeff: float,
            creature: 'Creature' = None,
    ):
        self.rand_coeff = rand_coeff
        super().__init__(creature)

class NoAction(Action):
    """Бездействие - заглушка."""
    name = 'No Action'

    def do(self) -> None:
        """Бездействует."""
        print(f'{self.name}')

class ChaseTail(CreatureAction):
    """Выполнение действия питомцем - погоня за хвостом."""
    name: str =  'погоня за хвостом'

    def do(self):
        """Выполненить действие - погоня за хвостом."""
        print(f'Event - {self.__doc__}')
