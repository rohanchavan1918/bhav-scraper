import glob
import os
from bhavproject.settings import CSV_DATA_PATH

def get_latest_file():
    '''
        The files downloaded from bse website are stored in 'CSV_DATA_PATH', returns the latest file from that directory.
        On Saturday and Sunday the bhav file is not updated on the website of BSE, this function returns the recently added file.
    '''
    list_of_files = glob.glob(CSV_DATA_PATH+'*.zip') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file