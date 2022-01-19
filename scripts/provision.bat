@echo off

:: Set environment variables
CALL %~dp0\set_variables.bat

:: Activate needed GCP APIs
gcloud services enable --project=%GCP_PROJECT_NAME% automl.googleapis.com
gcloud services enable --project=%GCP_PROJECT_NAME% bigquerydatatransfer.googleapis.com
gcloud services enable --project=%GCP_PROJECT_NAME% cloudscheduler.googleapis.com
gcloud services enable --project=%GCP_PROJECT_NAME% cloudfunctions.googleapis.com
gcloud services enable --project=%GCP_PROJECT_NAME% cloudbuild.googleapis.com
gcloud services enable --project=%GCP_PROJECT_NAME% cloudresourcemanager.googleapis.com
gcloud services enable --project=%GCP_PROJECT_NAME% containerregistry.googleapis.com
gcloud services enable --project=%GCP_PROJECT_NAME% language.googleapis.com

:: Create Bigquery datasets
gcloud alpha bq datasets create --project %GCP_PROJECT_NAME% %BQ_DATASET_RAW_NAME%
gcloud alpha bq datasets create --project %GCP_PROJECT_NAME% %BQ_DATASET_MASTER_NAME%
gcloud alpha bq datasets create --project %GCP_PROJECT_NAME% %BQ_DATASET_APPLICATION_NAME%

:: Create GCS bucket for master data files
gsutil mb -p %GCP_PROJECT_NAME% gs://%GCP_PROJECT_NAME%__%GS_MASTER_DATA_BUCKET_NAME%

:: Create Bigquery tables, views and queries
:: Build sql queries
python build_queries.python
:: Create tables
gcloud alpha bq tables create --project=%GCP_PROJECT_NAME% --dataset=%BQ_DATASET_MASTER_NAME% --schema-file=%BQ_TABLE_MASTER_TWEETS_DATA_SCHEMA% %BQ_TABLE_RAW_TWEETS_DATA_NAME%
gcloud alpha bq tables create --project=%GCP_PROJECT_NAME% --dataset=%BQ_DATASET_MASTER_NAME% --schema-file=%BQ_TABLE_MASTER_TWEETS_SENTIMENT_SCHEMA% %BQ_TABLE_MASTER_TWEETS_SENTIMENT_NAME%
gcloud alpha bq tables create --project=%GCP_PROJECT_NAME% --dataset=%BQ_DATASET_MASTER_NAME% %BQ_VIEW_MASTER_TWEETS_PENDING_SENTIMENT_NAME% --view=<%BQ_VIEW_MASTER_TWEETS_PENDING_SENTIMENT_QUERY%
gcloud alpha bq tables create --project=%GCP_PROJECT_NAME% --dataset=%BQ_DATASET_APPLICATION_NAME% %BQ_VIEW_MASTER_SENTIMENT_APPLICATION_DATA_NAME% --view=<%BQ_VIEW_MASTER_SENTIMENT_APPLICATION_DATA_QUERY%
:: Schedule masterization query
bq query --nouse_legacy_sql --project_id=%GCP_PROJECT_NAME% --display_name=testeq --target_dataset=%BQ_DATASET_MASTER_NAME% --schedule='every 24 hours' < %BQ_QUERY_TWEETS_DATA_MASTERIZATION%
