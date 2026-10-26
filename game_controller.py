from game_field import GameField
from units import BaseUnit, UNIT_TYPES
from base import Base
from landscape import Grass, Forest, Mountain, Water, LANDSCAPE_TYPES
from neutral_objects import INeutralObject, NEUTRAL_TYPES
from typing import List, Tuple, Optional
import random


class GameController:

    def __init__(self, width: int = 20, height: int = 20):
        # Генерация ландшафта
        self._landscape_grid = self._generate_landscape(width, height)
        
        self._field = GameField(width, height, max_objects=50, 
                                landscape_grid=self._landscape_grid)
        self._base = Base(position=(1, 1), max_units=10, resources=100)
        self._field.add_object(self._base)
        self._selected_unit: Optional[BaseUnit] = None
        self._running = True

        # Генерация нейтральных объектов
        self._generate_neutral_objects()
    def _generate_neutral_objects(self):
        """Автоматическая генерация нейтральных объектов на поле."""
        from neutral_objects import TreasureChest, HealingFountain, Trap, Merchant
        
        # Создаём по 2 объекта каждого типа
        objects_to_create = [
            (TreasureChest, 2, 50),      # (класс, количество, параметр)
            (HealingFountain, 2, 30),
            (Trap, 3, 25),
            (Merchant, 1, None),
        ]
        
        for obj_class, count, param in objects_to_create:
            for _ in range(count):
                position = self._find_free_position()
                if position:
                    if param is not None:
                        obj = obj_class(position, param)
                    else:
                        obj = obj_class(position)
                    self._field.add_object(obj)


    def _find_free_position(self) -> Optional[Tuple[int, int]]:
        """Найти случайную свободную позицию на поле."""
        import random
        
        for _ in range(100):  # Пробуем 100 раз
            x = random.randint(2, self._field.width - 2)
            y = random.randint(2, self._field.height - 2)
            if not self._field.get_object_at((x, y)):
                return (x, y)
        
        return None

    def _generate_landscape(self, width: int, height: int):
        """Генерация случайного ландшафта"""
        grid = []
        for y in range(height):
            row = []
            for x in range(width):
                # Случайный выбор ландшафта с весами
                rand = random.random()
                if rand < 0.6:  # 60% трава
                    row.append(Grass())
                elif rand < 0.8:  # 20% лес
                    row.append(Forest())
                elif rand < 0.9:  # 10% горы
                    row.append(Mountain())
                else:  # 10% вода
                    row.append(Water())
            grid.append(row)
        return grid

    def start(self):
        """Запуск игры."""
        print("Добро пожаловать в RPG игру!")
        while self._running:
            self._main_menu()

    def _main_menu(self):
        """Главное меню"""
        from instance_counter import InstanceCounter

        print("\n" + "="*40)
        print("1 - Управление базой")
        print("2 - Управление юнитом")
        print("3 - Загрузить игру")
        print("4 - Сохранить игру")
        print("5 - Закончить ход")
        print("6 - Новая игра")
        print("0 - Выход")
        print("="*40)
        print(f" Живых объектов: {InstanceCounter.get_count()}")

        choice = input("Выбор: ").strip()

        if choice == "1":
            self._base_menu()
        elif choice == "2":
            self._unit_menu()
        elif choice == "3":
            print(" Загрузка игры пока не реализована")
        elif choice == "4":
            print("Сохранение игры пока не реализовано")
        elif choice == "5":
            self._end_turn()
        elif choice == "6":
            self._new_game()
        elif choice == "0":
            print(" До свидания!")
            self._running = False
        else:
            print("⚠ Неверный выбор!")

    def _counter_menu(self):
        """Меню статистики счётчика (вариант 17)."""
        from instance_counter import InstanceCounter

        while True:
            print(f"\n{Fore.CYAN}{Style.BRIGHT}--- Статистика счётчика (вар.17) ---")
            print(f"1 - Показать текущее количество")
            print(f"2 - Показать общее количество созданных")
            print(f"3 - Показать лог операций")
            print(f"4 - Сохранить в JSON")
            print(f"5 - Загрузить из JSON")
            print(f"0 - Назад")
            print(f"{Style.RESET_ALL}")

            choice = input("Выбор: ").strip()

            if choice == "1":
                print(f" Живых экземпляров: {InstanceCounter.get_count()}")
            elif choice == "2":
                print(f" Всего создано за сессию: {InstanceCounter.get_total_created()}")
            elif choice == "3":
                log = InstanceCounter.get_log()
                if not log:
                    print("Лог пуст.")
                else:
                    for entry in log:
                        action = entry.get("action", "")
                        icon = "✅" if action == "created" else "🗑"
                        print(f"  {icon} ID={entry.get('id')}: {entry.get('name')} "
                            f"({entry.get('created_at', entry.get('deleted_at', ''))})")
            elif choice == "4":
                filepath = input("Путь к файлу (по умолчанию instances_log.json): ").strip()
                if not filepath:
                    filepath = "instances_log.json"
                # Создаём временный экземпляр для сохранения
                temp = InstanceCounter("Сохранение")
                temp.save_to_json(filepath)
                del temp
            elif choice == "5":
                filepath = input("Путь к файлу (по умолчанию instances_log.json): ").strip()
                if not filepath:
                    filepath = "instances_log.json"
                InstanceCounter.load_from_json(filepath)
            elif choice == "0":
                break
            else:
                print("⚠ Неверный выбор!")

    def _save_game(self):
        """Сохранить игру."""
        filepath = input("Путь к файлу сохранения (по умолчанию savegame.json): ").strip()
        if not filepath:
            filepath = "savegame.json"
        self._base.save_game(filepath)


    def _load_game(self):
        """Загрузить игру."""
        filepath = input("Путь к файлу сохранения (по умолчанию savegame.json): ").strip()
        if not filepath:
            filepath = "savegame.json"
        self._base.load_game(filepath)

    def _base_menu(self):
        """Меню управления базой."""
        while True:
            print("\n Управление базой ")
            print("1 - Состояние базы")
            print("2 - Состояние войска")
            print("3 - Создание юнита")
            print("4 - Особые умения")
            print("0 - Назад")

            choice = input("Выбор действия: ").strip()

            if choice == "1":
                print("\n" + str(self._base))
            elif choice == "2":
                self._show_army_status()
            elif choice == "3":
                self._create_unit_menu()
            elif choice == "4":
                print(" Особые умения пока не реализованы")
            elif choice == "0":
                break
            else:
                print("⚠ Неверный выбор!")

    def _show_army_status(self):
        """Показать состояние войска (рис. 5)."""
        print("\n Состояние войска ")
        print(f"Ресурсы на лучников: {self._base.resources}")
        print(f"Ресурсы на волшебников: {self._base.resources}")
        print(f"Ресурсы на воинов: {self._base.resources}")
        print(f"Численность войска: {self._base.units_count} единиц")
        print("Из них:")

        # Подсчёт по типам
        unit_counts = {}
        for unit in self._base.units:
            name = unit.get_name()
            unit_counts[name] = unit_counts.get(name, 0) + 1

        print(f"  Лучники: {unit_counts.get('Лучник', 0)} :: Лук: {unit_counts.get('Лучник', 0)} - _- Арбалет: 0")
        print(f"  Волшебники: 0 :: Целитель: {unit_counts.get('Целитель', 0)} - _- Маг: {unit_counts.get('Маг', 0)}")
        print(f"  Воины: {unit_counts.get('Мечник', 0)} :: Мечники: {unit_counts.get('Мечник', 0)} - _- Рыцари: 0")

        print("\nСписок юнитов:")
        for i, unit in enumerate(self._base.units, 1):
            symbol = unit.get_symbol()
            name = unit.get_name()
            print(f"  {i} - ({symbol}) - {name}")

    def _create_unit_menu(self):
        """Меню создания юнита."""
        print("\n Создание юнита ")
        print("Доступные типы:")
        for i, (name, _) in enumerate(UNIT_TYPES.items(), 1):
            print(f"  {i} - {name}")

        choice = input("Выбор типа юнита: ").strip()
        try:
            idx = int(choice) - 1
            unit_names = list(UNIT_TYPES.keys())
            if 0 <= idx < len(unit_names):
                unit_type = unit_names[idx]
                
                # Находим свободную позицию рядом с базой
                base_x, base_y = self._base.get_position()
                spawn_position = self._find_free_position_near(base_x, base_y)
                
                if spawn_position:
                    self._base.create_unit(unit_type, spawn_position)
                    # Добавляем юнита на поле
                    unit = self._base.units[-1]  # Последний созданный
                    self._field.add_object(unit)
                else:
                    print("⚠ Нет свободных позиций рядом с базой!")
            else:
                print("⚠ Неверный номер!")
        except ValueError:
            print(" Введите число!")
    def _find_free_position_near(self, base_x: int, base_y: int) -> Optional[Tuple[int, int]]:
        """Найти свободную позицию рядом с базой."""
        # Проверяем клетки вокруг базы по спирали
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), 
                    (1, 1), (-1, 1), (1, -1), (-1, -1)]
        
        for dx, dy in directions:
            x, y = base_x + dx, base_y + dy
            if 0 <= x < self._field.width and 0 <= y < self._field.height:
                if not self._field.get_object_at((x, y)):
                    return (x, y)
        
        # Если все рядом заняты — ищем дальше
        for radius in range(2, 5):
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    x, y = base_x + dx, base_y + dy
                    if 0 <= x < self._field.width and 0 <= y < self._field.height:
                        if not self._field.get_object_at((x, y)):
                            return (x, y)
    
        return None

    def _unit_menu(self):
        """Меню управления юнитом (рис. 4)."""
        if not self._base.units:
            print("⚠ Нет доступных юнитов!")
            return

        print("\n Выберите юнита ")
        for i, unit in enumerate(self._base.units, 1):
            print(f"  {i} - {unit.get_name()} на {unit.get_position()}")

        choice = input("Номер юнита: ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(self._base.units):
                self._selected_unit = self._base.units[idx]
                self._unit_control_menu()
            else:
                print("⚠ Неверный номер!")
        except ValueError:
            print(" Введите число!")

    def _unit_control_menu(self):
        """Меню управления конкретным юнитом."""
        while True:
            print(f"\n Управление: {self._selected_unit.get_name()} ")
            print("1 - Перемещение")
            print("2 - Использование способности")
            print("3 - Оставить юнита в покое")
            print("0 - Назад")

            choice = input("Выбор действия: ").strip()

            if choice == "1":
                self._move_unit()
            elif choice == "2":
                self._use_ability()
            elif choice == "3":
                print(f"{self._selected_unit.get_name()} отдыхает.")
                break
            elif choice == "0":
                break
            else:
                print("⚠ Неверный выбор!")

    def _move_unit(self):
        """Перемещение юнита."""
        print(f"Текущая позиция: {self._selected_unit.get_position()}")
        x = int(input("Новая координата X: "))
        y = int(input("Новая координата Y: "))
        new_pos = (x, y)

        # Проверка границ
        if not (0 <= x < self._field.width and 0 <= y < self._field.height):
            print("⚠ Позиция вне поля!")
            return

        # Проверка ландшафта
        landscape = self._landscape_grid[y][x]
        if not landscape.can_unit_enter(self._selected_unit.get_name()):
            print(f" {self._selected_unit.get_name()} не может войти на {landscape.get_name()}!")
            return

        # Проверка занятости
        existing = self._field.get_object_at(new_pos)
        if existing and existing != self._selected_unit:
            # Проверяем, является ли объект нейтральным
            from neutral_objects import INeutralObject
            if isinstance(existing, INeutralObject):
                # Юнит может встать на клетку с нейтральным объектом
                pass
            else:
                print("⚠ Позиция занята!")
                return

        # Перемещение
        self._field.remove_object(self._selected_unit)
        self._selected_unit.move(new_pos)
        self._field.add_object(self._selected_unit)
        print(f" {self._selected_unit.get_name()} переместился на {new_pos}")

        # Проверяем взаимодействие с нейтральным объектом
        self._check_neutral_interaction(new_pos)

    def _check_neutral_interaction(self, position: Tuple[int, int]):
        """Проверить и вызвать взаимодействие с нейтральным объектом."""
        from neutral_objects import INeutralObject
        
        obj = self._field.get_object_at(position)
        if obj and isinstance(obj, INeutralObject):
            print(f"\n {self._selected_unit.get_name()} наткнулся на {obj.get_name()}!")
            
            # Для торговца показываем меню
            from neutral_objects import Merchant
            if isinstance(obj, Merchant):
                self._merchant_menu(obj)
            else:
                # Автоматическое взаимодействие для остальных
                result = obj + self._selected_unit  # Перегрузка оператора
                print(result)
                
                # Удаляем объект если он одноразовый (сундук, ловушка)
                from neutral_objects import TreasureChest, Trap
                if isinstance(obj, (TreasureChest, Trap)):
                    if hasattr(obj, '_opened') and obj._opened:
                        self._field.remove_object(obj)
                        print("🗑 Объект исчез с поля.")
                    elif hasattr(obj, '_triggered') and obj._triggered:
                        self._field.remove_object(obj)
                        print(" Ловушка исчезла с поля.")

    def _merchant_menu(self, merchant):
        """Меню взаимодействия с торговцем."""
        print(f"\n--- Торговец ---")
        print(f"Привет, {self._selected_unit.get_name()}! Что хочешь купить?")
        print("1 - Улучшить атаку (+5) — 30 золота")
        print("2 - Улучшить броню (+3) — 40 золота")
        print("0 - Уйти")
        
        choice = input("Выбор: ").strip()
        
        if choice == "1":
            if self._base.resources >= 30:
                self._base._resources -= 30
                self._selected_unit._attack += 5
                print(f" Атака улучшена! Теперь: {self._selected_unit._attack}")
            else:
                print("⚠ Недостаточно ресурсов!")
        elif choice == "2":
            if self._base.resources >= 40:
                self._base._resources -= 40
                self._selected_unit._armor += 3
                print(f" Броня улучшена! Теперь: {self._selected_unit._armor}")
            else:
                print("⚠ Недостаточно ресурсов!")
        else:
            print("Торговец: До встречи!")

    def _use_ability(self):
        """Использование способности юнита."""
        from units import Healer
        if isinstance(self._selected_unit, Healer):
            print("Выберите цель для лечения:")
            for i, unit in enumerate(self._base.units, 1):
                if unit != self._selected_unit:
                    print(f"  {i} - {unit.get_name()} (HP: {unit.get_health()})")
            choice = input("Номер цели: ").strip()
            try:
                idx = int(choice) - 1
                targets = [u for u in self._base.units if u != self._selected_unit]
                if 0 <= idx < len(targets):
                    self._selected_unit.heal(targets[idx])
            except ValueError:
                print("⚠ Введите число!")
        else:
            print(f"{self._selected_unit.get_name()} атакует!")
            # Здесь можно добавить логику атаки

    def _end_turn(self):
        """Завершить ход."""
        print("\n Конец хода ")
        print("Поле:")
        print(self._field)

    def _new_game(self):
        """Новая игра."""
        print("\n Новая игра...")
        self.__init__()  # Пересоздание контроллера