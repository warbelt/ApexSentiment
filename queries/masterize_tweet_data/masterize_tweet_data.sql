-- This query does two things:
--  - Make sure to only select ids that are not alredy in the masterized data
--  - Select rows to be masterized, cast and rename raw input fields before inserting in master data
INSERT INTO
    `apex-sentiment.master.tweet_data`
SELECT
    new_tweets.id                                                               AS tweet_id,
    TIMESTAMP_MILLIS(CAST(CAST(new_tweets.created_at AS FLOAT64 ) AS INT64))    AS tweet_time,
    new_tweets.tweet                                                            AS tweet_text,
    new_tweets.language                                                         AS tweet_language,
    CAST(new_tweets.nlikes AS INT64)                                            AS tweet_likes,
    CAST(new_tweets.nreplies AS INT64)                                          AS tweet_replies,
    CAST(new_tweets.nretweets AS INT64)                                         AS tweet_retweets,
    new_tweets.search                                                           AS scrap_search_query,
    new_tweets.character                                                        AS scrap_search_character,
FROM (
    SELECT DISTINCT
        *
    FROM
        `apex-sentiment.raw.tweet_data`
) new_tweets
LEFT JOIN (
    SELECT DISTINCT
        tweet_id,
    FROM
        `apex-sentiment.master.tweet_data`
) old_tweets
ON new_tweets.id = old_tweets.tweet_id
WHERE old_tweets.tweet_id IS NULL
