import os
from abc import abstractmethod

import pandas as pd
from mysql.connector.abstracts import MySQLConnectionAbstract
from text_unidecode import unidecode

from ChartTypeEnum import ChartTypeEnum
from ChartParams import ChartParams
from ChartVisualizer import ChartVisualizer
from SqlQueries.SqlQueries import SqlQueries


class Analyzer:
    results_dir = './results/data'

    def __init__(self, connection: MySQLConnectionAbstract):
        self.connection = connection
        
        self.sql_queries = SqlQueries()

    def dependency_score_on_time(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(self.sql_queries.time_and_score(), self.connection)
        title = 'Zależność wyniku od czasu gry'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer._save_to_file(result_pd, title)

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

    def count_of_rejected_scores(self, show_result: bool = True, result_to_file: bool = True) -> None:
        result_pd = pd.read_sql(self.sql_queries.count_of_rejected_scores(), self.connection)
        title = 'Liczba odrzuconych wyników'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer._save_to_file(result_pd, title)

    def count_of_preferred_playing_style(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(self.sql_queries.count_of_preferred_playing_style(), self.connection)
        title = 'Preferowany stylów grania wśród użytkowników'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer._save_to_file(result_pd, title)

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

    def mean_accurate_by_preferred_playing_style_with_best_score(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(self.sql_queries.mean_accurate_by_preferred_playing_style_with_best_score(), self.connection)
        title = 'Średnia celność na preferowany styl grania'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer._save_to_file(result_pd, title)

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

    def accurate_by_score_with_gender(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(self.sql_queries.accurate_by_score_with_gender(), self.connection)
        title = 'Zależność celności od liczby punktów z podziałem na płeć'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer._save_to_file(result_pd, title)

        if visualize or save_visualization:
            ChartVisualizer.visualize(ChartTypeEnum.SCATTER, ChartParams(
                x=result_pd['score'],
                y=result_pd['accurate'],
                fig_title=title,
                fig_size=(20, 10),
                x_label='Liczba punktów',
                y_label='Celność [%]',
                classes=result_pd['gender'],
            ), save_visualization)

    def accurate_by_score_with_fav_game_type(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(self.sql_queries.accurate_by_score_with_fav_game_type(), self.connection)
        title = 'Zależność celności od liczby punktów z podziałem na typ ulubionej gry'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer._save_to_file(result_pd, title)

        if visualize or save_visualization:
            ChartVisualizer.visualize(ChartTypeEnum.SCATTER, ChartParams(
                x=result_pd['score'],
                y=result_pd['accurate'],
                fig_title=title,
                fig_size=(20, 10),
                x_label='Liczba punktów',
                y_label='Celność [%]',
                classes=result_pd['fav_game_type'],
            ), save_visualization)

    def mediocre_game_count_to_best_score_on_fav_game_type(self, show_result: bool = True, result_to_file: bool = True) -> None:
        result_pd = pd.read_sql(self.sql_queries.mediocre_game_count_to_best_score_on_fav_game_type(), self.connection)
        title = 'Przeciętna liczba gier do najlepszego wyniku na typ gry'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer._save_to_file(result_pd, title)

    def mean_time_to_click_by_square_size(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(self.sql_queries.mean_time_to_click_by_square_size(), self.connection)
        title = 'Zależność średniego czasu do kliknięcia kwadratu w zależności od jego rozmiaru'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer._save_to_file(result_pd, title)

        if visualize or save_visualization:
            ChartVisualizer.visualize(ChartTypeEnum.SCATTER, ChartParams(
                x=result_pd['square_size'],
                y=result_pd['mean_time_to_click'],
                fig_title=title,
                fig_size=(20, 10),
                x_label='Wielkość kwadratu [px]',
                y_label='Średni czas do kliknięcia [s]',
            ), save_visualization)

    def mean_time_to_click_by_square_velocity(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(self.sql_queries.mean_time_to_click_by_square_velocity(), self.connection)
        title = 'Zależność średniego czasu do kliknięcia kwadratu w zależności od jego czasu spadania'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer._save_to_file(result_pd, title)

        if visualize or save_visualization:
            ChartVisualizer.visualize(ChartTypeEnum.SCATTER, ChartParams(
                x=result_pd['time_to_fall'],
                y=result_pd['mean_time_to_click'],
                fig_title=title,
                fig_size=(20, 10),
                x_label='Czas do spadnięcia kwadratu [s]',
                y_label='Średni czas do kliknięcia [s]',
            ), save_visualization)

    def squares_size_and_time_to_fall_taking_away_hp(self, show_result: bool = True, result_to_file: bool = True) -> None:
        result_pd = pd.read_sql(self.sql_queries.squares_size_and_time_to_fall_taking_away_hp(), self.connection)
        title = 'Rozkład kwadratów zabierających punkty życia'

        small_squares_count = result_pd[result_pd['size'] < 60].shape[0]
        big_squares_count = result_pd.shape[0] - small_squares_count

        fast_squares_count = result_pd[result_pd['time_to_fall'] < 7].shape[0]
        slow_squares_count = result_pd.shape[0] - fast_squares_count

        new_result = pd.DataFrame([
            [small_squares_count + slow_squares_count, small_squares_count + fast_squares_count],
            [big_squares_count + slow_squares_count, big_squares_count + fast_squares_count]
        ], columns=['small', 'big'], index=['slow', 'fast'])

        if show_result:
            print(new_result.to_markdown())

        if result_to_file:
            Analyzer._save_to_file(new_result, title)

    @staticmethod
    def _save_to_file(data: pd.DataFrame, title: str, sub_dir: str = None) -> None:
        filename = title.replace(' ', '_')
        filename = unidecode(filename)
        filename = f"{filename}.csv"

        sub_dir = f'/{sub_dir}' if sub_dir is not None else ''
        dir_path = f'{Analyzer.results_dir}{sub_dir}'

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        data.to_csv(f'{Analyzer.results_dir}{sub_dir}/{filename}', index=False)

    @abstractmethod
    def best_score(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> str:
        ...

    @abstractmethod
    def mean_score(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> str:
        ...

    @abstractmethod
    def mean_time_to_click(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> str:
        ...

    @abstractmethod
    def time_to_click_by_square_size(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> str:
        ...

    @abstractmethod
    def time_to_click_by_square_velocity(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> str:
        ...

    @abstractmethod
    def best_score_with_game_count(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> str:
        ...

    @abstractmethod
    def mean_accurate(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> str:
        ...

    @abstractmethod
    def count_of_games_to_best_score(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> str:
        ...

    @abstractmethod
    def median_of_score(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> str:
        ...
