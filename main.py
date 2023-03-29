import random
import time
from typing import List

import ray

from station import Station, StationObservationArea


def main() -> None:
    # For testing purposes only or if we fail to implement load_stations_added_from_website()
    stations = generate_random_stations()

    # stations = load_stations_added_from_website()
    start_simulation(stations)


def generate_random_stations() -> List[Station]:
    # param
    stations_number = 4
    stations = [Station.remote(idx=i, observation_area=generate_random_observation_area()) for i in range(stations_number)]
    return stations


def generate_random_observation_area() -> StationObservationArea:
    # Suppose the final image has shape 400 x 400
    # Suppose the station covers the area of a rectangle with a minimum side length of 20 and a maximum of 100
    x_min = random.randint(0, 300)
    y_min = random.randint(0, 300)
    x_max = random.randint(x_min + 20, x_min + 100)
    y_max = random.randint(y_min + 20, y_min + 100)
    return StationObservationArea(x_min, x_max, y_min, y_max)


def load_stations_added_from_website() -> List[Station]:
    pass


def save_stations_added_from_website() -> None:
    pass


def update_stations_after_removing_from_website() -> None:
    pass


def start_simulation(stations: List[Station]) -> None:
    stations_number = len(stations)
    [stations_worker.remote(stations, station_number) for station_number in range(stations_number)]

    # For testing purposes only:
    while True:
        time.sleep(1)
        i = 0
        for station in stations:
            time.sleep(1)
            print("Station: ", i, " new activity: ")
            station.read_report.remote()
            i += 1


@ray.remote
def stations_worker(stations: List[Station], station_number: int) -> None:
    # param
    activity_simulation_break_time = 5

    while True:
        random_station_number = random.randint(0, len(stations) - 1)

        # For testing purposes only:
        print("Station number: ", station_number, "Random station_number: ", random_station_number)

        if station_number == random_station_number:
            stations[station_number].simulate_new_activity.remote()
        time.sleep(activity_simulation_break_time)


if __name__ == "__main__":
    main()
