from api.driver import get_driver
from api.utils import dotdict, dotify

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

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

    DELAY = 20

    def __init__(self) -> None:
        self.driver = get_driver()
        with open(os.path.join('config', 'config.json'), 'r', encoding='utf-8') as file:
            self.config = dotify(json.load(file)) 
        self.app_selectors = self.config.selectors.app
        self.platf_selectors = self.config.selectors.platform
        self.creds = self.config.creds
        self.app_params = dotify({
            'app_number': None,
            'stage': None
        })
    
    def select(self, selector):
        element = WebDriverWait(self.driver, self.DELAY).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
        return element
    
    def multiselect(self, selector):
        element = WebDriverWait(self.driver, self.DELAY).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, selector)))
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
    
    def click_table_button(self, selector):
        elem = self.select(selector)
        ac = ActionChains(self.driver)
        ac.move_to_element(elem).move_by_offset(2, 2).click().perform()
    
    def click_menu_item(self, item_name):
        menu_items = self.multiselect(self.app_selectors.main_menu_items)
        try:
            item = list(filter(lambda x: x.text.split('(')[0].strip() == item_name, menu_items))[0]
            item.click()
        except IndexError:
            print(f'Не нашлось пункта меню с именем {item_name}')
    
    def select_table_item(self, table_selector, item_index=0):
        table_items = self.multiselect(table_selector)
        try:
            item = table_items[item_index]
            item.click()
        except IndexError:
            print(f'Индекс {item_index} выше количества найденных значений ({len(table_items)})')
    
    def get_app_number(self):
        app_number = self.select(self.app_selectors.app_creation.app_number_field)
        self.app_params.app_number = app_number.get_attribute('value')
        print(f'Номер заявки: {self.app_params.app_number}')
    
    @wait(0.5)
    def select_dropdown(self, dropdown_selector, dropdown_value):
        if type(dropdown_value) == list:
            for item in dropdown_value:
                self.print_to_input(dropdown_selector, item)
                self.hit_enter(dropdown_selector)
        else:
            self.print_to_input(dropdown_selector, dropdown_value)
            self.hit_enter(dropdown_selector)
    
    def click_button_from_group(self, button_group_selector, button_index):
        buttons = self.multiselect(button_group_selector)
        buttons[button_index].click()

    def setup_stage(self, stage_name):
        self.app_params.stage = stage_name
        print('Текущий этап: ' + stage_name)
    
    def click_placeholder_button(self, button_code):
        buttons = WebDriverWait(self.driver, self.DELAY).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.app_selectors.placeholder_buttons.selector)))
        buttons[self.app_selectors.placeholder_buttons.order[button_code]].click()
    
    def click_func_button(self, button_code):
        buttons = WebDriverWait(self.driver, self.DELAY).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.app_selectors.func_buttons.selector)))
        buttons[self.app_selectors.func_buttons.order[button_code]].click()
