class SqlQueries:
    mean_score_by_fav_game_type = """
        SELECT i.favourite_game_type AS fav_game_type, AVG(g.score) AS mean_score
        FROM game g
        JOIN `user` u ON g.user_id = u.id
        JOIN initial_survey i ON u.id = i.user_id
        WHERE u.roles NOT LIKE '%ROLE_ADMIN%'
        GROUP BY i.favourite_game_type
    """

    time_and_score = """
        SELECT g.time AS time, g.score AS score, i.favourite_game_type AS fav_game_type
        FROM game g
        JOIN `user` u ON g.user_id = u.id
        JOIN initial_survey i ON u.id = i.user_id
        WHERE u.roles NOT LIKE '%ROLE_ADMIN%'
    """

    best_score_by_age = """
        SELECT i.age AS age, MAX(g.score) AS best_score
        FROM game g
        JOIN `user` u ON g.user_id = u.id
        JOIN initial_survey i ON u.id = i.user_id
        WHERE u.roles NOT LIKE '%ROLE_ADMIN%'
            AND g.score > 100
            AND g.score < 2500
        GROUP BY i.age
    """

    best_score_by_fav_game_type_with_number_of_game = """
        
    """
