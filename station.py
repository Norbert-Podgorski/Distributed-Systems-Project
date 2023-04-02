import os
import random
from dataclasses import dataclass
from typing import Dict
from xml.dom import minidom

import ray


@dataclass
class StationObservationArea:
    x_min: int
    x_max: int
    y_min: int
    y_max: int


@ray.remote
class Station(object):
    def __init__(self, idx: int, observation_area: StationObservationArea, database):
        self.idx: int = idx
        self.observation_area: StationObservationArea = observation_area
        self.activity_detected: Dict[str, int] = {}
        self.create_report_structure()
        self.database = database
        self.database.add_station.remote(self.idx, self.observation_area.x_min, self.observation_area.x_max,
                                         self.observation_area.y_min, self.observation_area.y_max)

    def simulate_new_activity(self) -> None:
        activity_x_coord = random.randint(self.observation_area.x_min, self.observation_area.x_max)
        activity_y_coord = random.randint(self.observation_area.y_min, self.observation_area.y_max)
        activity_power = random.randint(1, 10)
        self.update_report(activity_x_coord, activity_y_coord, activity_power)

    def read_report(self) -> None:
        # For testing purposes only:
        report = minidom.parse("station_reports/" + str(self.idx) + ".xml")
        activity = report.getElementsByTagName("detected_activity")[0]
        print("activity_x_coord: ", activity.getAttribute('x'))
        print("activity_y_coord: ", activity.getAttribute('y'))
        print("activity_power: ", activity.getAttribute('power'))
        if len(activity.getAttribute('x')) > 0:
            self.database.add_observation.remote(self.idx, int(activity.getAttribute('x')),
                                                 int(activity.getAttribute('y')), int(activity.getAttribute('power')))

        self.clear_report()

    def create_report_structure(self) -> None:
        root = minidom.Document()

        station = root.createElement('station')
        station.setAttribute('idx', str(self.idx))
        root.appendChild(station)

        observation_area = root.createElement('observation_area')
        observation_area.setAttribute('x_min', str(self.observation_area.x_min))
        observation_area.setAttribute('x_max', str(self.observation_area.x_max))
        observation_area.setAttribute('y_min', str(self.observation_area.y_min))
        observation_area.setAttribute('y_max', str(self.observation_area.y_max))
        station.appendChild(observation_area)

        detected_activity = root.createElement('detected_activity')
        detected_activity.setAttribute('x', None)
        detected_activity.setAttribute('y', None)
        detected_activity.setAttribute('power', None)
        station.appendChild(detected_activity)

        xml_str = root.toprettyxml(indent="\t")
        directory_path = "station_reports"
        save_path_file = directory_path + "/" + str(self.idx) + ".xml"

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        with open(save_path_file, "w") as f:
            f.write(xml_str)

    def update_report(self, activity_x_coord: int, activity_y_coord: int, activity_power: int) -> None:
        report = minidom.parse("station_reports/" + str(self.idx) + ".xml")
        activity = report.getElementsByTagName("detected_activity")[0]
        activity.setAttribute('x', str(activity_x_coord))
        activity.setAttribute('y', str(activity_y_coord))
        activity.setAttribute('power', str(activity_power))

        xml_str = report.toprettyxml(indent="\t")
        save_path_file = "station_reports/" + str(self.idx) + ".xml"

        with open(save_path_file, "w") as f:
            f.write(xml_str)

    def clear_report(self):
        # Server should use this once it has read the report
        report = minidom.parse("station_reports/" + str(self.idx) + ".xml")
        activity = report.getElementsByTagName("detected_activity")[0]
        activity.setAttribute('x', None)
        activity.setAttribute('y', None)
        activity.setAttribute('power', None)

        xml_str = report.toprettyxml(indent="\t")
        save_path_file = "station_reports/" + str(self.idx) + ".xml"

        with open(save_path_file, "w") as f:
            f.write(xml_str)
