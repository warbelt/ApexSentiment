from google.cloud import bigquery

BQ_TABLE_SCHEMA = [
    bigquery.SchemaField("tweet_id",                bigquery.enums.SqlTypeNames.STRING),
    bigquery.SchemaField("sentiment_magnitude",     bigquery.enums.SqlTypeNames.FLOAT),
    bigquery.SchemaField("sentiment_score",         bigquery.enums.SqlTypeNames.FLOAT),
    bigquery.SchemaField("_data_sentiment_date",    bigquery.enums.SqlTypeNames.DATE),
]
