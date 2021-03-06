@echo off

:: Set environment variables
CALL %~dp0\set_variables.bat

:: Retrieve scrapping function URI and store into CLOUD_FUNCTION_URL
FOR /F "tokens=* USEBACKQ" %%g IN (`gcloud functions describe orchestrate_scrapping --region=us-east1 ^| findstr "http.*cloudfunctions.net.*"`) do SET "CLOUD_FUNCTION_URL=%%g"
:: Schedule periodic call to scrapping function
gcloud scheduler jobs create http run_orchestrate_scrapping --project %GCP_PROJECT_NAME% --location %FUNCTIONS_REGION% --schedule="0 */3 * * *" --uri=%CLOUD_FUNCTION_URL:~5% --http-method=GET