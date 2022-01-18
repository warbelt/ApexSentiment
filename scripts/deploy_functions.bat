@echo off

CALL %~dp0\set_variables.bat

:: --- ingest_tweets function
:: deploy function
CALL gcloud functions deploy ingest_tweets ^
--source cloud_functions\ingest_tweets ^
--project=%GCP_PROJECT_NAME% ^
--region=%FUNCTIONS_REGION% ^
--memory=512MB ^
--timeout=180s ^
--runtime=python39 ^
--trigger-http ^
--allow-unauthenticated ^
--env-vars-file cloud_functions\ingest_tweets\env.yaml

:: --- orchestrate_scrapping fuction
:: upload searches csv file
CALL gsutil cp storage/searches.csv gs://%GCP_PROJECT_NAME%__%gs_master_data_bucket_name%
:: deploy function
CALL gcloud functions deploy orchestrate_scrapping ^
--source cloud_functions\orchestrate_scrapping ^
--project=%GCP_PROJECT_NAME% ^
--region=%FUNCTIONS_REGION% ^
--memory=128MB ^
--runtime python39 ^
--trigger-http ^
--allow-unauthenticated ^
--env-vars-file cloud_functions\orchestrate_scrapping\env.yaml

:: --- analyse sentiment fuction
:: deploy function
CALL gcloud functions deploy analyse_sentiment ^
--source cloud_functions\analyse_sentiment ^
--project=%GCP_PROJECT_NAME% ^
--region=%FUNCTIONS_REGION% ^
--memory=512MB ^
--runtime python39 ^
--trigger-http ^
--allow-unauthenticated ^
--env-vars-file cloud_functions\analyse_sentiment\env.yaml