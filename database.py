import ray
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


@ray.remote
class Database:
    def __init__(
        self, database_type: str = 'postgresql', user: str = 'postgres', password: str = 'postgres',
        database_url: str = 'localhost', port: int = 5432, database_name: str = 'postgres'
    ):
        db_string = f"{database_type}://{user}:{password}@{database_url}:{port}/{database_name}"
        self.engine = create_engine(db_string)
        self.Base = declarative_base()

        self.clear_database()
        self.create_stations_table()

    def create_stations_table(self):
        query = '''CREATE TABLE IF NOT EXISTS stations (
                    station_idx INT NOT NULL PRIMARY KEY,
                    x_min INT NOT NULL,
                    x_max INT NOT NULL,
                    y_min INT NOT NULL,
                    y_max INT NOT NULL
                    )
        '''
        self.engine.execute(query)

    def clear_database(self):
        for station_idx in range(self.engine.execute('SELECT MAX(station_idx) FROM stations').fetchall()[0][0] + 1):
            self.engine.execute(f'DROP TABLE station_number_{station_idx}')
        self.engine.execute(f'DROP TABLE stations')

    def add_station(self, station_idx: int, x_min: int, x_max: int, y_min: int, y_max: int):
        query = f'''CREATE TABLE station_number_{station_idx} (
                    observation_idx INT NOT NULL PRIMARY KEY,
                    station_idx INT NOT NULL REFERENCES stations(station_idx),
                    x INT NOT NULL,
                    y INT NOT NULL,
                    power INT NOT NULL
                    )
        '''
        self.engine.execute(query)

        query = f'INSERT INTO stations VALUES ({station_idx}, {x_min}, {x_max}, {y_min}, {y_max})'
        self.engine.execute(query)

    def add_observation(self, station_idx: int, x: int, y: int, power: int):
        observation_idx = 1
        if self.engine.execute(
            f'''SELECT observation_idx FROM station_number_{station_idx} 
                    ORDER BY observation_idx DESC'''
        ).fetchone() is not None:
            observation_idx = self.engine.execute(
                f'''SELECT observation_idx FROM station_number_{station_idx} 
                    ORDER BY observation_idx DESC'''
            ).fetchone()[0] + 1

        query = f'INSERT INTO station_number_{station_idx} VALUES ({observation_idx}, {station_idx}, {x}, {y}, {power})'

        self.engine.execute(query)


if __name__ == '__main__':
    pass
