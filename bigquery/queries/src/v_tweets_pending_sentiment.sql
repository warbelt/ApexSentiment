SELECT
    *
FROM (
    SELECT
        all_tweets.tweet_id,
        tweet_text,
        tweet_language,
        scrap_search_character,
        LENGTH(tweet_text)          AS tweet_length,
        ROW_NUMBER() OVER (
            PARTITION BY
                tweet_language,
                scrap_search_character
            ORDER BY
                LENGTH(tweet_text) DESC
                                    ) AS part_rank
    FROM (
        SELECT DISTINCT
            *
        FROM
            `{{PROJECT_NAME}}.{{MASTER_DATASET_NAME}}.{{MASTER_TWEETS_DATA_TABLE_NAME}}`
    ) all_tweets
    LEFT JOIN (
        SELECT DISTINCT
            tweet_id,
        FROM
            `{{PROJECT_NAME}}.{{MASTER_DATASET_NAME}}.{{MASTER_TWEETS_SENTIMENT_TABLE_NAME}}`
    ) analysed_tweets
    ON all_tweets.tweet_id = analysed_tweets.tweet_id
    WHERE analysed_tweets.tweet_id IS NULL
)
WHERE
    part_rank <= 100
AND
    tweet_language IN (
        'en',
        'es',
        'fr',
        'pt',
        'ja')
AND
    tweet_length < 400
ORDER BY
    part_rank DESC