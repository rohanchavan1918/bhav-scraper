import requests, csv,zipfile, os
from io import BytesIO
from datetime import datetime
from bhavproject.settings import BHAV_BASE_URI, CSV_DATA_PATH
import pandas as pd
from io import TextIOWrapper, StringIO
from django.core.cache import cache

class BhavScraper:
    '''
        Pipeline for downloading and processing the bhav copy file scraped from BSE.

    '''

    def __init__(self):
        print("Bhav scraper initialized.")
        self.bhav_file_name = self.get_bhav_filename()
        self.downloaded_bhav_file_path = None
    
    def get_bhav_filename(self) -> 'datetime':
        '''
            Generates the bhav file name according to current date 
        '''
        now = datetime.now()
        todays_date, todays_month = now.day, now.month
        todays_date = "0"+str(todays_date) if len(str(todays_date)) == 1 else str(todays_date)
        todays_month = "0"+str(todays_month) if len(str(todays_month)) == 1 else str(todays_month)
        todays_year = str(now.year % 100)
        bhav_file_name = "EQ"+todays_date+todays_month+todays_year+"_CSV.zip"
        return bhav_file_name
    
    def get_bhav_zip_data(self):
        '''
            Download the recent bhav zip file and save it in data dir
        '''
        bhav_zip_url = BHAV_BASE_URI+self.bhav_file_name
        _zip_file_path = os.path.join(CSV_DATA_PATH,self.bhav_file_name)
        _csv_file_path = _zip_file_path.replace("_CSV.zip",".csv")
        headers = {
            "Origin":"https://www.bseindia.com",
            "Referer":"https://www.bseindia.com/",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36"
        }
        try:
            response = requests.get(bhav_zip_url, headers=headers, timeout=15)
            response.raise_for_status()
            with open(_zip_file_path, "wb") as file:
                file.write(response.content)
                file.close()
            with zipfile.ZipFile(_zip_file_path, "r") as zip_ref:
                for file in zip_ref.namelist():
                    data = []
                    with zip_ref.open(file) as myfile:
                        reader = csv.reader(TextIOWrapper(myfile, 'utf-8'))
                        for row in reader:
                            data.append(row)
                    return data
        except Exception as e:
            print("[Error] In getting bhav - ", e)
            

    
    def cache_data(self, data):
        ''' 
        #############################################
        Reads the csv and cache the data.
        #############################################
        Since BSE does not publish data on weekends, thus the scraper wont be able to collect recent data on weekends,
        so it is essential to keep the data persistant in redis.
        The previous cache data is evicted, and new data is cached.        
        '''
        cache.delete_pattern("*")
        print("[INFO] cache evicted successfully ", datetime.now())
        for d in data:
            obj = {}
            obj['code'] = d[0]
            obj['name'] = d[1]
            obj['open'] = d[4]
            obj['high'] = d[5]
            obj['low'] = d[6]
            obj['close'] = d[7]
            obj['last'] = d[8]
            success = cache.set(obj['name'],obj,None)
        print("[INFO] New data cached successfully ",datetime.now())

    def run(self):
        ''' Driver function '''
        bhav_data = self.get_bhav_zip_data()
        self.cache_data(bhav_data)

# To run the scraper directly from shell.
def run_bhav_scraper():
    bhav_scraper = BhavScraper()
    bhav_scraper.run()