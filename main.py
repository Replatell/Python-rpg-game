from game_controller import GameController
from instance_counter import InstanceCounter


def main():

    # Сбрасываем счётчики при новом запуске
    InstanceCounter.reset()
    
    game = GameController(width=20, height=20)
    game.start()


if __name__ == "__main__":
    main()
