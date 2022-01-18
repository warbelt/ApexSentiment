import os
import sys
import yaml


SOURCE_QUERIES_FOLDER = r"..\bigquery\queries\src"
COMPILED_QUERIES_FOLDER = r"..\bigquery\queries\dist"
BUILD_VARIABLES_FILE = r"build_variables.yaml"


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
    vars_file_path = os.path.join(os.path.dirname(sys.argv[0]), BUILD_VARIABLES_FILE)

    if not os.path.isdir(dist_dir):
        os.mkdir(dist_dir)

    with open(vars_file_path, "r") as f:
        replacements = yaml.safe_load(f)

    compile_query("masterize_tweet_data.sql", src_dir, dist_dir, replacements)
    compile_query("v_sentiment_enriched.sql", src_dir, dist_dir, replacements)
    compile_query("v_tweets_pending_sentiment.sql", src_dir, dist_dir, replacements)
