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
    def __init__(self, idx: int, observation_area: StationObservationArea):
        self.idx: int = idx
        self.observation_area: StationObservationArea = observation_area
        self.activity_detected: Dict[str, int] = {}

    def simulate_new_activity(self) -> None:
        activity_power = random.randint(1, 10)
        activity_x_coord = random.randint(self.observation_area.x_min, self.observation_area.x_max)
        activity_y_coord = random.randint(self.observation_area.y_min, self.observation_area.y_max)
        self.activity_detected = {"activity_x_coord": activity_x_coord, "activity_y_coord": activity_y_coord, "activity_power": activity_power}

    def get_and_clear_activity(self) -> Dict[str, int]:
        activity = self.activity_detected
        self.activity_detected = {}
        return activity
