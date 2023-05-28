import os
from abc import abstractmethod

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mysql.connector.abstracts import MySQLConnectionAbstract
from text_unidecode import unidecode

from ChartTypeEnum import ChartTypeEnum
from ChartParams import ChartParams
from ChartVisualizer import ChartVisualizer
from SqlQueries.SqlQueries import SqlQueries


class Analyzer:
    results_dir = './results/data'
    small_square_border = 60
    fast_square_border = 6.5

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

        small_fast_squares_count = result_pd[(result_pd['size'] < self.small_square_border) & (result_pd['time_to_fall'] < self.fast_square_border)].shape[0]
        big_fast_squares_count = result_pd[(result_pd['size'] >= self.small_square_border) & (result_pd['time_to_fall'] < self.fast_square_border)].shape[0]

        small_slow_squares_count = result_pd[(result_pd['size'] < self.small_square_border) & (result_pd['time_to_fall'] >= self.fast_square_border)].shape[0]
        big_slow_squares_count = result_pd[(result_pd['size'] >= self.small_square_border) & (result_pd['time_to_fall'] >= self.fast_square_border)].shape[0]

        new_result = pd.DataFrame([
            [small_slow_squares_count, small_fast_squares_count],
            [big_slow_squares_count, big_fast_squares_count]
        ], columns=['slow', 'fast'], index=['small', 'big'])

        if show_result:
            print(new_result.to_markdown())

        if result_to_file:
            Analyzer._save_to_file(new_result, title)

    def mean_time_to_click_squares_by_size_and_time_to_fall(self, selected_category: str, show_result: bool = True, result_to_file: bool = True) -> None:
        uniques_categories = pd.read_sql(self.sql_queries.uniques_category_from_survey(selected_category), self.connection)[selected_category]
        result_pd = pd.read_sql(self.sql_queries.clicked_squares_size_and_time_to_fall_and_time_to_click(selected_category), self.connection)
        title = f'Średni czas do kliknięcia kwadratów z podziałem na rozmiar oraz szybkość w zależności od {self.translate_category(selected_category, True)}'

        new_result = np.empty((uniques_categories.shape[0], 5), dtype=object)

        for index, unique_category in uniques_categories.items():
            filtered_result = result_pd[result_pd[selected_category] == unique_category]

            avg_time_to_click_on_small = filtered_result[filtered_result['size'] < self.small_square_border]['time_to_click'].mean()
            avg_time_to_click_on_big = filtered_result[filtered_result['size'] >= self.small_square_border]['time_to_click'].mean()

            avg_time_to_click_on_slow = filtered_result[filtered_result['time_to_fall'] >= self.fast_square_border]['time_to_click'].mean()
            avg_time_to_click_on_fast = filtered_result[filtered_result['time_to_fall'] < self.fast_square_border]['time_to_click'].mean()

            new_result[index] = np.array([
                avg_time_to_click_on_small,
                avg_time_to_click_on_big,
                avg_time_to_click_on_slow,
                avg_time_to_click_on_fast,
                unique_category,
            ])

        new_result = pd.DataFrame(
            new_result,
            columns=[
                f'small < {self.small_square_border}px',
                f'big >= {self.small_square_border}px',
                f'slow < {self.fast_square_border}s',
                f'fast >= {self.fast_square_border}s',
                selected_category
            ]
        )
        new_result = new_result.drop(selected_category, axis=1).applymap(lambda x: float(x))
        new_result[selected_category] = uniques_categories
        # new_result = new_result.dropna()

        sub_dir = selected_category.replace("_", "-").replace("favourite", "fav")

        if show_result:
            print(new_result.to_markdown())

        if result_to_file:
            Analyzer._save_to_file(new_result, title, sub_dir)

        ax = new_result.plot(
            x=selected_category,
            kind='bar',
            stacked=False,
            figsize=(20, 10),
            title=title,
            ylabel='Średni czas do kliknięcia [s]',
            rot=30,
        )
        for p in ax.patches:
            ax.annotate(f'{p.get_height():.2f}', (p.get_x() * 1.005, p.get_height() * 1.005), fontsize=8)

        filename = ChartVisualizer.save_encode_filename(title)
        plt.savefig(f'./results/images/{sub_dir}/{filename}')
        plt.savefig(f'./results/pdf/{sub_dir}/{filename.replace("png", "pdf")}', format="pdf", bbox_inches="tight")

        plt.close()

    def median_time_to_click_squares_by_size_and_time_to_fall(self, selected_category: str, show_result: bool = True, result_to_file: bool = True) -> None:
        uniques_categories = pd.read_sql(self.sql_queries.uniques_category_from_survey(selected_category), self.connection)[selected_category]
        result_pd = pd.read_sql(
            self.sql_queries.clicked_squares_size_and_time_to_fall_and_time_to_click(selected_category),
            self.connection
        )
        title = f'Mediana czasu do kliknięcia kwadratów z podziałem na rozmiar oraz szybkość w zależności od {self.translate_category(selected_category, True)}'

        new_result = np.empty((uniques_categories.shape[0], 5), dtype=object)

        for index, unique_category in uniques_categories.items():
            filtered_result = result_pd[result_pd[selected_category] == unique_category]

            avg_time_to_click_on_small = filtered_result[filtered_result['size'] < self.small_square_border][
                'time_to_click'].median()
            avg_time_to_click_on_big = filtered_result[filtered_result['size'] >= self.small_square_border][
                'time_to_click'].median()

            avg_time_to_click_on_slow = filtered_result[filtered_result['time_to_fall'] >= self.fast_square_border][
                'time_to_click'].median()
            avg_time_to_click_on_fast = filtered_result[filtered_result['time_to_fall'] < self.fast_square_border][
                'time_to_click'].median()

            new_result[index] = np.array([
                avg_time_to_click_on_small,
                avg_time_to_click_on_big,
                avg_time_to_click_on_slow,
                avg_time_to_click_on_fast,
                unique_category,
            ])

        new_result = pd.DataFrame(
            new_result,
            columns=[
                f'small < {self.small_square_border}px',
                f'big >= {self.small_square_border}px',
                f'slow < {self.fast_square_border}s',
                f'fast >= {self.fast_square_border}s',
                selected_category
            ]
        )
        new_result = new_result.drop(selected_category, axis=1).applymap(lambda x: float(x))
        new_result[selected_category] = uniques_categories
        # new_result = new_result.dropna()

        sub_dir = selected_category.replace("_", "-").replace("favourite", "fav")

        if show_result:
            print(new_result.to_markdown())

        if result_to_file:
            Analyzer._save_to_file(new_result, title, sub_dir)

        ax = new_result.plot(
            x=selected_category,
            kind='bar',
            stacked=False,
            figsize=(20, 10),
            title=title,
            ylabel='Mediana czasu do kliknięcia [s]',
            rot=30,
        )
        for p in ax.patches:
            ax.annotate(f'{p.get_height():.2f}', (p.get_x() * 1.005, p.get_height() * 1.005), fontsize=8)

        filename = ChartVisualizer.save_encode_filename(title)
        plt.savefig(f'./results/images/{sub_dir}/{filename}')
        plt.savefig(f'./results/pdf/{sub_dir}/{filename.replace("png", "pdf")}', format="pdf", bbox_inches="tight")

        plt.close()

    def mean_time_spending_on_gaming_by_category(self, selected_category: str, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(
            self.sql_queries.time_spend_on_gaming_by_category(selected_category),
            self.connection
        )
        result_pd = result_pd.groupby(selected_category)['gaming_per_day'].mean()
        title = f'Średnia czasu spędzanego na granie dziennie w zależności od {self.translate_category(selected_category, True)}'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer._save_to_file(result_pd, title, sub_dir=selected_category)

        if visualize or save_visualization:
            ChartVisualizer.visualize(ChartTypeEnum.BAR, ChartParams(
                x=result_pd.keys(),
                y=result_pd.values,
                fig_title=title,
                fig_size=(20, 10),
                x_label=self.translate_category(selected_category).capitalize(),
                y_label='Średnia czasu spędzanego na granie dziennie [h]',
            ), save_visualization, sub_dir=selected_category)

    def median_time_spending_on_gaming_by_category(self, selected_category: str, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(
            self.sql_queries.time_spend_on_gaming_by_category(selected_category),
            self.connection
        )
        result_pd = result_pd.groupby(selected_category)['gaming_per_day'].median()
        title = f'Mediana czasu spędzanego na granie dziennie w zależności od {self.translate_category(selected_category, True)}'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer._save_to_file(result_pd, title, sub_dir=selected_category)

        if visualize or save_visualization:
            ChartVisualizer.visualize(ChartTypeEnum.BAR, ChartParams(
                x=result_pd.keys(),
                y=result_pd.values,
                fig_title=title,
                fig_size=(20, 10),
                x_label=self.translate_category(selected_category).capitalize(),
                y_label='Mediana czasu spędzanego na granie dziennie [h]',
            ), save_visualization, sub_dir=selected_category)

    def mean_time_using_computer_by_category(self, selected_category: str, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(
            self.sql_queries.time_spend_on_computer_by_category(selected_category),
            self.connection
        )
        result_pd = result_pd.groupby(selected_category)['computer_usage_per_day'].mean()
        title = f'Średnia liczba godzin używania komputera dziennie w zależności od {self.translate_category(selected_category, True)}'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer._save_to_file(result_pd, title, sub_dir=selected_category)

        if visualize or save_visualization:
            ChartVisualizer.visualize(ChartTypeEnum.BAR, ChartParams(
                x=result_pd.keys(),
                y=result_pd.values,
                fig_title=title,
                fig_size=(20, 10),
                x_label=self.translate_category(selected_category).capitalize(),
                y_label='Średnia liczba godzin używania komputera dziennie [h]',
            ), save_visualization, sub_dir=selected_category)

    def median_time_using_computer_by_category(self, selected_category: str, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(
            self.sql_queries.time_spend_on_computer_by_category(selected_category),
            self.connection
        )
        result_pd = result_pd.groupby(selected_category)['computer_usage_per_day'].median()
        title = f'Mediana liczby godzin używania komputera dziennie w zależności od {self.translate_category(selected_category, True)}'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer._save_to_file(result_pd, title, sub_dir=selected_category)

        if visualize or save_visualization:
            ChartVisualizer.visualize(ChartTypeEnum.BAR, ChartParams(
                x=result_pd.keys(),
                y=result_pd.values,
                fig_title=title,
                fig_size=(20, 10),
                x_label=self.translate_category(selected_category).capitalize(),
                y_label='Mediana liczba godzin używania komputera dziennie [h]',
            ), save_visualization, sub_dir=selected_category)

    def median_accurate_by_category(self, selected_category: str, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> None:
        result_pd = pd.read_sql(
            self.sql_queries.time_spend_on_computer_by_category(selected_category),
            self.connection
        )
        result_pd = result_pd.groupby(selected_category)['computer_usage_per_day'].median()
        title = f'Mediana liczby godzin używania komputera dziennie w zależności od {self.translate_category(selected_category, True)}'

        if show_result:
            print(result_pd.to_markdown())

        if result_to_file:
            Analyzer._save_to_file(result_pd, title, sub_dir=selected_category)

        if visualize or save_visualization:
            ChartVisualizer.visualize(ChartTypeEnum.BAR, ChartParams(
                x=result_pd.keys(),
                y=result_pd.values,
                fig_title=title,
                fig_size=(20, 10),
                x_label=self.translate_category(selected_category).capitalize(),
                y_label='Mediana liczba godzin używania komputera dziennie [h]',
            ), save_visualization, sub_dir=selected_category)

    @staticmethod
    def _save_to_file(data: pd.DataFrame, title: str, sub_dir: str = None) -> None:
        filename = title.replace(' ', '_')
        filename = unidecode(filename)
        filename = f"{filename}.csv"

        sub_dir = f'/{sub_dir}' if sub_dir is not None else ''
        sub_dir = sub_dir.replace("_", "-").replace("favourite", "fav")
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
    def median_time_to_click(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True,
                             save_visualization: bool = True) -> None:
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
    def median_accurate(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True,
                        save_visualization: bool = True) -> None:
        ...

    @abstractmethod
    def count_of_games_to_best_score(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> str:
        ...

    @abstractmethod
    def median_of_score(self, show_result: bool = True, result_to_file: bool = True, visualize: bool = True, save_visualization: bool = True) -> str:
        ...

    @staticmethod
    def translate_category(category: str, in_dependent: bool = False) -> str:
        if category == 'favourite_game_type':
            return ('typu' if in_dependent else 'typ') + 'ulubionej gry'

        if category == 'gender':
            return 'płci' if in_dependent else 'płeć'

        if category == 'age':
            return 'wieku' if in_dependent else 'wiek'

        return category
