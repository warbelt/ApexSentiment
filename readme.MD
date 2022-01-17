# IAM Policies
User needs Bigquery Owner role for scheduling queryies


# Environment variables

### For ingest_tweets function
- **SCRAP_MAX_TWEETS**: max number of tweets to scrap in one execution
- **SCRAP_DESTINATION_TABLE**: bigquery table to store scrapped tweets
### For local developement
- **GOOGLE_APPLICATION_CREDENTIALS**: points to your credentials JSON file




# Activate APIs
automl.googleapis.com                Cloud AutoML API
bigquerydatatransfer.googleapis.com  BigQuery Data Transfer API
cloudscheduler.googleapis.com        Cloud Scheduler API
cloudfunctions.googleapis.com        Cloud Functions API
cloudbuild.googleapis.com            Cloud Build API
cloudresourcemanager.googleapis.com  Cloud Resource Manager API
containerregistry.googleapis.com     Container Registry API
language.googleapis.com              Cloud Natural Language API