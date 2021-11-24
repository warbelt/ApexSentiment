import os

import twint
from google.cloud import bigquery

from schemas import BQ_TABLE_SCHEMA


def get_tweets_data(search_string:str, limit: int):
    conf = twint.Config()
    conf.Hide_output = True
    conf.Limit = limit
    conf.Search = search_string
    conf.Pandas = True

    twint.run.Search(conf)
    tweets_df = twint.storage.panda.Tweets_df

    return tweets_df


def save_df_to_bq(df, schema, table_id:str) -> int:
    client = bigquery.Client()

    job_config = bigquery.LoadJobConfig(
        schema = schema,
        write_disposition = "WRITE_APPEND"
    )

    job = client.load_table_from_dataframe(
        df, table_id, job_config=job_config
    )
    job.result()

    table = client.get_table(table_id)
    return(table.num_rows)


def ingest_tweets(request):
    tweet_limit = os.getenv('SCRAP_MAX_TWEETS', 1000)
    if 'SCRAP_DESTINATION_TABLE' not in os.environ:
        return "Environment variable not set: 'SCRAP_DESTINATION_TABLE'"
    else:
        destination_table = os.environ['SCRAP_DESTINATION_TABLE']


    if request.args and 'character' in request.args:
        character = request.args.get('character')
    else: return "Missing 'character' argument"

    if request.args and 'search_query' in request.args:
        search_query = request.args.get('search_query')
    else: return "Missing 'search_query' argument"

    tweets_df = get_tweets_data(search_query, tweet_limit, start_date=start_date, end_date=end_date)

    tweets_df['created_at'] = tweets_df['created_at'].astype(int)
    tweets_df['hashtags'] = tweets_df['hashtags'].astype(str)
    tweets_df['cashtags'] = tweets_df['cashtags'].astype(str)
    tweets_df['urls'] = tweets_df['urls'].astype(str)
    tweets_df['photos'] = tweets_df['photos'].astype(str)
    tweets_df['reply_to'] = tweets_df['reply_to'].astype(str)
    tweets_df['character'] = character

    loaded_rows = save_df_to_bq(tweets_df, BQ_TABLE_SCHEMA, destination_table)

    return f'Loaded {loaded_rows} tweets'