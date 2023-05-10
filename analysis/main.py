import mysql.connector as mc

from Analyzer import Analyzer

if __name__ == '__main__':
    with mc.connect(
        user='root',
        password='12345678',
        host='127.0.0.1',
        database='spadajace_kwadraciki',
        port='3306',
    ) as connection:
        analyzer = Analyzer(connection)

        analyzer.mean_score_by_fav_game_type()
        analyzer.dependency_score_on_time()
        analyzer.best_score_by_age()
        analyzer.best_score_by_fav_game_type_with_game_count()
        analyzer.count_of_rejected_scores()
        analyzer.mean_score_by_age()
        analyzer.count_of_preferred_playing_style()
        analyzer.mean_accurate_by_fav_game_type()
        analyzer.mean_accurate_by_preferred_playing_style_with_best_score()
