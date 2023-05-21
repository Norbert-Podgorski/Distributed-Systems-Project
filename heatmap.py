import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine


def legend_without_duplicate_labels(figure):
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    figure.legend(by_label.values(), by_label.keys(), bbox_to_anchor=(1.01, 1), loc='upper left')


def generate_heatmap():
    db_string = "postgresql://postgres:postgres@localhost:5432/postgres"
    engine = create_engine(db_string)

    df_stations = pd.DataFrame(engine.execute('SELECT * FROM stations').fetchall())

    for idx, station in enumerate(list(df_stations.station_idx)):
        query = f'SELECT * FROM station_number_{station}'
        if idx == 0:
            df_observations = pd.DataFrame(engine.execute(query).fetchall())
        else:
            df_observations = pd.concat([df_observations, pd.DataFrame(engine.execute(query).fetchall())])

    sns.scatterplot(data=df_observations, x='x', y='y', hue='station_idx', size='power')
    legend_without_duplicate_labels(plt)
    plt.grid()
    plt.tight_layout()
    plt.savefig('./static/heatmap_pic.png')
    plt.grid()



if __name__ == '__main__':
    generate_heatmap()
