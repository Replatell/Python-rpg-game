from interfaces import IFieldObject
from typing import List, Tuple, Optional
import copy


class GameField:
    """Игровое поле — контейнер для объектов на прямоугольной сетке."""

    def __init__(self, width: int = 20, height: int = 20, max_objects: int = 50, landscape_grid=None):
        self._width = width
        self._height = height
        self._max_objects = max_objects
        self._objects: List[IFieldObject] = []
        self._landscape_grid = landscape_grid

    #Свойства 
    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def objects_count(self) -> int:
        return len(self._objects)

    #Управление объектами 
    def add_object(self, obj: IFieldObject) -> bool:
        """Добавить объект на поле. Возвращает True если успешно."""
        if len(self._objects) >= self._max_objects:
            print(f"⚠ Превышен лимит объектов ({self._max_objects})!")
            return False

        x, y = obj.get_position()
        if not (0 <= x < self._width and 0 <= y < self._height):
            print(f" Позиция ({x},{y}) вне поля!")
            return False

        #Проверка: не занято ли место
        for existing in self._objects:
            if existing.get_position() == obj.get_position():
                print(f" Позиция ({x},{y}) уже занята!")
                return False

        self._objects.append(obj)
        return True

    def remove_object(self, obj: IFieldObject) -> bool:
        """Удалить объект с поля."""
        if obj in self._objects:
            self._objects.remove(obj)
            return True
        return False

    def get_object_at(self, position: Tuple[int, int]) -> Optional[IFieldObject]:
        """Получить объект по координатам."""
        for obj in self._objects:
            if obj.get_position() == position:
                return obj
        return None

    def copy(self) -> 'GameField':
        """Создать копию поля со всеми объектами."""
        new_field = GameField(self._width, self._height, self._max_objects)
        new_field._objects = copy.deepcopy(self._objects)
        return new_field

    #Отображение
    def render(self) -> str:
        """Отрисовать поле в виде строки (для консоли)."""
        # Создаём сетку из ландшафта (если есть) или пустую
        if self._landscape_grid:
            grid = [[self._landscape_grid[y][x].get_symbol() 
                     for x in range(self._width)] 
                    for y in range(self._height)]
        else:
            grid = [['.' for _ in range(self._width)] for _ in range(self._height)]

        # Расставляем границы
        for x in range(self._width):
            grid[0][x] = 'X'
            grid[self._height - 1][x] = 'X'
        for y in range(self._height):
            grid[y][0] = 'X'
            grid[y][self._width - 1] = 'X'

        # Расставляем объекты (поверх ландшафта)
        for obj in self._objects:
            x, y = obj.get_position()
            grid[y][x] = obj.get_symbol()

        # Собираем в строку
        lines = []
        for row in grid:
            lines.append(' '.join(row))
        return '\n'.join(lines)

    def __str__(self):
        return self.render()