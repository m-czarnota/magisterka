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

    accurate_by_score_with_gender = f"""
        SELECT 
            g.score AS score,
            (
                SELECT ((COUNT(s.miss_shots) - SUM(s.miss_shots)) / COUNT(s.miss_shots)) * 100
                FROM square s
                WHERE s.game_id = g.id
            ) AS accurate,
            i.gender AS gender
        {__from_game_join_user_survey}
            AND g.score > 100
    """

    accurate_by_score_with_fav_game_type = f"""
        SELECT 
            g.score AS score,
            (
                SELECT ((COUNT(s.miss_shots) - SUM(s.miss_shots)) / COUNT(s.miss_shots)) * 100
                FROM square s
                WHERE s.game_id = g.id
            ) AS accurate,
            i.favourite_game_type as fav_game_type
        {__from_game_join_user_survey}
            AND g.score > 100
    """

    mediocre_game_count_to_best_score_on_fav_game_type = f"""
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

    time_to_click_by_square_size_by_age = f"""
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

    time_to_click_by_square_size_by_fav_game_type = f"""
        SELECT 
            i.favourite_game_type AS fav_game_type,
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

    mean_time_to_click_by_square_size = f"""
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

    time_to_click_by_square_velocity_by_age = f"""
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

    time_to_click_by_square_velocity_by_fav_game_type = f"""
        SELECT 
            i.favourite_game_type AS fav_game_type,
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

    mean_time_to_click_by_square_velocity = f"""
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

    score_with_fav_game_type = f"""
        SELECT g.score AS score, i.favourite_game_type AS fav_game_type
        {__from_game_join_user_survey}
            AND g.score > 100
    """

    squares_size_and_time_to_fall_taking_away_hp = f"""
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
