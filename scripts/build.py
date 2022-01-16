import os


SOURCE_QUERIES_FOLDER = "bigquery\queries\src"
COMPILED_QUERIES_FOLDER = "bigquery\queries\dist"


def compile_query(query_file_name: str, replacements: dict):
    with open(os.path.join(SOURCE_QUERIES_FOLDER, query_file_name), 'r') as file :
        filedata = file.read()

    for src, dst in replacements.items():
        filedata = filedata.replace("{{"+src+"}}", dst)

    with open(os.path.join(COMPILED_QUERIES_FOLDER, query_file_name), 'w') as file :
        file.write(filedata)


REPLACEMENTS = {
    "PROJECT_NAME" : "rock-sentinel",
    "MASTER_DATASET_NAME" : "master",
    "MASTER_TWEETS_DATA_TABLE_NAME" : "tweets_data",
    "RAW_DATASET_NAME" : "raw",
    "RAW_TWEETS_DATA_TABLE_NAME" : "tweets_data",
    "MASTER_TWEETS_SENTIMENT_TABLE_NAME" : "tweets_sentiment",
}

compile_query("masterize_tweet_data.sql", REPLACEMENTS)
compile_query("v_sentiment_enriched.sql", REPLACEMENTS)
compile_query("v_tweets_pending_sentiment.sql", REPLACEMENTS)
