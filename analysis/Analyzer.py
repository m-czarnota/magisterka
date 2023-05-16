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

    def mean_time_to_click_by_fav_game_type(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(SqlQueries.mean_time_to_click_by_fav_game_type, self.connection)
        title = 'Średni czas do kliknięcia na typ ulubionej gry'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer.__save_to_file(result_pd, title)

        if visualize or save_visualization:
            ChartVisualizer.visualize(ChartTypeEnum.BAR, ChartParams(
                x=result_pd['fav_game_type'],
                y=result_pd['mean_time'],
                fig_title=title,
                fig_size=(20, 10),
                x_label='Typ ulubionej gry',
                y_label='Średni czas do kliknięcia [s]',
                bar_width=0.3,
            ), save_visualization)

    def mean_time_to_click_by_age(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(SqlQueries.mean_time_to_click_by_age, self.connection)
        title = 'Średni czas do kliknięcia na wiek'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer.__save_to_file(result_pd, title)

        if visualize or save_visualization:
            ChartVisualizer.visualize(ChartTypeEnum.BAR, ChartParams(
                x=result_pd['age'],
                y=result_pd['mean_time'],
                fig_title=title,
                fig_size=(20, 10),
                x_label='Wiek',
                y_label='Średni czas do kliknięcia [s]',
                bar_width=0.3,
            ), save_visualization)

    def count_of_games_to_best_score_by_fav_game_type(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(SqlQueries.count_of_games_to_best_score_by_fav_game_type, self.connection)
        title = 'Liczba gier do osiągnięcia najwyższego wyniku na typ ulubionej gry'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer.__save_to_file(result_pd, title)

        if visualize or save_visualization:
            ChartVisualizer.visualize(ChartTypeEnum.BAR, ChartParams(
                x=result_pd['fav_game_type'],
                y=result_pd['game_count'],
                fig_title=title,
                fig_size=(20, 10),
                x_label='Typ ulubionej gry',
                y_label='Liczba gier',
                bar_width=0.3,
            ), save_visualization)

    def accurate_by_score_with_gender(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(SqlQueries.accurate_by_score_with_gender, self.connection)
        title = 'Zależność celności od liczby punktów z podziałem na płeć'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer.__save_to_file(result_pd, title)

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
        result_pd = pd.read_sql(SqlQueries.accurate_by_score_with_fav_game_type, self.connection)
        title = 'Zależność celności od liczby punktów z podziałem na typ ulubionej gry'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer.__save_to_file(result_pd, title)

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
        result_pd = pd.read_sql(SqlQueries.mediocre_game_count_to_best_score_on_fav_game_type, self.connection)
        title = 'Przeciętna liczba gier do najlepszego wyniku na typ gry'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer.__save_to_file(result_pd, title)

    def time_to_click_by_square_size_by_age(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(SqlQueries.time_to_click_by_square_size_by_age, self.connection)
        title = 'Zależność czasu do kliknięcia kwadratu w zależności od jego rozmiaru na wiek'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer.__save_to_file(result_pd, title)

        if visualize or save_visualization:
            ChartVisualizer.visualize(ChartTypeEnum.SCATTER, ChartParams(
                x=result_pd['square_size'],
                y=result_pd['time_to_click'],
                fig_title=title,
                fig_size=(20, 10),
                x_label='Wielkość kwadratu [px]',
                y_label='Czas do kliknięcia [s]',
                classes=result_pd['age'],
            ), save_visualization)

    def time_to_click_by_square_size_by_fav_game_type(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(SqlQueries.time_to_click_by_square_size_by_fav_game_type, self.connection)
        title = 'Zależność czasu do kliknięcia kwadratu w zależności od jego rozmiaru na typ ulubionej gry'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer.__save_to_file(result_pd, title)

        if visualize or save_visualization:
            ChartVisualizer.visualize(ChartTypeEnum.SCATTER, ChartParams(
                x=result_pd['square_size'],
                y=result_pd['time_to_click'],
                fig_title=title,
                fig_size=(20, 10),
                x_label='Wielkość kwadratu [px]',
                y_label='Czas do kliknięcia [s]',
                classes=result_pd['fav_game_type'],
            ), save_visualization)

    def mean_time_to_click_by_square_size(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(SqlQueries.mean_time_to_click_by_square_size, self.connection)
        title = 'Zależność średniego czasu do kliknięcia kwadratu w zależności od jego rozmiaru'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer.__save_to_file(result_pd, title)

        if visualize or save_visualization:
            ChartVisualizer.visualize(ChartTypeEnum.SCATTER, ChartParams(
                x=result_pd['square_size'],
                y=result_pd['mean_time_to_click'],
                fig_title=title,
                fig_size=(20, 10),
                x_label='Wielkość kwadratu [px]',
                y_label='Średni czas do kliknięcia [s]',
            ), save_visualization)

    def time_to_click_by_square_velocity_by_age(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(SqlQueries.time_to_click_by_square_velocity_by_age, self.connection)
        title = 'Zależność czasu do kliknięcia kwadratu w zależności od jego czasu spadania na wiek'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer.__save_to_file(result_pd, title)

        if visualize or save_visualization:
            ChartVisualizer.visualize(ChartTypeEnum.SCATTER, ChartParams(
                x=result_pd['time_to_fall'],
                y=result_pd['time_to_click'],
                fig_title=title,
                fig_size=(20, 10),
                x_label='Czas do spadnięcia kwadratu [s]',
                y_label='Czas do kliknięcia [s]',
                classes=result_pd['age'],
            ), save_visualization)

    def time_to_click_by_square_velocity_by_fav_game_type(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(SqlQueries.time_to_click_by_square_velocity_by_fav_game_type, self.connection)
        title = 'Zależność czasu do kliknięcia kwadratu w zależności od jego czasu spadania na typ ulubionej gry'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer.__save_to_file(result_pd, title)

        if visualize or save_visualization:
            ChartVisualizer.visualize(ChartTypeEnum.SCATTER, ChartParams(
                x=result_pd['time_to_fall'],
                y=result_pd['time_to_click'],
                fig_title=title,
                fig_size=(20, 10),
                x_label='Czas do spadnięcia kwadratu [s]',
                y_label='Czas do kliknięcia [s]',
                classes=result_pd['fav_game_type'],
            ), save_visualization)

    def mean_time_to_click_by_square_velocity(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(SqlQueries.mean_time_to_click_by_square_velocity, self.connection)
        title = 'Zależność średniego czasu do kliknięcia kwadratu w zależności od jego czasu spadania'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer.__save_to_file(result_pd, title)

        if visualize or save_visualization:
            ChartVisualizer.visualize(ChartTypeEnum.SCATTER, ChartParams(
                x=result_pd['time_to_fall'],
                y=result_pd['mean_time_to_click'],
                fig_title=title,
                fig_size=(20, 10),
                x_label='Czas do spadnięcia kwadratu [s]',
                y_label='Średni czas do kliknięcia [s]',
            ), save_visualization)

    def median_of_score_by_fav_game_type(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(SqlQueries.score_with_fav_game_type, self.connection)
        result_pd = result_pd.groupby('fav_game_type')['score'].median()
        title = 'Mediana wyniku na typ ulubionej gry'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer.__save_to_file(result_pd, title)

        if visualize or save_visualization:
            ChartVisualizer.visualize(ChartTypeEnum.BAR, ChartParams(
                x=result_pd.keys(),
                y=result_pd.values,
                fig_title=title,
                fig_size=(20, 10),
                x_label='Typ ulubionej gry',
                y_label='Mediana wyniku',
            ), save_visualization)

    def squares_size_and_time_to_fall_taking_away_hp(self, show_result: bool = True, result_to_file: bool = True) -> None:
        result_pd = pd.read_sql(SqlQueries.squares_size_and_time_to_fall_taking_away_hp, self.connection)
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
            Analyzer.__save_to_file(new_result, title)

    @staticmethod
    def __save_to_file(data: pd.DataFrame, title: str) -> None:
        filename = title.replace(' ', '_')
        filename = unidecode(filename)
        filename = f"{filename}.csv"

        data.to_csv(f'{Analyzer.results_dir}/{filename}', index=False)
