from SqlQueries.SqlQueries import SqlQueries


class AgeSqlQueries(SqlQueries):
    def best_score(self) -> str:
        return f"""
            SELECT i.age AS age, MAX(g.score) AS best_score
            {self._from_game_join_user_survey}
            GROUP BY i.age
        """

    def mean_score(self) -> str:
        return f"""
            SELECT i.age AS age, AVG(g.score) as mean_score
            {self._from_game_join_user_survey}
                AND g.score > 100
            GROUP BY i.age
        """
    
    def time_to_click(self) -> str:
        return f"""
            SELECT i.age AS age, s.time_to_click AS time_to_click
            FROM game g
            JOIN `user` u ON g.user_id = u.id
            JOIN initial_survey i ON u.id = i.user_id
            JOIN square s ON s.game_id = g.id
            WHERE u.roles NOT LIKE '%ROLE_ADMIN%'
                AND g.score > 100
                AND s.time_to_click IS NOT NULL
            GROUP BY s.id
        """
    
    def time_to_click_by_square_size(self) -> str:
        return f"""
            SELECT 
                i.age AS age,
                s.time_to_click AS time_to_click,
                s.size AS square_size
            FROM game g
            JOIN `user` u ON g.user_id = u.id
            JOIN initial_survey i ON u.id = i.user_id
            JOIN square s ON s.game_id = g.id
            WHERE u.roles NOT LIKE '%ROLE_ADMIN%'
                AND g.score > 100
                AND s.time_to_click IS NOT NULL
            GROUP BY g.id
        """

    def time_to_click_by_square_velocity(self) -> str:
        return f"""
            SELECT 
                i.age AS age,
                s.time_to_click AS time_to_click,
                s.time_to_fall AS time_to_fall
            FROM game g
            JOIN `user` u ON g.user_id = u.id
            JOIN initial_survey i ON u.id = i.user_id
            JOIN square s ON s.game_id = g.id
            WHERE u.roles NOT LIKE '%ROLE_ADMIN%'
                AND g.score > 100
                AND s.time_to_click IS NOT NULL
            GROUP BY g.id
        """

    def best_score_with_game_count(self) -> str:
        return f"""
            SELECT i.age AS age, MAX(g.score) AS best_score, COUNT(g.score) AS game_count
            {self._from_game_join_user_survey}
                AND g.score > 100
            GROUP BY i.age
        """

    def accurate(self) -> str:
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
            GROUP BY g.id
        """

    def count_of_games_to_best_score(self) -> str:
        return f"""
            SELECT i.age AS age, (
                SELECT COUNT(g2.id)
                FROM game g2
                WHERE g2.user_id = u.id
            ) AS game_count, g.score, u.id
            {self._from_game_join_user_survey}
                AND g.score IN (
                    SELECT MAX(g.score) 
                    {self._from_game_join_user_survey}
                    GROUP BY i.age
                )
            GROUP BY i.age
        """

    def score_with_class(self) -> str:
        return f"""
            SELECT g.score AS score, i.age AS age
            {self._from_game_join_user_survey}
                AND g.score > 100
        """
