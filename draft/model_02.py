"""Model (MVC)."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Type, Iterable
from functools import cached_property
from pathlib import Path


# DictOfRanges: dict[tuple[int, int], Any]
class DictOfRanges(dict):
    """Словарь диапазонов для возрастных периодов."""
    def __init__(self, mappable: dict):
        for key in mappable:
            if (
                not isinstance(key, tuple)
                or len(key) != 2
                or not isinstance(key[0], int)
                or not isinstance(key[1], int)
            ):
                raise ValueError('Invalid data type.')
        super().__init__(mappable)
    
    def __getitem__(self, key):
        if isinstance(key, int):
            for left, right in self:
                if left <= key <= right:
                    return super().__getitem__((left, right))
        else:
            return super().__getitem__(key)
    

# observer
class Parameter:
    """Параметр питомца(существа)"""
    name: str = None
    
    def __init__(
            self,
            initial: float, 
            min: float, 
            max: float,  
            creature: 'Creature' = None
    ):
        self.__value = initial
        self._min = min
        self._max = max
        self.creature = creature

    @property
    def value(self) -> float:
        return self.__value
    
    @cached_property
    def range(self) -> tuple[float, float]:
        return (self._min, self._max)

    @value.setter
    def value(self, new_value: float) -> None: 
        if new_value <= self._min:
            self.__value = self._min
        elif self._max <= new_value:
            self.__value = self._max
        else:
            self.__value = new_value

    @abstractmethod
    def update(self) -> None:
        pass


class Health(Parameter):
    """Здоровье - параметр Tamagotchi."""
    name = 'Health'

    def update(self) -> None:
        """Обновление параметра."""
        satiety = self.creature.parameters[Satiety]
        critcal = sum(satiety.range) / 4
        if 0 < satiety.value < critcal:
            self.value -= 1
        elif satiety.value == 0:
            self.value -= 2


class Satiety(Parameter):
    """Сытость - параметр Tamagotchi."""
    name = 'Satiety'

    def update(self) -> None:
        """Обновление параметра."""
        self.value -= 1

class Fatigue(Parameter):
    """Усталость - параметр Tamagotchi."""
    name = 'Fatigue'

    def update(self) -> None:
        """Обновление параметра."""

class Hygiene(Parameter):
    """Чистота - параметр Tamagotchi."""
    name = 'Hygiene'

    def update(self) -> None:
        """Обновление параметра."""

class Mood(Parameter):
    """Настроение - параметр Tamagotchi."""
    name = 'Mood'

    def update(self) -> None:
        """Обновление параметра."""

class Stamina(Parameter):
    """Выносливость - параметр Tamagotchi."""
    name = 'Stamina'

    def update(self) -> None:
        """Обновление параметра."""






# class Parameters(Enum):
#     HEALTH = Health
#     SATIETY = Satiety
Parameters = Enum(
    'Parameters', 
    {
        cls.__name__: cls
        for cls in Parameter.__subclasses__()
    }
)
# >>> Parameters
# <enum 'Parameters'>
# >>> list(Parameters)
# [<Parameters.Health: <class '__main__.Health'>>, 
#  <Parameters.Satiety: <class '__main__.Satiety'>>, 
#  <Parameters.Fatigue: <class '__main__.Fatigue'>>, 
#  <Parameters.Hygiene: <class '__main__.Hygiene'>>, 
#  <Parameters.Mood: <class '__main__.Mood'>>, 
#  <Parameters.Disease: <class '__main__.Disease'>>, 
#  <Parameters.Stamina: <class '__main__.Stamina'>>]
# >>>
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
            creature: 'Creature' = None
    ):
        self.amount = amount
        super().__init__(creature)

    def do(self) -> None:
        """Выполненить действие - покормить."""
        self.creature.parameters[Satiety].value += self.amount


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


class ChaseTail(CreatureAction):
    """Выполнение действия питомцем - погоня за хвостом."""
    name: str =  'погоня за хвостом'

    def do(self):
        """Выполненить действие - погоня за хвостом."""
        ...



class MaturePhase:
    """Возрастной период питомца (фаза зрелости)."""
        
    def __init__(
            self,
            days: int,
            *parameters: Parameter,
            player_actions: Iterable[PlayerAction],
            creature_actions: Iterable[CreatureAction]
            # coeffs: dict = {}
    ):
        self.days = days
        self.parameters = tuple(parameters)
        self.player_actions = tuple(player_actions)
        self.creature_actions = tuple(creature_actions)
        # self.coeffs = coeffs

# >>> mf = MaturePhase(5, None)
# >>> mf
# <__main__.MaturePhase object at 0x000001D15E7078D0>
# >>> MaturePhase.__mro__
# (<class '__main__.MaturePhase'>, <class 'object'>)
# >>> mf.__dict__
# {'days': 5, 'parameters': (None,)}       

# Реализовать хранение информации о виде в файле!!!
class Kind(DictOfRanges):
    """Описывает вид существа с характерными для него параметрами."""

    def __init__(
            self, 
            name: str, 
            *mature_phases: MaturePhase
    ):
        self.name: str = name
        left = 0
        phases = {}
        for phase in mature_phases:
            key_range = left, left + phase.days - 1
            phases[key_range] = phase
            left += phase.days
        super().__init__(phases)
        
# >>> cat = Kind(
# ...     'кот',
# ...     MaturePhase(5, None),
# ...     MaturePhase(15, None),
# ...     MaturePhase(35, None),
# ...     MaturePhase(55, None),
# ...     MaturePhase(75, None)
# ... )
# >>>
# >>> cat
# {
#     (0, 4): <__main__.MaturePhase object at 0x000002C810C07050>, 
#     (5, 19): <__main__.MaturePhase object at 0x000002C810F73290>, 
#     (20, 54): <__main__.MaturePhase object at 0x000002C810F73190>, 
#     (55, 109): <__main__.MaturePhase object at 0x000002C810F73250>, 
#     (110, 184): <__main__.MaturePhase object at 0x000002C810F730D0>
# }

    
# memento -> originator(class Creature)
@dataclass
class State:
    """Состояние питомца."""
    age: int
    # param1: None

    def __repr__(self):
        return '/'.join(f'{param}={value}' for param, value in self.__dict__.items())


# caretaker -> опекун для State
class History(list):
    """История состояний питомца."""

    def get_param(self, parameter: Type) -> list[float]:
        """История изменений отдельного параметра."""
        return [getattr(state, parameter.__name__) for state in self]

# >>> yasha
# Кубик Yasha 0
#         Health 50.00
#         Satiety 50.00
#         Fatigue 50.00
#         Hygiene 50.00
#         Mood 50.00
#         Stamina 50.00
# >>>
# >>> yasha.history
# []
# >>>
# >>> yasha.update()
# >>> yasha.update()
# >>> yasha.update()
# >>>
# >>> yasha.history
# [State(age=0), State(age=0), State(age=0)]
# >>>
# >>> yasha.age = 5
# >>> yasha.update()
# >>> yasha.history
# [State(age=0), State(age=0), State(age=0), State(age=5)]
# >>>
# >>> yasha.history[0].__dict__
# {'age': 5, 'Health': 50, 'Satiety': 49, 'Fatigue': 50, 'Hygiene': 50, 'Mood': 50, 'Stamina': 50}
# >>> yasha.history[len(yasha.history) - 1].__dict__
# {'age': 5, 'Health': 50, 'Satiety': 35, 'Fatigue': 50, 'Hygiene': 50, 'Mood': 50, 'Stamina': 50}
# >>>
# >>> yasha.history.get_param_history(Health)
# [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50]
# >>> yasha.history.get_param(Satiety)
# [49, 48, 47, 46, 45, 44, 43, 42, 41, 40, 39, 38, 37, 36, 35]
# >>>


# originator
class Creature:
    """Описывает питомца - игровое существо. Tamagotchi."""

    def __init__(self, kind: Kind, name: str,):
        self.kind = kind
        self.name = name
        self.__age: int = 0
        self.parameters: dict[Type, Parameter] = {}
        params = kind[0].parameters
        for param in params:
            cls = Parameters[param.name].value
            self.parameters[cls] = cls(param.value, param._min, param._max, self)
        self.player_actions: set[PlayerAction]
        self.creature_actions: set[CreatureAction] 
        self.__set_actions()
        self.history: History = History()

    def __set_actions(self) -> None:
        self.player_actions = {
            action.__class__(**{**action.__dict__, 'creature': self})
            for action in self.kind[self.age].player_actions
        }
        self.creature_actions = {
            action.__class__(**{**action.__dict__, 'creature': self})
            for action in self.kind[self.age].creature_actions
        }
    
    def update(self) -> None:
        """Обновление всех параметров Tamagotchi."""
        for parameter in self.parameters.values():
            parameter.update()
        self.save()

    @property
    def age(self) -> int:
        return self.__age
    
    @age.setter
    def age(self, new_age: int):
        isgrow = self.kind[self.__age] is not self.kind[new_age]
        self.__age = new_age
        if isgrow:
            self._grow_up()
            # print(self.kind[self.__age])     
        # else:
        #     ...

    def _grow_up(self) -> None:
        """Изменение возрастного периода питомца - взросление."""
        for param in self.kind[self.age].parameters:
            cls = Parameters[param.name].value
            value = param.value or self.parameters[cls].value
            self.parameters[cls] = cls(value, param._min, param._max, self)
        self.__set_actions()

    def save(self) -> State:
        """Сохранение состояния питомца."""
        state = State(self.age)
        for cls, parameter in self.parameters.items():
            setattr(state, cls.__name__, parameter.value)
        self.history.append(state)
        return state

    def __repr__(self):
        title = f'{self.kind.name} {self.name} {self.age}'
        params = '\n'.join(f'\t{p.name} {p.value:.2f}' for p in self.parameters.values())
        return f'{title}\n{params}'

# >>> yasha
# Кубик Yasha 0
#         Health 50.00
#         Satiety 50.00
#         Fatigue 50.00
#         Hygiene 50.00
#         Mood 50.00
#         Stamina 50.00
# >>> yasha.parameters[Health].range
# (0, 50)
# >>>
# >>> yasha.age = 6
# <__main__.MaturePhase object at 0x0000028FF0DD0350>
# >>> yasha
# Кубик Yasha 6
#         Health 50.00
#         Satiety 50.00
#         Fatigue 50.00
#         Hygiene 50.00
#         Mood 50.00
#         Stamina 50.00
# >>> yasha.parameters[Health].range
# (0, 75)
# >>>
# >>> yasha.age = 55
# <__main__.MaturePhase object at 0x0000028FF0DD0510>
# >>> yasha
# Кубик Yasha 55
#         Health 50.00
#         Satiety 50.00
#         Fatigue 50.00
#         Hygiene 50.00
#         Mood 50.00
#         Stamina 50.00
# >>> yasha.parameters[Health].range
# (0, 100)
# >>>



cube = Kind(
    'Кубик', 
    MaturePhase(
        5, 
        Parameters(Health).value(50, 0, 50),
        Parameters(Satiety).value(50, 0, 50),
        Parameters(Fatigue).value(50, 0, 50),
        Parameters(Hygiene).value(50, 0, 50),
        Parameters(Mood).value(50, 0, 50),
        Parameters(Stamina).value(50, 0, 50),
        player_actions=[
            Feed(3)
        ],
        creature_actions=[
            ChaseTail(0.7),
        ]
    ),
    MaturePhase(
        20,
        Parameters(Health).value(0, 0, 75),
        Parameters(Satiety).value(0, 0, 75),
        Parameters(Fatigue).value(0, 0, 75),
        Parameters(Hygiene).value(0, 0, 75),
        Parameters(Mood).value(0, 0, 75),
        Parameters(Stamina).value(0, 0, 75),
        player_actions=[
            Feed(5)
        ],
        creature_actions=[
            ChaseTail(0.1),
        ]
    ), 
    MaturePhase(
        50, 
        Parameters(Health).value(0, 0, 100),
        Parameters(Satiety).value(0, 0, 100),
        Parameters(Fatigue).value(0, 0, 100),
        Parameters(Hygiene).value(0, 0, 100),
        Parameters(Mood).value(0, 0, 100),
        Parameters(Stamina).value(0, 0, 100),
        player_actions=[
            Feed(7)
        ],
        creature_actions=[]
    )
)

# >>> m = Parameters(Mood)
# >>> m.value
# <class '__main__.Mood'>
# >>> m.value()
# ...
# TypeError: Parameter.__init__() missing 3 required positional arguments: 'initial', 'min', and 'max'

yasha = Creature(cube,'Yasha')

buttons = [
    action.do
    for action in yasha.player_actions
]

# >>> yasha.kind
# {
#     (0, 4): <__main__.MaturePhase object at 0x000001D6CE54F610>, 
#     (5, 24): <__main__.MaturePhase object at 0x000001D6CE54F7D0>, 
#     (25, 74): <__main__.MaturePhase object at 0x000001D6CE54F990>
# }


# >>> yasha.parameters
# {
    # <class '__main__.Health'>: <__main__.Health object at 0x000001D6CE54FA90>, 
    # <class '__main__.Satiety'>: <__main__.Satiety object at 0x000001D6CE54FAD0>, 
    # <class '__main__.Fatigue'>: <__main__.Fatigue object at 0x000001D6CE54FB10>, 
    # <class '__main__.Hygiene'>: <__main__.Hygiene object at 0x000001D6CE54FB50>, 
    # <class '__main__.Mood'>: <__main__.Mood object at 0x000001D6CE54FB90>, 
    # <class '__main__.Stamina'>: <__main__.Stamina object at 0x000001D6CE54FBD0>
# }

# >>> yasha.player_actions
# {<__main__.Feed object at 0x00000189FF926FD0>}
# >>> yasha.creature_actions
# {<__main__.ChaseTail object at 0x00000189FF927010>}
# >>> tuple(yasha.player_actions)[0].creature
# Кубик Yasha 0
#         Health 50.00
#         Satiety 50.00
#         Fatigue 50.00
#         Hygiene 50.00
#         Mood 50.00
#         Stamina 50.00
# >>> tuple(yasha.creature_actions)[0].creature
# Кубик Yasha 0
#         Health 50.00
#         Satiety 50.00
#         Fatigue 50.00
#         Hygiene 50.00
#         Mood 50.00
#         Stamina 50.00
# >>>



# >>> yasha
# Кубик Yasha 0
#         Health 50.00
#         Satiety 50.00
#         Fatigue 50.00
#         Hygiene 50.00
#         Mood 50.00
#         Stamina 50.00
# >>>
# >>> for _ in range(20):
# ...     yasha.update()
# ...
# >>> yasha
# Кубик Yasha 0
#         Health 50.00
#         Satiety 30.00
#         Fatigue 50.00
#         Hygiene 50.00
#         Mood 50.00
#         Stamina 50.00
# >>>
# >>> buttons
# [<bound method Feed.do of <__main__.Feed object at 0x000001DB7F4CAFD0>>]
# >>> buttons[0]()
# >>>
# >>> yasha
# Кубик Yasha 0
#         Health 50.00
#         Satiety 33.00
#         Fatigue 50.00
#         Hygiene 50.00
#         Mood 50.00
#         Stamina 50.00
# >>>
# >>> yasha.age = 10
# >>> yasha
# Кубик Yasha 10
#         Health 50.00
#         Satiety 33.00
#         Fatigue 50.00
#         Hygiene 50.00
#         Mood 50.00
#         Stamina 50.00
# >>>
# >>> for _ in range(20):
# ...     yasha.update()
# ...
# >>> yasha
# Кубик Yasha 10
#         Health 45.00
#         Satiety 13.00
#         Fatigue 50.00
#         Hygiene 50.00
#         Mood 50.00
#         Stamina 50.00
# >>>
# >>> buttons[0]()
# >>>
# >>> yasha
# Кубик Yasha 10
#         Health 45.00
#         Satiety 16.00
#         Fatigue 50.00
#         Hygiene 50.00
#         Mood 50.00
#         Stamina 50.00
# >>>
# >>> buttons = [
# ...     action.do
# ...     for action in yasha.player_actions
# ... ]
# >>>
# >>> buttons[0]()
# >>>
# >>> yasha
# Кубик Yasha 10
#         Health 45.00
#         Satiety 21.00
#         Fatigue 50.00
#         Hygiene 50.00
#         Mood 50.00
#         Stamina 50.00
# >>> buttons[0]()
# >>> buttons[0]()
# >>> buttons[0]()
# >>> buttons[0]()
# >>> buttons[0]()
# >>> buttons[0]()
# >>> buttons[0]()
# >>> buttons[0]()
# >>> buttons[0]()
# >>> buttons[0]()
# >>> buttons[0]()
# >>> buttons[0]()
# >>> buttons[0]()
# >>> buttons[0]()
# >>> yasha
# Кубик Yasha 10
#         Health 45.00
#         Satiety 75.00
#         Fatigue 50.00
#         Hygiene 50.00
#         Mood 50.00
#         Stamina 50.00
# >>>





