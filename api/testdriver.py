from api.driver import get_driver
from api.utils import dotdict, dotify

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from functools import wraps
import os
import json
import time 

def wait(seconds):
    def outer(func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            time.sleep(seconds)
        return wrapper
    return outer

class testdriver:

    DELAY = 10

    def __init__(self) -> None:
        self.driver = get_driver()
        with open(os.path.join('config', 'config.json'), 'r', encoding='utf-8') as file:
            self.config = dotify(json.load(file)) 
        self.app_selectors = self.config.selectors.app
        self.platf_selectors = self.config.selectors.platform
        self.creds = self.config.creds
    
    def select(self, selector):
        element = WebDriverWait(self.driver, self.DELAY).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        return element
    
    def multiselect(self, selector):
        element = WebDriverWait(self.driver, self.DELAY).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
        return element
    
    def print_to_input(self, input_selector, input):
        input_field = self.select(input_selector)
        input_field.send_keys(Keys.CONTROL + "a")
        input_field.send_keys(Keys.DELETE)
        input_field.send_keys(input)
    
    def hit_enter(self, selector):
        field = self.select(selector)
        field.send_keys(Keys.ENTER)
    
    def click_element(self, selector):
        elem = self.select(selector)
        elem.click()
    
    def click_menu_item(self, item_name):
        menu_items = self.multiselect(self.app_selectors.main_menu_items)
        try:
            item = list(filter(lambda x: x.text.split('(')[0].strip() == item_name, menu_items))[0]
            item.click()
        except IndexError:
            print(f'Не нашлось пункта меню с именем {item_name}')
    

    def login(self, user):
        self.print_to_input(self.platf_selectors.login_field, self.creds[user].login)
        self.print_to_input(self.platf_selectors.pass_field, self.creds[user].password)
        self.hit_enter(self.platf_selectors.pass_field)
    
    def logout(self):
        self.click_element(self.platf_selectors.profile_icon)
        self.click_element(self.platf_selectors.logout)
    
    @wait(2)
    def find_client(self, search_param, search_value):
        self.click_menu_item('Поиск')
        self.print_to_input(self.app_selectors.client_search[search_param], search_value)
        self.click_element(self.app_selectors.client_search.search_button)