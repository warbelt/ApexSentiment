WITH
    avg_sentiment_by_lang AS (
        SELECT
            AVG(sentiment_score)            AS lang_avg_score,
            AVG(sentiment_magnitude)        AS lang_avg_magnitude,
            tweet_language
        FROM
            (SELECT * FROM `{{GCP_PROJECT_NAME}}.{{BQ_DATASET_MASTER_NAME}}.{{BQ_TABLE_MASTER_TWEETS_SENTIMENT_NAME}}` WHERE sentiment_score != 0.0) sent
        LEFT JOIN
            `{{GCP_PROJECT_NAME}}.{{BQ_DATASET_MASTER_NAME}}.{{BQ_TABLE_MASTER_TWEETS_DATA_NAME}}` tweets_data
        ON
            sent.tweet_id = tweets_data.tweet_id
        GROUP BY
            tweet_language
    ),
    avg_sentiment_by_char AS (
        SELECT
            AVG(sentiment_score)            AS char_avg_score,
            AVG(sentiment_magnitude)        AS char_avg_magnitude,
            scrap_search_character
        FROM
            (SELECT * FROM `{{GCP_PROJECT_NAME}}.{{BQ_DATASET_MASTER_NAME}}.{{BQ_TABLE_MASTER_TWEETS_SENTIMENT_NAME}}` WHERE sentiment_score != 0.0) sent
        LEFT JOIN
            `{{GCP_PROJECT_NAME}}.{{BQ_DATASET_MASTER_NAME}}.{{BQ_TABLE_MASTER_TWEETS_DATA_NAME}}` tweets_data
        ON
            sent.tweet_id = tweets_data.tweet_id
        GROUP BY
            scrap_search_character
    )
SELECT
    sentiment.*,
    tweet_data.* EXCEPT (tweet_id),
    avg_sentiment_by_lang.* EXCEPT (tweet_language),
    avg_sentiment_by_char.* EXCEPT (scrap_search_character),
FROM
    `{{GCP_PROJECT_NAME}}.{{BQ_DATASET_MASTER_NAME}}.{{BQ_TABLE_MASTER_TWEETS_SENTIMENT_NAME}}` sentiment
LEFT JOIN
    `{{GCP_PROJECT_NAME}}.{{BQ_DATASET_MASTER_NAME}}.{{BQ_TABLE_MASTER_TWEETS_DATA_NAME}}` tweet_data
ON
    sentiment.tweet_id = tweet_data.tweet_id
LEFT JOIN
    avg_sentiment_by_lang
ON
    tweet_data.tweet_language = avg_sentiment_by_lang.tweet_language
LEFT JOIN
    avg_sentiment_by_char
ON
    tweet_data.scrap_search_character = avg_sentiment_by_char.scrap_search_character