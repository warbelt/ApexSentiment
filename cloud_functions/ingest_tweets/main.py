"""
This function is responsible for extracting tweet data using the twint library.
Scrapped data will be saved to a BigQuery table.

This function expects the following arguments in the request:
character: Name of the search. Search results will be labeled with this value.
search_query: Search string using the twitter advanced search format
start_date: Lower end of the search's time range.
end_date: Upper end of the search's time range.
date: Single date for the search

One, and only one of the following combinations must be specified:
date
start_date AND end_date.
"""
import os
import time
from datetime import date

import twint
from google.cloud import bigquery

from schemas import BQ_TABLE_SCHEMA


def get_tweets_data(search_string:str, limit: int, start_date: str = '', end_date: str = ''):
    conf = twint.Config()
    conf.Hide_output = True
    conf.Limit = limit
    conf.Search = search_string
    conf.Pandas = True
    conf.Since = start_date
    conf.Until = end_date

    twint.run.Search(conf)
    tweets_df = twint.storage.panda.Tweets_df

    return tweets_df


def save_df_to_bq(df, schema, table_id:str):
    client = bigquery.Client()

    job_config = bigquery.LoadJobConfig(
        schema = schema,
        write_disposition = "WRITE_APPEND"
    )

    busy = True
    backoff = 20
    while busy:
        try:
            job = client.load_table_from_dataframe(
                df, table_id, job_config=job_config
            )
            job.result(retry=bigquery.DEFAULT_RETRY)
            busy = False
        except:
            print(f"retry in [{backoff}] seconds")
            time.sleep(backoff)


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

    if request.args and 'start_date' in request.args:
        start_date = request.args.get('start_date')
    else:
        start_date = ''

    if request.args and 'end_date' in request.args:
        end_date = request.args.get('end_date')
    else:
        end_date = ''

    if request.args and 'date' in request.args:
        exact_date = request.args.get('date')
    else:
        exact_date = ''

    if exact_date != '':
        if start_date != '':
            return "Invalid 'start_date' and 'date' arguments simultaneously"
        else:
            start_date = exact_date + ' 00:00:00'

        if end_date != '':
            return "Invalid 'end_date' and 'date' arguments simultaneously"
        else:
            end_date = exact_date + ' 23:59:59'

    print(f'Scrap {tweet_limit} tweets for query {search_query}.')

    tweets_df = get_tweets_data(search_query, tweet_limit, start_date=start_date, end_date=end_date)

    print(f'Retrieved {len(tweets_df.index)} tweets.')

    for col in tweets_df.columns.tolist():
        tweets_df[col] = tweets_df[col].astype(str)
    tweets_df['character'] = character
    tweets_df['_data_ingest_date'] = date.today()

    save_df_to_bq(tweets_df, BQ_TABLE_SCHEMA, destination_table)
    return f'Retrieved {len(tweets_df.index)} tweets.'
