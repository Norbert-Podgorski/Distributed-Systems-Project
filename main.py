import random
import time
from typing import List

import ray

from station import Station


def start_simulation() -> None:
    # param
    stations_number = 4
    stations = [Station.remote() for _ in range(stations_number)]

    [stations_worker.remote(stations, station_number) for station_number in range(stations_number)]

    # For testing purposes only:
    while True:
        time.sleep(1)
        i = 0
        for station in stations:
            time.sleep(1)
            new_activity = ray.get(station.get_and_clear_activity.remote())
            if new_activity:
                print("Station: ", i, " new activity:", new_activity)
            else:
                print("Station: ", i, " no new activity")
            i += 1


@ray.remote
def stations_worker(stations: List[Station], station_number: int) -> None:
    # param
    activity_simulation_break_time = 5

    while True:
        station_number = random.randint(0, 2)

        # For testing purposes only:
        print("Station number: ", station_number, "Random station_number: ", station_number)

        if station_number == station_number:
            stations[station_number].simulate_new_activity.remote()
        time.sleep(activity_simulation_break_time)


if __name__ == "__main__":
    start_simulation()
