class SqlQueries:
    mean_score_by_fav_game_type = """
        SELECT i.favourite_game_type AS fav_game_type, AVG(g.score) AS mean_score
        FROM game g
        JOIN `user` u ON g.user_id = u.id
        JOIN initial_survey i ON u.id = i.user_id
        WHERE u.roles NOT LIKE '%ROLE_ADMIN%'
        GROUP BY i.favourite_game_type
    """