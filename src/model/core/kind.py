

from dataclasses import dataclass
from typing import Type, Iterable
from random import sample, choice
from core.actions import PlayerAction, CreatureAction, NoAction
from core.parameters import *


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

    def random_action(self):
        """Случайное действие питомца."""
        action = choice(tuple(self.creature_actions))
        no_action = NoAction()
        prob = int(action.rand_coeff * 100)
        choice(sample([action, no_action], counts=[prob, 100-prob], k=100)).do()

# >>> for _ in range(20):
# ...     yasha.random_action()
# ...
# Event - Выполнение действия питомцем - погоня за хвостом.
# Event - Выполнение действия питомцем - погоня за хвостом.
# Event - Выполнение действия питомцем - погоня за хвостом.
# Event - Выполнение действия питомцем - погоня за хвостом.
# No Action
# Event - Выполнение действия питомцем - погоня за хвостом.
# No Action
# No Action
# Event - Выполнение действия питомцем - погоня за хвостом.
# Event - Выполнение действия питомцем - погоня за хвостом.
# No Action
# Event - Выполнение действия питомцем - погоня за хвостом.
# Event - Выполнение действия питомцем - погоня за хвостом.
# Event - Выполнение действия питомцем - погоня за хвостом.
# Event - Выполнение действия питомцем - погоня за хвостом.
# Event - Выполнение действия питомцем - погоня за хвостом.
# No Action
# No Action
# No Action
# No Action

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


