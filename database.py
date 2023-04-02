from sqlalchemy import Column, create_engine, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base


class Database:
    def __init__(self, database_type: str = 'postgresql', user: str = 'postgres', password: str = 'postgres',
                 database_url: str = 'localhost', port: int = 5432, database_name: str = 'postgres'):

        db_string = f"{database_type}://{user}:{password}@{database_url}:{port}/{database_name}"
        self.engine = create_engine(db_string)
        self.Base = declarative_base()

        self.create_stations_table()

    def create_stations_table(self):
        class Stations(self.Base):
            __tablename__ = 'stations'
            station_idx = Column(Integer, primary_key=True)
            x_min = Column(Integer)
            x_max = Column(Integer)
            y_min = Column(Integer)
            y_max = Column(Integer)

        self.Base.metadata.create_all(self.engine)

    def delete_table(self, station_idx: int):
        self.engine.execute(f'DROP TABLE station_number_{station_idx}')

    def add_station(self, station_idx: int, x_min: int, x_max: int, y_min: int, y_max: int):
        station_idx_class = station_idx

        class StationNumber(self.Base):
            __tablename__ = f'station_number_{station_idx_class}'
            observation_idx = Column(Integer, primary_key=True)
            station_idx = Column(Integer, ForeignKey('stations.station_idx'))
            x = Column(Integer)
            y = Column(Integer)
            power = Column(Integer)

        self.Base.metadata.create_all(self.engine)

        query = f'INSERT INTO stations VALUES ({station_idx}, {x_min}, {x_max}, {y_min}, {y_max})'

        self.engine.execute(query)

    def delete_station(self, station_idx: int):
        self.engine.execute(f'DROP TABLE station_number_{station_idx}')
        self.engine.execute(f'DELETE FROM stations WHERE station_idx={station_idx}')

    def add_observation(self, station_idx: int, x: int, y: int, power: int):
        query = f'''INSERT INTO station_number_{station_idx} (station_idx, x, y, power)
                VALUES ({station_idx}, {x}, {y}, {power})'''

        self.engine.execute(query)

    def delete_observation(self, station_idx: int, observation_idx: int):
        self.engine.execute(f'DELETE FROM station_number_{station_idx} WHERE observation_idx={observation_idx}')

    def delete_last_observation(self):
        # TODO
        pass


if __name__ == '__main__':
    pass
