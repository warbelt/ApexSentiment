"""
This function is responsible for calling the ingest_tweets function once for
every different search query, as configured in /storage/searches.csv

The searches file has two columns:
name: Name of the search. It will be used to label search results
query: Search query using twitter advanced search format

This function receives no arguments in the request.
For every row in the searches file, a call to the scrapping function will be
scheduled.
"""
import os
import requests
import urllib.parse
import datetime
import csv
import io

from google.cloud import storage


def get_searches_dict(bucket, filename):
    """
    """
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket)

    blob = bucket.blob(filename)
    blob = blob.download_as_string()
    blob = blob.decode('utf-8')

    blob = io.StringIO(blob)

    searches = csv.reader(blob)
    searches_dict = {row[0]:row[1] for row in searches}

    return searches_dict


def orchestrate_scrapping(request):
    if 'SCRAPPING_CLOUD_FUNCTION_URL' not in os.environ:
        return "Environment variable not set: 'SCRAPPING_CLOUD_FUNCTION_URL'"
    else:
        scrapping_url = os.environ['SCRAPPING_CLOUD_FUNCTION_URL']

    if 'SEARCHES_FILE_BUCKET' not in os.environ:
        return "Environment variable not set: 'SEARCHES_FILE_BUCKET'"
    else:
        searches_bucket = os.environ['SEARCHES_FILE_BUCKET']

    if 'SEARCHES_FILE_FILENAME' not in os.environ:
        return "Environment variable not set: 'SEARCHES_FILE_FILENAME'"
    else:
        searches_file = os.environ['SEARCHES_FILE_FILENAME']


    searches_dict = get_searches_dict(searches_bucket, searches_file)

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    date_string = yesterday.strftime("%Y-%m-%d")

    for k, v in searches_dict.items():
        parsed_search = urllib.parse.quote(v)
        query_string = f"?character={k}&search_query={parsed_search}&date={date_string}"
        url = f"{scrapping_url}{query_string}"
        print(f"calling function url: {url}")
        # This is a bit hacky, we don't want to wait for the response.
        # Set a low timeout, send request and forget about response.
        try:
            requests.get(url, timeout=1)
        except requests.exceptions.ReadTimeout:
            pass

    print('Scrap finished. See the ingestion function logs to see individual results/errors')
    return("Scrap success")