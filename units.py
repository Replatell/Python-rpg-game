from interfaces import IUnit
from typing import Tuple
from instance_counter import InstanceCounter


class BaseUnit(IUnit):
    """Базовая реализация юнита с общими характеристиками."""

    def __init__(self, name: str, health: int, attack: int, armor: int,
                 position: Tuple[int, int], symbol: str):
        self._name = name
        self._health = health
        self._max_health = health
        self._attack = attack
        self._armor = armor
        self._position = position
        self._symbol = symbol
        self._counter = InstanceCounter(name=name)

    #Реализация методов интерфейса 
    def get_name(self) -> str:
        return self._name

    def get_health(self) -> int:
        return self._health

    def get_attack(self) -> int:
        return self._attack

    def get_armor(self) -> int:
        return self._armor

    def get_position(self) -> Tuple[int, int]:
        return self._position

    def get_symbol(self) -> str:
        return self._symbol

    def move(self, new_position: Tuple[int, int]) -> None:
        self._position = new_position

    def take_damage(self, damage: int) -> None:
        real_damage = max(0, damage - self._armor)
        self._health -= real_damage
        if self._health < 0:
            self._health = 0

    def is_alive(self) -> bool:
        return self._health > 0

    def __str__(self):
        status = "жив" if self.is_alive() else "мёртв"
        return f"{self._name} [HP:{self._health}/{self._max_health}] ({status})"


#ПЕХОТА 
class Swordsman(BaseUnit):
    """Мечник — пехота ближнего боя."""
    def __init__(self, position: Tuple[int, int]):
        super().__init__(
            name="Мечник", health=100, attack=15, armor=5,
            position=position, symbol="M"
        )


class Spearman(BaseUnit):
    """Копейщик — пехота с защитой от конницы."""
    def __init__(self, position: Tuple[int, int]):
        super().__init__(
            name="Копейщик", health=80, attack=12, armor=8,
            position=position, symbol="S"
        )


#ЛУЧНИКИ
class Archer(BaseUnit):
    """Лучник — дальний бой, малая броня."""
    def __init__(self, position: Tuple[int, int]):
        super().__init__(
            name="Лучник", health=60, attack=18, armor=2,
            position=position, symbol="A"
        )


class Arbalester(BaseUnit):
    """Арбалетчик — мощный дальний бой."""
    def __init__(self, position: Tuple[int, int]):
        super().__init__(
            name="Арбалетчик", health=70, attack=22, armor=3,
            position=position, symbol="Z"
        )


#КОННИЦА / МАГИ 
class Magician(BaseUnit):
    """Маг — магическая атака, слабое здоровье."""
    def __init__(self, position: Tuple[int, int]):
        super().__init__(
            name="Маг", health=50, attack=25, armor=1,
            position=position, symbol="G"
        )


class Healer(BaseUnit):
    """Целитель — лечит союзников."""
    def __init__(self, position: Tuple[int, int]):
        super().__init__(
            name="Целитель", health=55, attack=5, armor=2,
            position=position, symbol="H"
        )

    def heal(self, target: BaseUnit, amount: int = 20) -> None:
        """Лечит целевого юнита."""
        if target.is_alive():
            target._health = min(target._max_health, target._health + amount)
            print(f"{self._name} лечит {target.get_name()} на {amount} HP.")


# Фабрика юнитов 
UNIT_TYPES = {
    "Мечник": Swordsman,
    "Копейщик": Spearman,
    "Лучник": Archer,
    "Арбалетчик": Arbalester,
    "Маг": Magician,
    "Целитель": Healer,
}

def __del__(self):
        """При уничтожении юнита — уничтожаем и счётчик."""
        if hasattr(self, '_counter'):
            del self._counter