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
            x = [f'{fav_game_type} / {count}' for fav_game_type, count in
                 zip(result_pd['fav_game_type'], result_pd['game_count'])]

            ChartVisualizer.visualize(ChartTypeEnum.BAR, ChartParams(
                x=x,
                y=result_pd['mean_score'],
                fig_title=title,
                fig_size=(20, 10),
                x_label='Typ ulubionej gry / Liczba gier',
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
                x_label='Czas gry [s]',
                y_label='Liczba punktów',
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
                y_label='Liczba punktów',
                bar_width=0.3,
            ), save_visualization)

    def best_score_by_fav_game_type_with_game_count(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(SqlQueries.best_score_by_fav_game_type_with_game_count, self.connection)
        title = 'Najlepszy wynik na typ ulubionej gry'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer.__save_to_file(result_pd, title)

        if visualize or save_visualization:
            x = [f'{fav_game_type} / {count}' for fav_game_type, count in
                 zip(result_pd['fav_game_type'], result_pd['game_count'])]

            ChartVisualizer.visualize(ChartTypeEnum.BAR, ChartParams(
                x=x,
                y=result_pd['best_score'],
                fig_title=title,
                fig_size=(20, 10),
                x_label='Typ ulubionej gry / Liczba gier',
                y_label='Liczba punktów',
                bar_width=0.3,
            ), save_visualization)

    def count_of_rejected_scores(self, show_result: bool = True, result_to_file: bool = True) -> None:
        result_pd = pd.read_sql(SqlQueries.count_of_rejected_scores, self.connection)
        title = 'Liczba odrzuconych wyników'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer.__save_to_file(result_pd, title)
            
    def mean_score_by_age(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(SqlQueries.mean_score_by_age, self.connection)
        title = 'Średnia liczba punktów na wiek'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer.__save_to_file(result_pd, title)

        if visualize or save_visualization:
            ChartVisualizer.visualize(ChartTypeEnum.BAR, ChartParams(
                x=result_pd['age'],
                y=result_pd['mean_score'],
                fig_title=title,
                fig_size=(20, 10),
                x_label='Wiek',
                y_label='Liczba punktów',
                bar_width=0.3,
            ), save_visualization)

    def count_of_preferred_playing_style(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(SqlQueries.count_of_preferred_playing_style, self.connection)
        title = 'Preferowany stylów grania wśród użytkowników'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer.__save_to_file(result_pd, title)

        if visualize or save_visualization:
            ChartVisualizer.visualize(ChartTypeEnum.BAR, ChartParams(
                x=result_pd['preferred_playing_style'],
                y=result_pd['style_count'],
                fig_title=title,
                fig_size=(20, 10),
                x_label='Preferowany styl grania',
                y_label='Liczba głosów',
                bar_width=0.3,
            ), save_visualization)

    def mean_accurate_by_fav_game_type(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(SqlQueries.mean_accurate_by_fav_game_type, self.connection)
        title = 'Średnia celność na typ ulubionej gry'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer.__save_to_file(result_pd, title)

        if visualize or save_visualization:
            ChartVisualizer.visualize(ChartTypeEnum.BAR, ChartParams(
                x=result_pd['fav_game_type'],
                y=result_pd['accurate'],
                fig_title=title,
                fig_size=(20, 10),
                x_label='Typ ulubionej gry',
                y_label='Średnia celność [%]',
                bar_width=0.3,
            ), save_visualization)

    def mean_accurate_by_preferred_playing_style_with_best_score(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(SqlQueries.mean_accurate_by_preferred_playing_style_with_best_score, self.connection)
        title = 'Średnia celność na preferowany styl grania'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer.__save_to_file(result_pd, title)

        if visualize or save_visualization:
            x = [f'{game_style} / {score:.4f}' for game_style, score in
                 zip(result_pd['preferred_playing_style'], result_pd['best_score'])]

            ChartVisualizer.visualize(ChartTypeEnum.BAR, ChartParams(
                x=x,
                y=result_pd['accurate'],
                fig_title=title,
                fig_size=(20, 10),
                x_label='Preferowany styl grania / Maksymalna liczba punktów',
                y_label='Średnia celność [%]',
                bar_width=0.3,
                # classes=result_pd['best_score']
            ), save_visualization)

    @staticmethod
    def __save_to_file(data: pd.DataFrame, title: str) -> None:
        filename = title.replace(' ', '_')
        filename = unidecode(filename)
        filename = f"{filename}.csv"

        data.to_csv(f'{Analyzer.results_dir}/{filename}', index=False)
