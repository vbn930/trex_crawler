from Manager import DriverManager
from Utility import LoginModule
from Utility import Util
import atexit
import trex_crawler

#pyinstaller -n "TREX Crawler" --clean --onefile main.py

def main():
    logger = Util.Logger("Dev")
    crawler = trex_crawler.TREX_Crawler(logger)
    test_url = "https://www.t-rex-racing.com/"
    try:
        crawler.start_crawling()
    except Exception as e:
        logger.log(log_level="Error", log_msg=e)
    finally:
        exit_program = input("Press enter key to exit the program")

main()