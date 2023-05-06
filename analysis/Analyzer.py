import pandas as pd
from mysql.connector.abstracts import MySQLConnectionAbstract
from text_unidecode import unidecode

from ChartParams import ChartParams
from ChartVisualizer import ChartVisualizer
from SqlQueries import SqlQueries


class Analyzer:
    results_dir = './results/data'

    def __init__(self, connection: MySQLConnectionAbstract):
        self.connection = connection

    def mean_score_by_fav_game_type(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True):
        result_pd = pd.read_sql(SqlQueries.mean_score_by_fav_game_type, self.connection)
        title = 'Statystyczna średnia liczba punktów na typ ulubionej gry'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            filename = title.replace(' ', '_')
            filename = unidecode(filename)
            filename = f"{filename}.csv"

            result_pd.to_csv(f'{Analyzer.results_dir}/{filename}', index=False)

        if visualize or save_visualization:
            ChartVisualizer.bar(ChartParams(
                x=result_pd['fav_game_type'],
                y=result_pd['mean_score'],
                fig_title=title,
                fig_size=(20, 10),
                x_label='Typ ulubionej gry',
                y_label='Średnia liczba punktów',
            ), save_visualization)
