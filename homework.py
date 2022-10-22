class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return f"Тип тренировки: {self.training_type}; "\
               f"Длительность: {self.duration:.3f} ч.; "\
               f"Дистанция: {self.distance:.3f} км; "\
               f"Ср. скорость: {self.speed:.3f} км/ч; "\
               f"Потрачено ккал: {self.calories:.3f}."


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_H = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.len_step: float = 0.65
        self.len_step = 0.65

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.len_step / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.action * self.len_step / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * Running.get_mean_speed(self)
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * self.duration * 60)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    KMH_IN_MSEC = 0.278
    CM_IN_M = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:

        speed_ms: float = SportsWalking.get_mean_speed(self) * self.KMH_IN_MSEC
        height_m: float = self.height / self.CM_IN_M

        result = ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                  + ((speed_ms ** 2) / height_m)
                  * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                  * self.weight) * self.duration * 60)

        return result


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_SHIFT = 1.1
    CALORIES_WEIGHT_MULTIPLIER = 2

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.len_step = 1.38
        self.length_pool = length_pool
        self.count_pool = count_pool
        """Умышленно сделал счетчик бассейнов флоат,
        могут быть не полные круги"""

    def get_mean_speed(self) -> float:
        return (self.length_pool
                * self.count_pool / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((Swimming.get_mean_speed(self) + 1.1)
                * 2 * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type == "SWM":
        obj = Swimming(data[0], data[1], data[2], data[3], data[4])
        return obj
    elif workout_type == "RUN":
        obj = Running(data[0], data[1], data[2])
        return obj
    elif workout_type == "WLK":
        obj = SportsWalking(data[0], data[1], data[2], data[3])
        return obj
    else:
        print("не найдем идентификатор")


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
