import yaml

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


def save_df_to_bq(df, schema, table_id:str):
    client = bigquery.Client()

    job_config = bigquery.LoadJobConfig(
        schema = schema,
        write_disposition = "WRITE_TRUNCATE"
    )

    job = client.load_table_from_dataframe(
        df, table_id, job_config=job_config
    )
    job.result()

    table = client.get_table(table_id)
    print(
        "Loaded {} rows and {} columns to {}".format(
            table.num_rows, len(table.schema), table_id
        )
    )


def ingest_tweets(request):
    with open('config.yml', 'r') as file:
        conf = yaml.safe_load(file)

    if request.args and 'message' in request.args:
        return request.args.get('message')

    champion = 'Gibraltar'
    search_string = 'gibby'

    tweets_df = get_tweets_data(search_string, conf['limit'])

    tweets_df['created_at'] = tweets_df['created_at'].astype(int)
    tweets_df['hashtags'] = tweets_df['hashtags'].astype(str)
    tweets_df['cashtags'] = tweets_df['cashtags'].astype(str)
    tweets_df['urls'] = tweets_df['urls'].astype(str)
    tweets_df['photos'] = tweets_df['photos'].astype(str)
    tweets_df['reply_to'] = tweets_df['reply_to'].astype(str)
    tweets_df['champion'] = champion

    save_df_to_bq(tweets_df, BQ_TABLE_SCHEMA, conf['destination_table'])