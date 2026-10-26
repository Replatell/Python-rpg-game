from abc import ABC, abstractmethod
from typing import Tuple


class IUnit(ABC):
    """Интерфейс юнита — общий для всех типов войск."""

    @abstractmethod
    def get_name(self) -> str:
        """Возвращает название юнита."""
        pass

    @abstractmethod
    def get_health(self) -> int:
        """Возвращает текущее здоровье."""
        pass

    @abstractmethod
    def get_attack(self) -> int:
        """Возвращает силу атаки."""
        pass

    @abstractmethod
    def get_armor(self) -> int:
        """Возвращает значение брони."""
        pass

    @abstractmethod
    def get_position(self) -> Tuple[int, int]:
        """Возвращает координаты (x, y) на поле."""
        pass

    @abstractmethod
    def move(self, new_position: Tuple[int, int]) -> None:
        """Перемещает юнита на новую позицию."""
        pass

    @abstractmethod
    def take_damage(self, damage: int) -> None:
        """Получить урон."""
        pass

    @abstractmethod
    def is_alive(self) -> bool:
        """Проверяет, жив ли юнит."""
        pass

    @abstractmethod
    def get_symbol(self) -> str:
        """Символ для отображения на карте."""
        pass


class IFieldObject(ABC):
    """Интерфейс любого объекта на игровом поле."""

    @abstractmethod
    def get_position(self) -> Tuple[int, int]:
        pass

    @abstractmethod
    def get_symbol(self) -> str:
        pass