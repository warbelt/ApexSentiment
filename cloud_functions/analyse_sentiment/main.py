import os
from datetime import date

import pandas as pd
from google.cloud import language_v1
from google.cloud import bigquery

from schemas import BQ_TABLE_SCHEMA


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


def analyse_tweet_sentiment(lang_client: language_v1.LanguageServiceClient, text_content:str, language:str):
    type_ = language_v1.Document.Type.PLAIN_TEXT
    encoding_type = language_v1.EncodingType.UTF8

    document = {"content": text_content, "type_": type_, "language": language}
    response = lang_client.analyze_sentiment(request = {'document': document, 'encoding_type': encoding_type})

    return response.document_sentiment.score, response.document_sentiment.magnitude


def analyse_sentiment(request):
    if 'SENTIMENT_DESTINATION_TABLE' not in os.environ:
        return "Environment variable not set: 'SENTIMENT_DESTINATION_TABLE'"
    else:
        destination_table = os.environ['SENTIMENT_DESTINATION_TABLE']

    if 'PENDING_TWEETS_TABLE' not in os.environ:
        return "Environment variable not set: 'PENDING_TWEETS_TABLE'"
    else:
        pending_tweets_table = os.environ['PENDING_TWEETS_TABLE']

    if 'MAX_TWEETS_TO_ANALYSE' not in os.environ:
        return "Environment variable not set: 'MAX_TWEETS_TO_ANALYSE'"
    else:
        max_tweets = int(os.environ['MAX_TWEETS_TO_ANALYSE'])

    pending_tweets_table = "apex-sentiment.master.tweets_data_pending_sentiment"

    bq_client = bigquery.Client()
    lang_client = language_v1.LanguageServiceClient()

    pending_tweets = bq_client.query(f"""
        SELECT *
        FROM {pending_tweets_table}
        LIMIT {max_tweets}
    """).result()

    results = []
    for row in pending_tweets:
        sentiment_info = analyse_tweet_sentiment(lang_client, row['tweet_text'], row['tweet_language'])
        results.append({
            'tweet_id':row['tweet_id'],
            'sentiment_score':sentiment_info[0],
            'sentiment_magnitude':sentiment_info[1],
        })

    sentiment_df = pd.DataFrame(results)
    sentiment_df['_data_sentiment_date'] = date.today()

    save_df_to_bq(sentiment_df, BQ_TABLE_SCHEMA, destination_table)

    print(f'Loaded {len(sentiment_df)} sentiment datapoints')
    return f'Loaded {len(sentiment_df)} sentiment datapoints'
