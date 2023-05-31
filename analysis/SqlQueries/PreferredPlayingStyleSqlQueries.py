from SqlQueries.SqlQueries import SqlQueries


class PreferredPlayingStyleSqlQueries(SqlQueries):
    def best_score(self) -> str:
        return f"""
            SELECT i.preferred_playing_style AS preferred_playing_style, MAX(g.score) AS best_score
            {self._from_game_join_user_survey}
            GROUP BY i.preferred_playing_style
        """

    def mean_score(self) -> str:
        return f"""
            SELECT i.preferred_playing_style AS preferred_playing_style, AVG(g.score) as mean_score
            {self._from_game_join_user_survey}
                AND g.score > 100
            GROUP BY i.preferred_playing_style
        """

    def time_to_click(self) -> str:
        return f"""
            SELECT i.preferred_playing_style AS preferred_playing_style, s.time_to_click AS time_to_click
            FROM game g
            JOIN `user` u ON g.user_id = u.id
            JOIN initial_survey i ON u.id = i.user_id
            JOIN square s ON s.game_id = g.id
            WHERE u.roles NOT LIKE '%ROLE_ADMIN%'
                AND g.score > 100
                AND s.time_to_click IS NOT NULL
            GROUP BY s.id
        """

    def mean_time_to_click_by_square_size(self) -> str:
        return f"""
            SELECT 
                i.preferred_playing_style AS preferred_playing_style,
                AVG(s.time_to_click) AS time_to_click,
                s.size AS square_size
            FROM game g
            JOIN `user` u ON g.user_id = u.id
            JOIN initial_survey i ON u.id = i.user_id
            JOIN square s ON s.game_id = g.id
            WHERE u.roles NOT LIKE '%ROLE_ADMIN%'
                AND g.score > 100
                AND s.time_to_click IS NOT NULL
            GROUP BY s.size, i.preferred_playing_style
        """

    def mean_time_to_click_by_square_velocity(self) -> str:
        return f"""
            SELECT 
                i.preferred_playing_style AS preferred_playing_style,
                AVG(s.time_to_click) AS time_to_click,
                s.time_to_fall AS time_to_fall
            FROM game g
            JOIN `user` u ON g.user_id = u.id
            JOIN initial_survey i ON u.id = i.user_id
            JOIN square s ON s.game_id = g.id
            WHERE u.roles NOT LIKE '%ROLE_ADMIN%'
                AND g.score > 100
                AND s.time_to_click IS NOT NULL
            GROUP BY s.size, i.preferred_playing_style
        """

    def best_score_with_game_count(self) -> str:
        return f"""
            SELECT i.preferred_playing_style AS preferred_playing_style, MAX(g.score) AS best_score, COUNT(g.score) AS game_count
            {self._from_game_join_user_survey}
                AND g.score > 100
            GROUP BY i.preferred_playing_style
        """

    def accurate(self) -> str:
        return f"""
            SELECT
                i.preferred_playing_style AS preferred_playing_style,
                ((COUNT(s.miss_shots) - SUM(s.miss_shots)) / COUNT(s.miss_shots)) * 100 AS accurate
            FROM game g
                 JOIN `user` u ON g.user_id = u.id
                 JOIN initial_survey i ON u.id = i.user_id
                 JOIN square s ON s.game_id = g.id
            WHERE u.roles NOT LIKE '%ROLE_ADMIN%'
              AND g.score > 100
            GROUP BY g.id
        """

    def count_of_games_to_best_score(self) -> str:
        return f"""
            SELECT i.preferred_playing_style AS preferred_playing_style, (
                SELECT COUNT(g2.id)
                FROM game g2
                WHERE g2.user_id = u.id
            ) AS game_count, g.score, u.id
            {self._from_game_join_user_survey}
                AND g.score IN (
                    SELECT MAX(g.score) 
                    {self._from_game_join_user_survey}
                    GROUP BY i.preferred_playing_style
                )
            GROUP BY i.preferred_playing_style
        """

    def score_with_class(self) -> str:
        return f"""
            SELECT g.score AS score, i.preferred_playing_style AS preferred_playing_style
            {self._from_game_join_user_survey}
                AND g.score > 100
        """
