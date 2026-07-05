BASE_URL = "https://alternativeto.net"
LISTING_PATH = "/browse/new-apps/?p={test_page_number}"
test_page_number = 10
PROGRESS_FILE = "output/.progress.json"
OUTPUT_DIR = "output"
OUTPUT_FILE = "apps.csv"
MAX_RETRIES = 3
RETRY_DELAY = 5

START_PAGE = 101
END_PAGE = 200
BATCH_SIZE = 50 #pages

MIN_PAGE_DELAY = 8   
MAX_PAGE_DELAY = 15  
BATCH_BREAK = 30