import mysql.connector as mc

from Analyzer.AgeAnalyzer import AgeAnalyzer
from Analyzer.Analyzer import Analyzer
from Analyzer.FavGameTypeAnalyzer import FavGameTypeAnalyzer
from Analyzer.GenderAnalyzer import GenderAnalyzer


def analyze_class(custom_analyzer: Analyzer) -> None:
    custom_analyzer.mean_score()
    custom_analyzer.best_score()
    custom_analyzer.best_score_with_game_count()
    custom_analyzer.mean_accurate()
    custom_analyzer.median_accurate()
    custom_analyzer.mean_time_to_click()
    custom_analyzer.median_time_to_click()
    custom_analyzer.count_of_games_to_best_score()
    custom_analyzer.time_to_click_by_square_size()
    custom_analyzer.time_to_click_by_square_velocity()
    custom_analyzer.median_of_score()
    

if __name__ == '__main__':
    with mc.connect(
        user='root',
        password='12345678',
        host='127.0.0.1',
        database='spadajace_kwadraciki',
        port='3306',
    ) as connection:
        analyzer = Analyzer(connection)

        for class_analyzer in [GenderAnalyzer(connection), AgeAnalyzer(connection), FavGameTypeAnalyzer(connection)]:
            analyze_class(class_analyzer)
        #
        # analyzer.dependency_score_on_time()
        # analyzer.count_of_rejected_scores()
        # analyzer.count_of_preferred_playing_style()
        # analyzer.mean_accurate_by_preferred_playing_style_with_best_score()
        # analyzer.accurate_by_score_with_fav_game_type()
        # analyzer.accurate_by_score_with_gender()
        # analyzer.mediocre_game_count_to_best_score_on_fav_game_type()
        # analyzer.mean_time_to_click_by_square_size()
        # analyzer.mean_time_to_click_by_square_velocity()
        # analyzer.squares_size_and_time_to_fall_taking_away_hp()
        # analyzer.mean_time_to_click_squares_by_size_and_time_to_fall('favourite_game_type')
        # analyzer.median_time_to_click_squares_by_size_and_time_to_fall('favourite_game_type')
        # analyzer.mean_time_to_click_squares_by_size_and_time_to_fall('gender')
        # analyzer.median_time_to_click_squares_by_size_and_time_to_fall('gender')

        # analyzer.mean_time_to_click_squares_by_size_and_time_to_fall('age')
        # analyzer.median_time_to_click_squares_by_size_and_time_to_fall('age')
        # analyzer.mean_time_spending_on_gaming_by_category('age')
        # analyzer.median_time_spending_on_gaming_by_category('age')
        # analyzer.mean_time_using_computer_by_category('age')
        # analyzer.median_time_using_computer_by_category('age')
