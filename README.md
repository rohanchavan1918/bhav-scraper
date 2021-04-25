# BhavCopy 

BSE publishes a "Bhavcopy" (Equity) ZIP every day here: [https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx](https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx)
This app downloads the zip everyday and stores it in a redis cache. The stored data can be searched and filtered using the UI which is made with Vue.js.
Celery beat is being used to perform the task of downloading and processing the zip file in background (asyncronously ) in the scheduled time i.e 18.00 IST - monday to friday (BSE doesnot publish new zip files on saturday and sunday) .
Celery flower is used to get details of the tasks which are run by celery beat.

DEMO LINK  :- 
http://68.183.90.51/

To monitor the tasks
http://68.183.90.51/flower/

[Video](https://user-images.githubusercontent.com/25792843/115996549-5ec1cc00-a5fd-11eb-983d-823b74b7cc39.mp4)



### Project setup :
- First clone the repository.
	
	`git clone https://github.com/rohanchavan1918/bhav-scraper.git`
	
- Enter the project directory
	
	`cd bhav-scraper && cd bhav-project`
	
- Enter the django root directory ( where settings.py file exists) and create .env file.
	
	` cp env_template.txt .env`
	
edit the .env file and add your credentials and values.
	
### Running the project :
The easiest way to run this project is with docker-compose , run

	`docker-compose up`
	
You can use -d flag to run this in background in daemon mode
	
	`docker-compose up -d`
 
Running Project without docker ( Requirements - Redis, celery )

- start a virtual environment.

` python -m venv venv `

` ./venv/Scripts/activate` for linux `source venv/bin/activate`

- Install project requirements.

` pip install -r requirements.txt`		

- Create *.env* file according to *env_template.txt* 

- Run the development server 

` python manage.py runserver`

- In another terminal / cmd start celery and celery beat

	` celery -A bhavproject worker --loglevel=INFO `
	
	` celery -A bhavproject beat --loglevel=info `
		
