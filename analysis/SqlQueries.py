class SqlQueries:
    __from_game_join_user_survey = """
        FROM game g
        JOIN `user` u ON g.user_id = u.id
        JOIN initial_survey i ON u.id = i.user_id
        WHERE u.roles NOT LIKE '%ROLE_ADMIN%'
    """

    mean_score_by_fav_game_type = f"""
        SELECT i.favourite_game_type AS fav_game_type, AVG(g.score) AS mean_score, COUNT(g.id) AS game_count
        {__from_game_join_user_survey}
            AND g.score > 100
        GROUP BY i.favourite_game_type
    """

    time_and_score = f"""
        SELECT g.time AS time, g.score AS score, i.favourite_game_type AS fav_game_type
        {__from_game_join_user_survey}
    """

    best_score_by_age = f"""
        SELECT i.age AS age, MAX(g.score) AS best_score
        {__from_game_join_user_survey}
        GROUP BY i.age
    """

    mean_score_by_age = f"""
        SELECT i.age AS age, AVG(g.score) as mean_score
        {__from_game_join_user_survey}
            AND g.score > 100
        GROUP BY i.age
    """

    best_score_by_fav_game_type_with_game_count = f"""
        SELECT i.favourite_game_type AS fav_game_type, MAX(g.score) AS best_score, COUNT(g.score) AS game_count
        {__from_game_join_user_survey}
        GROUP BY i.favourite_game_type
    """

    count_of_rejected_scores = f"""
        SELECT COUNT(g.score) AS count_of_rejected_scores
        {__from_game_join_user_survey}
            AND g.score <= 100
    """

    count_of_preferred_playing_style = f"""
        SELECT i.preferred_playing_style AS preferred_playing_style, COUNT(i.preferred_playing_style) AS style_count
        {__from_game_join_user_survey}
        GROUP BY i.preferred_playing_style
    """

    mean_accurate_by_fav_game_type = f"""
        SELECT 
            i.favourite_game_type AS fav_game_type, 
            ((COUNT(s.miss_shots) - SUM(s.miss_shots)) / COUNT(s.miss_shots)) * 100 AS accurate
        FROM game g
        JOIN `user` u ON g.user_id = u.id
        JOIN initial_survey i ON u.id = i.user_id
        JOIN square s ON s.game_id = g.id
        WHERE u.roles NOT LIKE '%ROLE_ADMIN%'
            AND g.score > 100
        GROUP BY i.favourite_game_type
    """

    mean_accurate_by_preferred_playing_style_with_best_score = f"""
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

    mean_time_to_click_by_fav_game_type = f"""
        SELECT i.favourite_game_type AS fav_game_type, AVG(s.time_to_click) AS mean_time
        FROM game g
        JOIN `user` u ON g.user_id = u.id
        JOIN initial_survey i ON u.id = i.user_id
        JOIN square s ON s.game_id = g.id
        WHERE u.roles NOT LIKE '%ROLE_ADMIN%'
            AND g.score > 100
            AND s.time_to_click IS NOT NULL
        GROUP BY i.favourite_game_type
    """

    mean_time_to_click_by_age = f"""
        SELECT i.age AS age, AVG(s.time_to_click) AS mean_time
        FROM game g
        JOIN `user` u ON g.user_id = u.id
        JOIN initial_survey i ON u.id = i.user_id
        JOIN square s ON s.game_id = g.id
        WHERE u.roles NOT LIKE '%ROLE_ADMIN%'
            AND g.score > 100
            AND s.time_to_click IS NOT NULL
        GROUP BY i.age
    """

    count_of_games_to_best_score_by_fav_game_type = f"""
        SELECT i.favourite_game_type AS fav_game_type, (
            SELECT COUNT(g2.id)
            FROM game g2
            WHERE g2.user_id = u.id
        ) AS game_count, g.score, u.id
        {__from_game_join_user_survey}
            AND g.score IN (
                SELECT MAX(g.score) 
                {__from_game_join_user_survey}
                GROUP BY i.favourite_game_type
            )
        GROUP BY i.favourite_game_type
    """

    accurate_by_score = f"""
        SELECT 
            g.score AS score,
            (
                SELECT ((COUNT(s.miss_shots) - SUM(s.miss_shots)) / COUNT(s.miss_shots)) * 100
                FROM square s
                WHERE s.game_id = g.id
            ) AS accurate
        {__from_game_join_user_survey}
            AND g.score > 100
    """

    mediocre_game_count_to_best_score_on_fav_game_type = f"""
        SELECT 
            i.favourite_game_type AS fav_game_type, 
            AVG(
                SELECT best_scores.number_of_game FROM (SELECT MAX(score_numbers.score) AS best_score, score_numbers.number_of_game AS number_of_game 
                FROM (
                    SELECT g2.score AS score, ROW_NUMBER() over (ORDER BY (SELECT NULL)) AS number_of_game
                    FROM game g2
                    WHERE g2.user_id IN (SELECT g3.user_id FROM game g3 WHERE g3.id = g.id)
                ) AS score_numbers) AS best_scores
            ) AS mediocre_game_count
        {__from_game_join_user_survey}
            AND g.score > 100
        GROUP BY i.favourite_game_type
    """
