# bhav-scraper

### Tasks completed
- Project setup
- completed scraping data from bse, parsing data, and saving it in cache
- created endpoint to search the data from cache
  
### TODO
- job scheduling
- check if /data/ path exists or create
- create frontend
- configure celery flower for monitoring.
- dockerize
- deploy

celery -A bhavproject worker --loglevel=INFO
celery -A bhavproject beat --loglevel=INFO