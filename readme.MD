# IAM Policies
User needs Bigquery Owner role for scheduling queryies


# Environment variables

### For ingest_tweets function
- **SCRAP_MAX_TWEETS**: max number of tweets to scrap in one execution
- **SCRAP_DESTINATION_TABLE**: bigquery table to store scrapped tweets
### For local developement
- **GOOGLE_APPLICATION_CREDENTIALS**: points to your credentials JSON file
