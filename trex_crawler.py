from Utility import Util
from Manager import DriverManager
from Utility import LoginModule
from Manager import FileManager

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from dataclasses import dataclass
import pandas as pd
import datetime


@dataclass
class Product:
    code: str
    name: str
    price: str
    dealer_price: str
    description: str
    trans_description: str
    images: list

@dataclass
class ShopCatrgory:
    make: str
    model: str
    year: str
    href: str

class TREX_Crawler:
    def __init__(self, logger):
        self.file_manager = FileManager.FileManager()
        self.logger = logger
        self.driver_manager = DriverManager.WebDriverManager(self.logger)
        self.driver = self.driver_manager.driver
        self.file_manager.creat_dir("./temp")
        self.file_manager.creat_dir("./output")
        self.product_numbers = []
        self.product_abbreviations = []
        self.account = []
        self.product_informations = []
        self.data = dict()
        self.data_init()

    def data_init(self):
        self.data.clear()
        self.data["상품 코드"] = list()
        self.data["상품명"] = list()
        self.data["정상가"] = list()
        self.data["딜러가"] = list()
        self.data["대표 이미지"] = list()
        self.data["상세 이미지"] = list()
        self.data["옵션명"] = list()
        self.data["옵션 내용"] = list()
        self.data["설명"] = list()
        self.data["설명 번역"] = list()
        self.data["모델"] = list()

    def get_shop_categories(self, start_make, start_model, start_year):
        is_found_start_idx = False
        shop_categories = []
        
        #shop 옵션 값 가져오기
        make_select = Select(self.driver.find_element(By.ID, 'SelectCategory2'))
        make_options = make_select.options
        make_options = make_options[1:]

        for make_option in make_options:
            make_select.select_by_visible_text(make_option.text)
            model_select = Select(self.driver.find_element(By.ID, 'SelectMake2'))
            model_options = model_select.options
            model_options = model_options[2:]

            for model_option in model_options:
                model_select.select_by_visible_text(model_option.text)
                year_select = Select(self.driver.find_element(By.ID, 'SelectModel2'))
                year_options = year_select.options
                year_options = year_options[2:]

                for year_option in year_options:
                    if start_make == make_option.text and start_model == model_option.text and start_year == year_option.text and is_found_start_idx == False:
                        is_found_start_idx = True
                        print(f"Found start point! {make_option.text}, {model_option.text}, {year_option.text}")
                    
                    if is_found_start_idx:
                        shop_category = ShopCatrgory(make=make_option.text, model=model_option.text, year=year_option.text, href=year_option.get_attribute("value"))
                        print(f"Append {shop_category.make}, {shop_category.model}, {shop_category.year}, {shop_category.href}")
                        shop_categories.append(shop_category)

        return shop_categories

    def start_crawling(self):
        LoginModule.trex_login_module(self.driver_manager, self.logger, "bikeonline.korea@gmail.com", "piston7759!")
        self.driver_manager.get_page("https://www.t-rex-racing.com/")
        
        start_make = "Bimota"
        start_model = "DB3 Mantra"
        start_year = "1999-2000"
        shop_categories = self.get_shop_categories(start_make, start_model, start_year)  
