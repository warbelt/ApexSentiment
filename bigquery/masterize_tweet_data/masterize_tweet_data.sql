-- This query does two things:
--  - Make sure to only select ids that are not alredy in the masterized data
--  - Select rows to be masterized, cast and rename raw input fields before inserting in master data
-- When providing a .json schema to the 'gclud bq tables create' command, columns are created in alphabetical
-- order. Select columns in this query are ordered because of that reason


INSERT INTO
    `apex-sentiment.master.tweets_data`
SELECT
    new_tweets._data_ingest_date                                                AS _data_ingest_date
    CURRENT_DATE()                                                              AS _data_master_date
    new_tweets.character                                                        AS scrap_search_character,
    new_tweets.search                                                           AS scrap_search_query,
    new_tweets.id                                                               AS tweet_id,
    new_tweets.language                                                         AS tweet_language,
    CAST(new_tweets.nlikes AS INT64)                                            AS tweet_likes,
    CAST(new_tweets.nretweets AS INT64)                                         AS tweet_retweets,
    CAST(new_tweets.nreplies AS INT64)                                          AS tweet_replies,
    TRIM(REGEXP_REPLACE(new_tweets.tweet, r"@\w+", ""))                         AS tweet_text,
    TIMESTAMP_MILLIS(CAST(CAST(new_tweets.created_at AS FLOAT64 ) AS INT64))    AS tweet_time,
FROM (
    SELECT DISTINCT
        *
    FROM
        `apex-sentiment.raw.tweets_data`
) new_tweets
LEFT JOIN (
    SELECT DISTINCT
        tweet_id,
    FROM
        `apex-sentiment.master.tweets_data`
) old_tweets
ON new_tweets.id = old_tweets.tweet_id
WHERE old_tweets.tweet_id IS NULL
