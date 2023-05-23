from abc import abstractmethod


class SqlQueries:
    def __init__(self):
        self._from_game_join_user_survey = """
            FROM game g
            JOIN `user` u ON g.user_id = u.id
            JOIN initial_survey i ON u.id = i.user_id
            WHERE u.roles NOT LIKE '%ROLE_ADMIN%'
        """

    def time_and_score(self) -> str:
        return f"""
            SELECT g.time AS time, g.score AS score, i.favourite_game_type AS fav_game_type
            {self._from_game_join_user_survey}
        """

    def count_of_rejected_scores(self) -> str:
        return f"""
            SELECT COUNT(g.score) AS count_of_rejected_scores
            {self._from_game_join_user_survey}
                AND g.score <= 100
        """

    def count_of_preferred_playing_style(self) -> str:
        return f"""
            SELECT i.preferred_playing_style AS preferred_playing_style, COUNT(i.preferred_playing_style) AS style_count
            {self._from_game_join_user_survey}
            GROUP BY i.preferred_playing_style
        """

    def mean_accurate_by_preferred_playing_style_with_best_score(self) -> str:
        return f"""
            SELECT 
                i.preferred_playing_style AS preferred_playing_style, 
                ((COUNT(s.miss_shots) - SUM(s.miss_shots)) / COUNT(s.miss_shots)) * 100 AS accurate, 
                MAX(g.score) as best_score
            FROM game g
            JOIN `user` u ON g.user_id = u.id
            JOIN initial_survey i ON u.id = i.user_id
            JOIN square s ON s.game_id = g.id
            WHERE u.roles NOT LIKE '%ROLE_ADMIN%'
                AND g.score > 100
            GROUP BY i.preferred_playing_style
        """

    def accurate_by_score_with_gender(self) -> str:
        return f"""
            SELECT 
                g.score AS score,
                (
                    SELECT ((COUNT(s.miss_shots) - SUM(s.miss_shots)) / COUNT(s.miss_shots)) * 100
                    FROM square s
                    WHERE s.game_id = g.id
                ) AS accurate,
                i.gender AS gender
            {self._from_game_join_user_survey}
                AND g.score > 100
        """

    def accurate_by_score_with_fav_game_type(self) -> str:
        return f"""
            SELECT 
                g.score AS score,
                (
                    SELECT ((COUNT(s.miss_shots) - SUM(s.miss_shots)) / COUNT(s.miss_shots)) * 100
                    FROM square s
                    WHERE s.game_id = g.id
                ) AS accurate,
                i.favourite_game_type as fav_game_type
            {self._from_game_join_user_survey}
                AND g.score > 100
        """

    def mediocre_game_count_to_best_score_on_fav_game_type(self) -> str:
        return f"""
            SELECT
                user_id,
                COUNT(*) AS game_count,
                MAX(score) AS best_score,
                (
                    SELECT COUNT(*) + 1
                    FROM game g2
                    WHERE g2.user_id = g1.user_id AND g2.score > g1.score
                ) AS best_game_order
            FROM
                game g1
            GROUP BY
                user_id
        """

    def mean_time_to_click_by_square_size(self) -> str:
        return f"""
            SELECT 
                s.size AS square_size,
                AVG(s.time_to_click) as mean_time_to_click
            FROM game g
            JOIN `user` u ON g.user_id = u.id
            JOIN initial_survey i ON u.id = i.user_id
            JOIN square s ON s.game_id = g.id
            WHERE u.roles NOT LIKE '%ROLE_ADMIN%'
                AND g.score > 100
                AND s.time_to_click IS NOT NULL
            GROUP BY s.size
        """

    def mean_time_to_click_by_square_velocity(self) -> str:
        return f"""
            SELECT 
                s.time_to_fall AS time_to_fall,
                AVG(s.time_to_click) as mean_time_to_click
            FROM game g
            JOIN `user` u ON g.user_id = u.id
            JOIN initial_survey i ON u.id = i.user_id
            JOIN square s ON s.game_id = g.id
            WHERE u.roles NOT LIKE '%ROLE_ADMIN%'
                AND g.score > 100
                AND s.time_to_click IS NOT NULL
            GROUP BY s.time_to_fall
        """

    def squares_size_and_time_to_fall_taking_away_hp(self) -> str:
        return f"""
            SELECT 
                s.size AS size,
                s.time_to_fall AS time_to_fall
            FROM game g
            JOIN `user` u ON g.user_id = u.id
            JOIN initial_survey i ON u.id = i.user_id
            JOIN square s ON s.game_id = g.id
            WHERE u.roles NOT LIKE '%ROLE_ADMIN%'
                AND g.score > 100
                AND s.time_to_click IS NULL
                AND s.status = 'OUT_OF_BOARD'
        """

    def clicked_squares_size_and_time_to_fall_and_time_to_click(self, category: str) -> str:
        return f"""
            SELECT 
                s.size AS size,
                s.time_to_fall AS time_to_fall,
                s.time_to_click AS time_to_click,
                i.{category} AS {category}
            FROM game g
            JOIN `user` u ON g.user_id = u.id
            JOIN initial_survey i ON u.id = i.user_id
            JOIN square s ON s.game_id = g.id
            WHERE u.roles NOT LIKE '%ROLE_ADMIN%'
                AND g.score > 100
                AND s.time_to_click IS NOT NULL
        """

    def uniques_category_from_survey(self, category: str) -> str:
        return f"""
            SELECT DISTINCT {category} AS {category}
            FROM initial_survey
        """

    def time_spend_on_gaming_by_category(self, category: str) -> str:
        return f"""
            SELECT i.{category}, i.gaming_per_day AS gaming_per_day
            {self._from_game_join_user_survey}
                AND g.score > 100
        """

    def time_spend_on_computer_by_category(self, category: str) -> str:
        return f"""
            SELECT i.{category}, i.computer_usage_per_day AS computer_usage_per_day
            {self._from_game_join_user_survey}
                AND g.score > 100
        """

    def median_accurate_by_category(self, category: str) -> str:
        return f"""
            SELECT 
                i.age AS age, 
                ((COUNT(s.miss_shots) - SUM(s.miss_shots)) / COUNT(s.miss_shots)) * 100 AS accurate
            FROM game g
            JOIN `user` u ON g.user_id = u.id
            JOIN initial_survey i ON u.id = i.user_id
            JOIN square s ON s.game_id = g.id
            WHERE u.roles NOT LIKE '%ROLE_ADMIN%'
                AND g.score > 100
            GROUP BY i.age
        """

    @abstractmethod
    def best_score(self) -> str:
        ...

    @abstractmethod
    def mean_score(self) -> str:
        ...

    @abstractmethod
    def time_to_click(self) -> str:
        ...

    @abstractmethod
    def time_to_click_by_square_size(self) -> str:
        ...

    @abstractmethod
    def time_to_click_by_square_velocity(self) -> str:
        ...

    @abstractmethod
    def best_score_with_game_count(self) -> str:
        ...

    @abstractmethod
    def accurate(self) -> str:
        ...

    @abstractmethod
    def count_of_games_to_best_score(self) -> str:
        ...

    @abstractmethod
    def score_with_class(self) -> str:
        ...
