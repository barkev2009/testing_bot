from api.driver import get_driver
from api.utils import dotify, WindowFinder, bcolors

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from functools import wraps
import os
import json
import time 
import traceback
from datetime import datetime
import uuid

def wait(seconds):
    def outer(func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            time.sleep(seconds)
        return wrapper
    return outer

def retry(func):
    def wrapper(self, *args, **kwargs):
        counter = 0
        while counter < 5:
            try:
                func(self, *args, **kwargs)
                break
            except Exception as e:
                counter += 1
                print(f'{bcolors.FAIL}Попыток израсходовано: {counter} | Функция: {func.__name__} | Ошибка: {bcolors.OKBLUE}{repr(e)}{bcolors.ENDC}')
                # print(f'Сообщение: {e}')
                traceback_uuid = str(uuid.uuid4())
                print(f'{bcolors.FAIL}Traceback ID: {bcolors.OKBLUE}{traceback_uuid}{bcolors.ENDC}')
                with open(os.path.join('logs', f'{datetime.now().strftime("%d.%m.%Y")}.log'), 'a', encoding='utf-8') as file:
                    file.write(f'Traceback ID: {traceback_uuid}\n')
                    file.write(traceback.format_exc())
                    file.write('\n'*5)
                self.logout()
        if counter >= 5:
            print(f'{func.__name__} | ERROR: Израсходовано максимальное количество попыток')
    return wrapper

class testdriver:

    DELAY = 10

    def __init__(self) -> None:
        self.driver = get_driver()
        with open(os.path.join('config', 'config.json'), 'r', encoding='utf-8') as file:
            self.config = dotify(json.load(file)) 
        self.app_selectors = self.config.selectors.app
        self.platf_selectors = self.config.selectors.platform
        self.creds = self.config.creds
        self.app_params = dotify({
            'app_number': None,
            'stage': None,
            'sitting_datetime': None
        })
    
    def select(self, selector):
        element = WebDriverWait(self.driver, self.DELAY).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        return element
    
    def multiselect(self, selector):
        element = WebDriverWait(self.driver, self.DELAY).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))
        return element
    
    def print_to_input(self, input_selector, input, wait=0):
        self.click_element(input_selector)
        input_field = self.select(input_selector)
        input_field.send_keys(Keys.CONTROL + "a")
        input_field.send_keys(Keys.DELETE)
        input_field.send_keys(input)
        if wait != 0:
            time.sleep(wait)
    
    def hit_enter(self, selector):
        field = self.select(selector)
        field.send_keys(Keys.ENTER)
    
    def click_element(self, selector, wait=0):
        elem = self.select(selector)
        elem.click()
        if wait != 0:
            time.sleep(wait)
    
    @wait(0.5)
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
            time.sleep(0.3)
        except IndexError:
            print(f'Индекс {item_index} выше количества найденных значений ({len(table_items)})')
    
    def get_app_number(self):
        app_number = self.select(self.app_selectors.app_creation.app_number_field)
        self.app_params.app_number = app_number.get_attribute('value')
        print(f'Номер заявки: {self.app_params.app_number}')
    
    @wait(1)
    def select_dropdown(self, dropdown_selector, dropdown_value):
        if type(dropdown_value) == list:
            for item in dropdown_value:
                self.print_to_input(dropdown_selector, item)
                # self.click_element(dropdown_selector)
        else:
            self.print_to_input(dropdown_selector, dropdown_value)
            # self.click_element(dropdown_selector)
    
    @wait(0.5)
    def click_button_from_group(self, button_group_selector, button_code, addition=None):
        if addition:
            buttons = self.multiselect(addition + button_group_selector.selector)
        else:
            buttons = self.multiselect(button_group_selector.selector)
        buttons[button_group_selector.order[button_code]].click()

    def setup_stage(self, stage_name):
        self.app_params.stage = stage_name
        print(f'{bcolors.OKGREEN}---> Текущий этап: {stage_name}{bcolors.ENDC}')
    
    def click_placeholder_button(self, button_code):
        buttons = WebDriverWait(self.driver, self.DELAY).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.app_selectors.placeholder_buttons.selector)))
        buttons[self.app_selectors.placeholder_buttons.order[button_code]].click()
        time.sleep(2)
    
    def click_func_button(self, button_code):
        buttons = WebDriverWait(self.driver, self.DELAY).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.app_selectors.func_buttons.selector)))
        buttons[self.app_selectors.func_buttons.order[button_code]].click()
        time.sleep(2)
    
    def click_tab(self, tab_group, tab_code):
        tabs = self.multiselect(self.app_selectors.tabs[tab_group].selector)
        list(filter(lambda x: x.get_attribute('data-index') == str(self.app_selectors.tabs[tab_group].data_index[tab_code]), tabs))[0].click()
        time.sleep(1)
    
    def login(self, user):
        self.print_to_input(self.platf_selectors.login_field, self.creds[user].login)
        self.print_to_input(self.platf_selectors.pass_field, self.creds[user].password)
        self.hit_enter(self.platf_selectors.pass_field)
    
    def logout(self):
        self.click_element(self.platf_selectors.profile_icon)
        self.click_element(self.platf_selectors.logout)

    def initiate_stage(self, initiator, stage_name):
        self.login(initiator)
        if not self.app_params.app_number:
            raise ValueError('Номер заявки пустой')
        self.setup_stage(stage_name)
        self.change_application()
    
    def find_object_in_table(self, selector_group, search_params, wait=0):
        self.click_element(self.app_selectors[selector_group].clear_button, 0.5)

        for param in search_params:
            if param.type == 'input':
                self.print_to_input(self.app_selectors[selector_group].filter[param.field], param.value)
            elif param.type == 'dropdown':
                self.select_dropdown(self.app_selectors[selector_group].filter[param.field], param.value)
        
        self.click_element(self.app_selectors[selector_group].search_button, 1)
        if selector_group == 'task_search':
            self.click_menu_item('Все задачи')
            time.sleep(0.5)
        self.select_table_item(self.app_selectors[selector_group].result_table_items, 0)
        self.click_table_button(self.app_selectors[selector_group].to_work_button)
        if wait != 0:
            time.sleep(wait)
    
    def wait_doc_upload(self, click_selector):
        self.upload_file()
        time.sleep(0.5)
        # wait_element = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, wait_selector)))
        # if (wait_element):
        self.click_element(click_selector)
    
    def close_alert(self, wait=0):
        alert = self.select('.jq_popup_message')
        alert.send_keys(Keys.ESCAPE)
        time.sleep(0.5)

    def close_popup(self, popup_selector):
        alert = self.select(popup_selector)
        alert.find_element(By.XPATH, '..').send_keys(Keys.ESCAPE)
        time.sleep(0.5)
    
    def upload_file(self):
        time.sleep(0.5)
        win = WindowFinder()
        win.find_window_wildcard(".*Открытие*") 
        win.set_foreground()
        path = self.config.app.file_path
        print(f'Filename: {os.path.join(*path)}')
        win.input_path(os.path.join(*path))
        win.click_button()
    
    def change_application(self):
        try:
            icon = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.icon22.forms')))
            icon.click()
            time.sleep(0.2)
            lis = self.multiselect('.authDropdown.formChecker li')
            for li in lis:
                if 'АРМ_Пользователя' in li.text:
                    li.click()
            time.sleep(5)
        except Exception:
            print('Не замечено перехода в приложение')
    
    def close_toasts(self):
        toasts = self.multiselect('.toast-element button.ui-dialog-titlebar-close')
        for toast in toasts:
            try:
                toast.click()
            except Exception:
                print('Не удалось закрыть тост')
    