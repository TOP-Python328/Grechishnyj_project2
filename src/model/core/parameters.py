__all__ = [
    'Parameters', 
    'Parameter',
    'Health', 
    'Satiety', 
    'Fatigue',
    'Hygiene',
    'Mood',
    'Stamina'
]

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from functools import cached_property

# переменные для аннотаций
Creature = None


class Parameter:
    """Параметр питомца(существа)"""
    name: str = None
    
    def __init__(
            self,
            initial: float, 
            min: float, 
            max: float,  
            creature: Creature = None
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