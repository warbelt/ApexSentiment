import os
import yaml


SOURCE_QUERIES_FOLDER = "bigquery/queries/src"
COMPILED_QUERIES_FOLDER = "bigquery/queries/dist"
BUILD_VARIABLES_FILE = "scripts/build_variables.yaml"


def compile_query(query_file_name: str, replacements: dict):
    with open(os.path.join(SOURCE_QUERIES_FOLDER, query_file_name), 'r') as file :
        filedata = file.read()

    for src, dst in replacements.items():
        filedata = filedata.replace("{{"+src+"}}", dst)

    with open(os.path.join(COMPILED_QUERIES_FOLDER, query_file_name), 'w') as file :
        file.write(filedata)


if __name__ == "__main__":
    if not os.path.isdir(COMPILED_QUERIES_FOLDER):
        os.mkdir(COMPILED_QUERIES_FOLDER)

with open(BUILD_VARIABLES_FILE, "r") as f:
    replacements = yaml.safe_load(f)

    compile_query("masterize_tweet_data.sql", replacements)
    compile_query("v_sentiment_enriched.sql", replacements)
    compile_query("v_tweets_pending_sentiment.sql", replacements)
