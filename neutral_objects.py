from abc import ABC, abstractmethod
from typing import Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from units import BaseUnit


class INeutralObject(ABC):
    """Интерфейс нейтрального объекта на поле."""

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_symbol(self) -> str:
        pass

    @abstractmethod
    def get_position(self) -> Tuple[int, int]:
        pass

    @abstractmethod
    def interact(self, unit: 'BaseUnit') -> str:
        """Взаимодействие с юнитом. Возвращает описание результата."""
        pass


class TreasureChest(INeutralObject):
    """Сундук с сокровищами — даёт золото."""

    def __init__(self, position: Tuple[int, int], gold: int = 50):
        self._position = position
        self._gold = gold
        self._opened = False

    def get_name(self) -> str: return "Сундук"
    def get_symbol(self) -> str: return "C"
    def get_position(self) -> Tuple[int, int]: return self._position

    def interact(self, unit: 'BaseUnit') -> str:
        if self._opened:
            return "Сундук уже открыт и пуст."
        self._opened = True
        return f"{unit.get_name()} открыл сундук и получил {self._gold} золота!"

    # Перегрузка оператора + : юнит + сундук = взаимодействие
    def __add__(self, unit: 'BaseUnit') -> str:
        return self.interact(unit)


class HealingFountain(INeutralObject):
    """Целебный фонтан — восстанавливает HP."""

    def __init__(self, position: Tuple[int, int], heal_amount: int = 30):
        self._position = position
        self._heal_amount = heal_amount

    def get_name(self) -> str: return "Фонтан"
    def get_symbol(self) -> str: return "F"
    def get_position(self) -> Tuple[int, int]: return self._position

    def interact(self, unit: 'BaseUnit') -> str:
        unit.take_damage(-self._heal_amount)  # отрицательный урон = лечение
        return f"{unit.get_name()} выпил из фонтана и восстановил {self._heal_amount} HP!"

    def __add__(self, unit: 'BaseUnit') -> str:
        return self.interact(unit)


class Trap(INeutralObject):
    """Ловушка — наносит урон."""

    def __init__(self, position: Tuple[int, int], damage: int = 25):
        self._position = position
        self._damage = damage
        self._triggered = False

    def get_name(self) -> str: return "Ловушка"
    def get_symbol(self) -> str: return "T"
    def get_position(self) -> Tuple[int, int]: return self._position

    def interact(self, unit: 'BaseUnit') -> str:
        if self._triggered:
            return "Ловушка уже сработала."
        self._triggered = True
        unit.take_damage(self._damage)
        return f"{unit.get_name()} наступил на ловушку и получил {self._damage} урона!"

    def __add__(self, unit: 'BaseUnit') -> str:
        return self.interact(unit)


class Merchant(INeutralObject):
    """Торговец — продаёт улучшения."""

    def __init__(self, position: Tuple[int, int]):
        self._position = position
        self._visited = False

    def get_name(self) -> str: return "Торговец"
    def get_symbol(self) -> str: return "$"
    def get_position(self) -> Tuple[int, int]: return self._position

    def interact(self, unit: 'BaseUnit') -> str:
        if self._visited:
            return "Торговец уже обслужил этого юнита."
        self._visited = True
        unit._attack += 5  # временное усиление
        return f"{unit.get_name()} купил у торговца оружие (+5 к атаке)!"

    def __add__(self, unit: 'BaseUnit') -> str:
        return self.interact(unit)


# Фабрика нейтральных объектов
NEUTRAL_TYPES = {
    "Сундук": TreasureChest,
    "Фонтан": HealingFountain,
    "Ловушка": Trap,
    "Торговец": Merchant,
}