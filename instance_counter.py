import json
import os
from datetime import datetime


class InstanceCounter:
    """
    Класс, подсчитывающий количество своих экземпляров в приложении.
    Вариант 17: перегрузка __del__, сохранение/загрузка в JSON.
    """

    # Классовая переменная — общая для всех экземпляров
    _instance_count = 0
    _total_created = 0  # Всего созданных за всё время
    _instances_log = []  # Лог созданных экземпляров

    def __init__(self, name: str = "Экземпляр", data: dict = None):
        """
        Создание экземпляра.
        :param name: Имя экземпляра
        :param data: Данные для восстановления из JSON (опционально)
        """
        InstanceCounter._instance_count += 1
        InstanceCounter._total_created += 1

        self._id = InstanceCounter._total_created
        self._name = name
        self._created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Если данные переданы из JSON — восстанавливаем их
        if data:
            self._name = data.get("name", name)
            self._created_at = data.get("created_at", self._created_at)
            self._id = data.get("id", self._id)

        # Логируем создание
        log_entry = {
            "id": self._id,
            "name": self._name,
            "created_at": self._created_at,
            "action": "created"
        }
        InstanceCounter._instances_log.append(log_entry)

        print(f" [{self._name}] создан. ID={self._id}")
        print(f"    Текущее количество экземпляров: {InstanceCounter._instance_count}")
        print(f"    Всего создано за сессию: {InstanceCounter._total_created}")

    def __del__(self):
        """
        Перегрузка __del__ — вызывается при уничтожении экземпляра.
        """
        InstanceCounter._instance_count -= 1

        log_entry = {
            "id": self._id,
            "name": self._name,
            "deleted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "action": "deleted"
        }
        InstanceCounter._instances_log.append(log_entry)

        print(f" [{self._name}] уничтожен. ID={self._id}")
        print(f"    Осталось экземпляров: {InstanceCounter._instance_count}")

    @classmethod
    def get_count(cls) -> int:
        """Вернуть текущее количество живых экземпляров."""
        return cls._instance_count

    @classmethod
    def get_total_created(cls) -> int:
        """Вернуть общее количество созданных экземпляров."""
        return cls._total_created

    @classmethod
    def get_log(cls) -> list:
        """Вернуть лог всех операций."""
        return cls._instances_log

    @classmethod
    def reset(cls):
        """Сбросить счётчики (для новой игры)."""
        cls._instance_count = 0
        cls._total_created = 0
        cls._instances_log = []
        print(" Счётчики сброшены.")

    def get_info(self) -> dict:
        """Получить информацию об экземпляре в виде словаря."""
        return {
            "id": self._id,
            "name": self._name,
            "created_at": self._created_at,
            "current_count": InstanceCounter._instance_count,
            "total_created": InstanceCounter._total_created
        }

    def save_to_json(self, filepath: str = "instances_log.json"):
        """
        Сохранить лог всех экземпляров в JSON-файл.
        """
        data = {
            "current_count": InstanceCounter._instance_count,
            "total_created": InstanceCounter._total_created,
            "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "log": InstanceCounter._instances_log
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f" Данные сохранены в {filepath}")

    @classmethod
    def load_from_json(cls, filepath: str = "instances_log.json") -> dict:
        """
        Загрузить данные из JSON-файла.
        Возвращает словарь с историей.
        """
        if not os.path.exists(filepath):
            print(f"⚠ Файл {filepath} не найден!")
            return {}

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        print(f" Загружены данные из {filepath}")
        print(f"   Сохранено: {data.get('saved_at')}")
        print(f"   Было экземпляров: {data.get('current_count')}")
        print(f"   Всего создано: {data.get('total_created')}")
        print(f"   Записей в логе: {len(data.get('log', []))}")

        return data

    def __str__(self):
        return (f"InstanceCounter(id={self._id}, name='{self._name}', "
                f"alive={InstanceCounter._instance_count})")


# ===== Интеграция с юнитами =====
class UnitCounter(InstanceCounter):
    """
    Специализированный счётчик для юнитов.
    Наследуется от InstanceCounter и автоматически считает юнитов.
    """

    def __init__(self, unit_name: str, unit_type: str):
        self._unit_type = unit_type
        super().__init__(name=f"{unit_type}: {unit_name}")

    def get_info(self) -> dict:
        info = super().get_info()
        info["unit_type"] = self._unit_type
        return info


# ===== Тестовый запуск =====
if __name__ == "__main__":
    print("=== Тест InstanceCounter ===\n")

    # Создаём экземпляры
    c1 = InstanceCounter("Юнит-1")
    c2 = InstanceCounter("Юнит-2")
    c3 = InstanceCounter("Юнит-3")

    print(f"\nТекущее количество: {InstanceCounter.get_count()}")
    print(f"Всего создано: {InstanceCounter.get_total_created()}")

    # Сохраняем в JSON
    c1.save_to_json("test_instances.json")

    # Удаляем один экземпляр
    print("\n--- Удаляем Юнит-2 ---")
    del c2

    print(f"\nТекущее количество: {InstanceCounter.get_count()}")

    # Загружаем из JSON
    print("\n--- Загрузка из JSON ---")
    InstanceCounter.load_from_json("test_instances.json")

    print("\n=== Тест завершён ===")