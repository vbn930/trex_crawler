from Manager import DriverManager
from Utility import LoginModule
from Utility import Util
import pu_crawler
import atexit

#pyinstaller -n "TREX Crawler" --clean --onefile main.py

def main():
    logger = Util.Logger("Dev")
    test_url = "https://iofferman.x.yupoo.com/categories/190905?isSubCate=true&page=2"
    try:
        driver_manager = DriverManager.WebDriverManager(logger)
        driver_manager.get_page(test_url)
    except Exception as e:
        logger.log(log_level="Error", log_msg=e)
    finally:
        exit_program = input("Press enter key to exit the program")

main()