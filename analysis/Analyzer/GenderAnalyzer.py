import pandas as pd
from mysql.connector.abstracts import MySQLConnectionAbstract

from Analyzer.Analyzer import Analyzer
from ChartParams import ChartParams
from ChartTypeEnum import ChartTypeEnum
from ChartVisualizer import ChartVisualizer
from SqlQueries.GenderSqlQueries import GenderSqlQueries


class GenderAnalyzer(Analyzer):   
    def __init__(self, connection: MySQLConnectionAbstract):
        super().__init__(connection)

        self.sql_queries = GenderSqlQueries()
        self._sub_dir = 'gender'

    def best_score(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True,
                   save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(self.sql_queries.best_score(), self.connection)
        title = 'Najlepszy wynik na grupę płciową'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer._save_to_file(result_pd, title, sub_dir=self._sub_dir)

        if visualize or save_visualization:
            ChartVisualizer.visualize(ChartTypeEnum.BAR, ChartParams(
                x=result_pd['gender'],
                y=result_pd['best_score'],
                fig_title=title,
                fig_size=(20, 10),
                x_label='Płeć',
                y_label='Liczba punktów',
                bar_width=0.3,
            ), save_visualization, sub_dir=self._sub_dir)

    def mean_score(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True,
                   save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(self.sql_queries.mean_score(), self.connection)
        title = 'Średnia liczba punktów na płeć'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer._save_to_file(result_pd, title, sub_dir=self._sub_dir)

        if visualize or save_visualization:
            ChartVisualizer.visualize(ChartTypeEnum.BAR, ChartParams(
                x=result_pd['gender'],
                y=result_pd['mean_score'],
                fig_title=title,
                fig_size=(20, 10),
                x_label='Płeć',
                y_label='Liczba punktów',
                bar_width=0.3,
            ), save_visualization, sub_dir=self._sub_dir)

    def mean_time_to_click(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True,
                           save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(self.sql_queries.time_to_click(), self.connection)
        result_pd = result_pd.groupby('gender')['time_to_click'].mean()
        title = 'Średni czas do kliknięcia na płeć'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer._save_to_file(result_pd, title, sub_dir=self._sub_dir)

        if visualize or save_visualization:
            ChartVisualizer.visualize(ChartTypeEnum.BAR, ChartParams(
                x=result_pd.keys(),
                y=result_pd.values,
                fig_title=title,
                fig_size=(20, 10),
                x_label='Płeć',
                y_label='Średni czas do kliknięcia [s]',
                bar_width=0.3,
            ), save_visualization, sub_dir=self._sub_dir)

    def median_time_to_click(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True,
                           save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(self.sql_queries.time_to_click(), self.connection)
        result_pd = result_pd.groupby('gender')['time_to_click'].median()
        title = 'Mediana czasu do kliknięcia na płeć'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer._save_to_file(result_pd, title, sub_dir=self._sub_dir)

        if visualize or save_visualization:
            ChartVisualizer.visualize(ChartTypeEnum.BAR, ChartParams(
                x=result_pd.keys(),
                y=result_pd.values,
                fig_title=title,
                fig_size=(20, 10),
                x_label='Płeć',
                y_label='Mediana czasu do kliknięcia [s]',
                bar_width=0.3,
            ), save_visualization, sub_dir=self._sub_dir)

    def mean_time_to_click_by_square_size(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(self.sql_queries.mean_time_to_click_by_square_size(), self.connection)
        title = 'Zależność średniego czasu do kliknięcia kwadratu w zależności od jego rozmiaru na typ płeć'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer._save_to_file(result_pd, title, sub_dir=self._sub_dir)

        if visualize or save_visualization:
            ChartVisualizer.visualize(ChartTypeEnum.SCATTER, ChartParams(
                x=result_pd['square_size'],
                y=result_pd['time_to_click'],
                fig_title=title,
                fig_size=(20, 10),
                x_label='Wielkość kwadratu [px]',
                y_label='Średni czas do kliknięcia [s]',
                classes=result_pd['gender'],
                line_in_mean=True,
            ), save_visualization, sub_dir=self._sub_dir)

    def mean_time_to_click_by_square_velocity(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(self.sql_queries.mean_time_to_click_by_square_velocity(), self.connection)
        title = 'Zależność średniego czasu do kliknięcia kwadratu w zależności od jego czasu spadania na płeć'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer._save_to_file(result_pd, title, sub_dir=self._sub_dir)

        if visualize or save_visualization:
            ChartVisualizer.visualize(ChartTypeEnum.SCATTER, ChartParams(
                x=result_pd['time_to_fall'],
                y=result_pd['time_to_click'],
                fig_title=title,
                fig_size=(20, 10),
                x_label='Czas do spadnięcia kwadratu [s]',
                y_label='Średni czas do kliknięcia [s]',
                classes=result_pd['gender'],
                line_in_mean=True,
            ), save_visualization, sub_dir=self._sub_dir)

    def best_score_with_game_count(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True,
                                   save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(self.sql_queries.best_score_with_game_count(), self.connection)
        title = 'Najlepszy wynik na płeć z liczbą gier'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer._save_to_file(result_pd, title, sub_dir=self._sub_dir)

        if visualize or save_visualization:
            x = [f'{fav_game_type} / {count}' for fav_game_type, count in
                 zip(result_pd['gender'], result_pd['game_count'])]

            ChartVisualizer.visualize(ChartTypeEnum.BAR, ChartParams(
                x=x,
                y=result_pd['best_score'],
                fig_title=title,
                fig_size=(20, 10),
                x_label='Płeć / Liczba gier',
                y_label='Liczba punktów',
                bar_width=0.3,
            ), save_visualization, sub_dir=self._sub_dir)

    def mean_accurate(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True,
                      save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(self.sql_queries.accurate(), self.connection)
        result_pd = result_pd.groupby('gender')['accurate'].mean()
        title = 'Średnia celność na płeć'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer._save_to_file(result_pd, title, sub_dir=self._sub_dir)

        if visualize or save_visualization:
            ChartVisualizer.visualize(ChartTypeEnum.BAR, ChartParams(
                x=result_pd.keys(),
                y=result_pd.values,
                fig_title=title,
                fig_size=(20, 10),
                x_label='Płeć',
                y_label='Średnia celność [%]',
                bar_width=0.3,
            ), save_visualization, sub_dir=self._sub_dir)

    def median_accurate(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True,
                      save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(self.sql_queries.accurate(), self.connection)
        result_pd = result_pd.groupby('gender')['accurate'].median()
        title = 'Mediana celności na płeć'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer._save_to_file(result_pd, title, sub_dir=self._sub_dir)

        if visualize or save_visualization:
            ChartVisualizer.visualize(ChartTypeEnum.BAR, ChartParams(
                x=result_pd.keys(),
                y=result_pd.values,
                fig_title=title,
                fig_size=(20, 10),
                x_label='Płeć',
                y_label='Mediana celności [%]',
                bar_width=0.3,
            ), save_visualization, sub_dir=self._sub_dir)

    def count_of_games_to_best_score(self, show_result: bool = True, result_to_file: bool = True,
                                     visualize: bool = True, save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(self.sql_queries.count_of_games_to_best_score(), self.connection)
        title = 'Liczba gier do osiągnięcia najwyższego wyniku na płeć'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer._save_to_file(result_pd, title, sub_dir=self._sub_dir)

        if visualize or save_visualization:
            ChartVisualizer.visualize(ChartTypeEnum.BAR, ChartParams(
                x=result_pd['gender'],
                y=result_pd['game_count'],
                fig_title=title,
                fig_size=(20, 10),
                x_label='Płeć',
                y_label='Liczba gier',
                bar_width=0.3,
            ), save_visualization, sub_dir=self._sub_dir)

    def median_of_score(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True,
                        save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(self.sql_queries.score_with_class(), self.connection)
        result_pd = result_pd.groupby('gender')['score'].median()
        title = 'Mediana wyniku na płeć'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer._save_to_file(result_pd, title, sub_dir=self._sub_dir)

        if visualize or save_visualization:
            ChartVisualizer.visualize(ChartTypeEnum.BAR, ChartParams(
                x=result_pd.keys(),
                y=result_pd.values,
                fig_title=title,
                fig_size=(20, 10),
                x_label='Płeć',
                y_label='Mediana wyniku',
            ), save_visualization, sub_dir=self._sub_dir)
