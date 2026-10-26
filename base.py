from typing import List, Dict, Type
from units import BaseUnit, UNIT_TYPES
from interfaces import IFieldObject
from game_field import GameField


class Base(IFieldObject):
    """База — строит юнитов, хранит ресурсы, размещается на поле."""

    def __init__(self, position, max_units: int = 10, resources: int = 100):
        self._position = position
        self._max_units = max_units
        self._resources = resources
        self._units: List[BaseUnit] = []
        self._symbol = "B"

    #Интерфейс IFieldObject
    def get_position(self):
        return self._position

    def get_symbol(self) -> str:
        return self._symbol

    # Свойства
    @property
    def resources(self) -> int:
        return self._resources

    @property
    def units(self) -> List[BaseUnit]:
        return self._units

    @property
    def units_count(self) -> int:
        return len(self._units)

    # Создание юнитов 
    def create_unit(self, unit_type_name: str, position) -> BaseUnit:
        """Создать юнита определённого типа."""
        if self.units_count >= self._max_units:
            print(f" Достигнут лимит юнитов ({self._max_units})!")
            return None

        if unit_type_name not in UNIT_TYPES:
            print(f"⚠ Неизвестный тип юнита: {unit_type_name}")
            return None

        unit_class: Type[BaseUnit] = UNIT_TYPES[unit_type_name]
        unit = unit_class(position)
        self._units.append(unit)
        print(f" Создан юнит: {unit.get_name()} на позиции {position}")
        return unit

    #Уничтожение юнита 
    def remove_unit(self, unit: BaseUnit) -> bool:
        """Удалить юнита (погиб или распущен)."""
        if unit in self._units:
            self._units.remove(unit)
            print(f" Юнит {unit.get_name()} удалён из базы.")
            return True
        return False

    # Состояние базы 
    def get_status(self) -> str:
        """Вывести состояние базы (как на рис. 5)."""
        lines = [
            f"Ресурсы базы: {self._resources}",
            f"Численность войска: {self.units_count} единиц",
            f"Максимум юнитов: {self._max_units}",
            "Список юнитов:"
        ]
        for i, unit in enumerate(self._units, 1):
            lines.append(f"  {i}. {unit}")
        return '\n'.join(lines)

    def __str__(self):
        return self.get_status()

    # base.py (добавить методы в класс Base)

    def save_game(self, filepath: str = "savegame.json"):
        """Сохранить состояние базы и счётчиков в JSON."""
        from instance_counter import InstanceCounter

        data = {
            "resources": self._resources,
            "max_units": self._max_units,
            "units_count": self.units_count,
            "position": list(self._position),
            "units": [
                {
                    "name": u.get_name(),
                    "health": u.get_health(),
                    "position": list(u.get_position()),
                    "symbol": u.get_symbol()
                }
                for u in self._units
            ],
            "counter_log": InstanceCounter.get_log(),
            "counter_count": InstanceCounter.get_count(),
            "counter_total": InstanceCounter.get_total_created()
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f" Игра сохранена в {filepath}")


    def load_game(self, filepath: str = "savegame.json"):
        """Загрузить состояние базы из JSON."""
        import json
        import os

        if not os.path.exists(filepath):
            print(f"⚠ Файл {filepath} не найден!")
            return False

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        self._resources = data["resources"]
        self._max_units = data["max_units"]
        self._position = tuple(data["position"])

        print(f" Игра загружена из {filepath}")
        print(f"   Ресурсы: {self._resources}")
        print(f"   Юнитов: {len(data['units'])}")
        print(f"   Счётчик: {data.get('counter_count', 0)} живых, {data.get('counter_total', 0)} всего")

        return True