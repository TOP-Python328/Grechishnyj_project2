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
            origin: 'Creature' = None
    ):
        self.__value = initial
        self.min = min
        self.max = max
        self.origin = origin

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

    # @abstractmethod
    def update(self) -> None:
        pass


class Health(Parameter):
    """Здоровье - параметр Tamagotchi."""
    name = 'Health'

    def update(self) -> None:
        """Обновление параметра."""

class Satiety(Parameter):
    """Сытость - параметр Tamagotchi."""
    name = 'Satiety'

    def update(self) -> None:
        """Обновление параметра."""

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



class MaturePhase:
    """Возрастной период питомца (фаза зрелости)."""
        
    def __init__(
            self,
            days: int,
            *parameters: Parameter
            # coeffs: dict = {}
    ):
        self.days = days
        self.parameters = parameters
        # self.coeffs = coeffs


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




class Creature:
    """Описывает питомца - игровое существо. Tamagotchi."""

    def __init__(
            self,
            kind: Kind,
            name: str,
    ):
        self.kind = kind
        self.name = name
        self.age: int = 0
        self.parameters: dict[Type, Parameter] = {}
        params = kind[0].parameters
        for param in params:
            key = Parameters[param.name].value
            cls = Parameters[param.name].value
            self.parameters[key] = cls(param.value,param.min,param.max,self)
            # print(param)
            # print(f'{Parameters[param.name].name = }')
            # print(f'{Parameters[param.name].value = }')
            # print(f'{cls = }')
        # for k, v in self.parameters.items():
        #     print(f'{k=} {v=} {v.__dict__}')
    
    def update(self) -> None:
        """Обновление всех параметров Tamagotchi."""



cube = Kind(
    'Кубик', 
    MaturePhase(
        5, 
        Parameters(Health).value(50, 75, 75),
        Parameters(Satiety).value(50, 75, 75),
        Parameters(Fatigue).value(50, 0, 100),
        Parameters(Hygiene).value(50, 0, 100),
        Parameters(Mood).value(50, 0, 100),
        Parameters(Stamina).value(50, 0, 100)
    ),
    MaturePhase(
        20,
        Parameters(Health).value(50, 75, 75),
        Parameters(Satiety).value(50, 75, 75),
        Parameters(Fatigue).value(50, 0, 100),
        Parameters(Hygiene).value(50, 0, 100),
        Parameters(Mood).value(50, 0, 100),
        Parameters(Stamina).value(50, 0, 100)
    ), 
    MaturePhase(
        50, 
        Parameters(Health).value(50, 75, 75),
        Parameters(Satiety).value(50, 75, 75),
        Parameters(Fatigue).value(50, 0, 100),
        Parameters(Hygiene).value(50, 0, 100),
        Parameters(Mood).value(50, 0, 100),
        Parameters(Stamina).value(50, 0, 100)
    )
)

yasha = Creature( 
    cube,
    'Yasha'
)

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





