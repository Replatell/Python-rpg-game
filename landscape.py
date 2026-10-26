from abc import ABC, abstractmethod
from typing import Tuple


class ILandscape(ABC):
    """Интерфейс ландшафта."""

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_symbol(self) -> str:
        """Символ для отображения на карте."""
        pass

    @abstractmethod
    def get_move_modifier(self) -> float:
        """Множитель скорости перемещения (1.0 = норма)."""
        pass

    @abstractmethod
    def get_attack_modifier(self) -> float:
        """Множитель атаки для юнита на этом ландшафте."""
        pass

    @abstractmethod
    def can_unit_enter(self, unit_type: str) -> bool:
        """Может ли юнит данного типа войти на эту клетку."""
        pass


class Grass(ILandscape):
    """Трава — обычный ландшафт, без модификаторов."""
    def get_name(self) -> str: return "Трава"
    def get_symbol(self) -> str: return "."
    def get_move_modifier(self) -> float: return 1.0
    def get_attack_modifier(self) -> float: return 1.0
    def can_unit_enter(self, unit_type: str) -> bool: return True


class Forest(ILandscape):
    """Лес — замедляет, но даёт бонус к защите."""
    def get_name(self) -> str: return "Лес"
    def get_symbol(self) -> str: return "♣"
    def get_move_modifier(self) -> float: return 0.5
    def get_attack_modifier(self) -> float: return 0.8
    def can_unit_enter(self, unit_type: str) -> bool: return True


class Mountain(ILandscape):
    """Горы — труднопроходимы, только для некоторых юнитов."""
    def get_name(self) -> str: return "Горы"
    def get_symbol(self) -> str: return "^"
    def get_move_modifier(self) -> float: return 0.3
    def get_attack_modifier(self) -> float: return 1.2
    def can_unit_enter(self, unit_type: str) -> bool:
        # Конница и маги не могут ходить по горам
        return unit_type not in ("Конница", "Маг")


class Water(ILandscape):
    """Вода — непроходима для большинства."""
    def get_name(self) -> str: return "Вода"
    def get_symbol(self) -> str: return "~"
    def get_move_modifier(self) -> float: return 0.0
    def get_attack_modifier(self) -> float: return 1.0
    def can_unit_enter(self, unit_type: str) -> bool: return False


# Фабрика ландшафтов
LANDSCAPE_TYPES = {
    "Трава": Grass,
    "Лес": Forest,
    "Горы": Mountain,
    "Вода": Water,
}