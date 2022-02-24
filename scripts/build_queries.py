"""
This script takes the base SQL files in bigquery/queries/src, and replaces
placeholder values with the final values stored as environment variables.
The resulting SQL code is writen in files in bigquery/queries/dist.

Placeholders are labeled as {{NAME}}

To add replacements:
1. Add a placeholder inside the src query
2. Add a replacement in the main function "replacements" dictionary 
"""
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


def main():
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

    compile_query("masterize_tweet_data.sql", src_dir, dist_dir, replacements)
    compile_query("v_sentiment_enriched.sql", src_dir, dist_dir, replacements)
    compile_query("v_tweets_pending_sentiment.sql", src_dir, dist_dir, replacements)


if __name__ == "__main__":
    main()
