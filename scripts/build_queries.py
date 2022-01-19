import os
import sys


SOURCE_QUERIES_FOLDER = r"..\bigquery\queries\src"
COMPILED_QUERIES_FOLDER = r"..\bigquery\queries\dist"


def compile_query(query_file_name: str, src_dir: str, dist_dir: str, replacements: dict):
    with open(os.path.join(src_dir, query_file_name), 'r') as file :
        filedata = file.read()

    for src, dst in replacements.items():
        filedata = filedata.replace("{{"+src+"}}", dst)

    with open(os.path.join(dist_dir, query_file_name), 'w') as file :
        file.write(filedata)


if __name__ == "__main__":
    src_dir = os.path.join(os.path.dirname(sys.argv[0]), SOURCE_QUERIES_FOLDER)
    dist_dir = os.path.join(os.path.dirname(sys.argv[0]), COMPILED_QUERIES_FOLDER)

    if not os.path.isdir(dist_dir):
        os.mkdir(dist_dir)

    replacements = {
        "GCP_PROJECT_NAME":os.getenv("GCP_PROJECT_NAME"),
        "BQ_DATASET_RAW_NAME":os.getenv("BQ_DATASET_RAW_NAME"),
        "BQ_DATASET_MASTER_NAME":os.getenv("BQ_DATASET_MASTER_NAME"),
        "BQ_TABLE_MASTER_TWEETS_DATA_NAME":os.getenv("BQ_TABLE_MASTER_TWEETS_DATA_NAME"),
        "BQ_TABLE_RAW_TWEETS_DATA_NAME":os.getenv("BQ_TABLE_RAW_TWEETS_DATA_NAME"),
        "BQ_TABLE_MASTER_TWEETS_SENTIMENT_NAME":os.getenv("BQ_TABLE_MASTER_TWEETS_SENTIMENT_NAME"),
    }

    print("repllace")
    print(replacements)

    compile_query("masterize_tweet_data.sql", src_dir, dist_dir, replacements)
    compile_query("v_sentiment_enriched.sql", src_dir, dist_dir, replacements)
    compile_query("v_tweets_pending_sentiment.sql", src_dir, dist_dir, replacements)
