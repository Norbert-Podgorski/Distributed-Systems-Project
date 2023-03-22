import random
from dataclasses import dataclass
from typing import Dict

import ray


@dataclass
class StationObservationArea:
    x_min: int
    x_max: int
    y_min: int
    y_max: int


@ray.remote
class Station(object):
    def __init__(self):
        self.activity_detected: Dict[str, int] = {}
        self.observation_area: StationObservationArea = self.generate_random_observation_area()

    @staticmethod
    def generate_random_observation_area() -> StationObservationArea:
        # Suppose the final image has shape 400 x 400 and station cover
        # Suppose the station covers the area of a rectangle with a minimum side length of 20 and a maximum of 100
        x_min = random.randint(0, 300)
        y_min = random.randint(0, 300)
        x_max = random.randint(x_min + 20, x_min + 100)
        y_max = random.randint(y_min + 20, y_min + 100)
        return StationObservationArea(x_min, x_max, y_min, y_max)

    def simulate_new_activity(self) -> None:
        activity_power = random.randint(1, 10)
        activity_x_coord = random.randint(self.observation_area.x_min, self.observation_area.x_max)
        activity_y_coord = random.randint(self.observation_area.y_min, self.observation_area.y_max)
        self.activity_detected = {"activity_x_coord": activity_x_coord, "activity_y_coord": activity_y_coord, "activity_power": activity_power}

    def get_and_clear_activity(self) -> Dict[str, int]:
        activity = self.activity_detected
        self.activity_detected = {}
        return activity
