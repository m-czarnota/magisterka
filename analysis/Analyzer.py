import pandas as pd
from mysql.connector.abstracts import MySQLConnectionAbstract
from text_unidecode import unidecode

from ChartTypeEnum import ChartTypeEnum
from ChartParams import ChartParams
from ChartVisualizer import ChartVisualizer
from SqlQueries import SqlQueries


class Analyzer:
    results_dir = './results/data'

    def __init__(self, connection: MySQLConnectionAbstract):
        self.connection = connection

    def mean_score_by_fav_game_type(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(SqlQueries.mean_score_by_fav_game_type, self.connection)
        title = 'Statystyczna średnia liczba punktów na typ ulubionej gry'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer.__save_to_file(result_pd, title)

        if visualize or save_visualization:
            ChartVisualizer.visualize(ChartTypeEnum.BAR, ChartParams(
                x=result_pd['fav_game_type'],
                y=result_pd['mean_score'],
                fig_title=title,
                fig_size=(20, 10),
                x_label='Typ ulubionej gry',
                y_label='Średnia liczba punktów',
            ), save_visualization)

    def dependency_score_on_time(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(SqlQueries.time_and_score, self.connection)
        title = 'Zależność wyniku od czasu gry'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer.__save_to_file(result_pd, title)

        if visualize or save_visualization:
            ChartVisualizer.visualize(ChartTypeEnum.SCATTER, ChartParams(
                x=result_pd['time'],
                y=result_pd['score'],
                fig_title=title,
                fig_size=(20, 10),
                x_label='Czas gry (s)',
                y_label='Wynik',
                classes=result_pd['fav_game_type'],
            ), save_visualization)

    def best_score_by_age(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(SqlQueries.best_score_by_age, self.connection)
        title = 'Najlepszy wynik na grupę wiekową'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer.__save_to_file(result_pd, title)

        if visualize or save_visualization:
            ChartVisualizer.visualize(ChartTypeEnum.BAR, ChartParams(
                x=result_pd['age'],
                y=result_pd['best_score'],
                fig_title=title,
                fig_size=(20, 10),
                x_label='Wiek',
                y_label='Wynik',
                bar_width=0.3,
            ), save_visualization)

    @staticmethod
    def __save_to_file(data: pd.DataFrame, title: str) -> None:
        filename = title.replace(' ', '_')
        filename = unidecode(filename)
        filename = f"{filename}.csv"

        data.to_csv(f'{Analyzer.results_dir}/{filename}', index=False)
