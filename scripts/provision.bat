CALL %~dp0\set_variables.bat

:: Activate needed GCP APIs
gcloud services enable --project=%gcp_project_name% automl.googleapis.com
gcloud services enable --project=%gcp_project_name% bigquerydatatransfer.googleapis.com
gcloud services enable --project=%gcp_project_name% cloudscheduler.googleapis.com
gcloud services enable --project=%gcp_project_name% cloudfunctions.googleapis.com
gcloud services enable --project=%gcp_project_name% cloudbuild.googleapis.com
gcloud services enable --project=%gcp_project_name% cloudresourcemanager.googleapis.com
gcloud services enable --project=%gcp_project_name% containerregistry.googleapis.com
gcloud services enable --project=%gcp_project_name% language.googleapis.com

:: Create Bigquery datasets
gcloud alpha bq datasets create --project %gcp_project_name% %bq_dataset_raw_name%
gcloud alpha bq datasets create --project %gcp_project_name% %bq_dataset_master_name%
gcloud alpha bq datasets create --project %gcp_project_name% %bq_dataset_application_name%

:: Create GCS bucket for master data files
gsutil mb -p %gcp_project_name% gs://%gcp_project_name%__%gs_master_data_bucket_name%

:: Create Bigquery tables
gcloud alpha bq tables create --project=%gcp_project_name% --dataset=%bq_dataset_master_name% --schema-file=%tweets_data_table_schema% %tweets_data_table_name%
gcloud alpha bq tables create --project=%gcp_project_name% --dataset=%bq_dataset_master_name% --schema-file=%tweets_sentiment_table_schema% %tweets_sentiment_table_name%
gcloud alpha bq tables create --project=%gcp_project_name% --dataset=%bq_dataset_master_name% %tweets_pending_sentiment_view_name% --view=<%tweets_pending_sentiment_view_query%
gcloud alpha bq tables create --project=%gcp_project_name% --dataset=%bq_dataset_application_name%  %sentiment_application_data_view_name% --view=<%sentiment_application_data_view_query%

:: Schedule masterization query
bq query --nouse_legacy_sql --project_id=%gcp_project_name% --display_name=testeq --target_dataset=%bq_dataset_master_name% --schedule='every 24 hours' < %tweets_data_masterization_query%
