from selenium.webdriver.common.by import By

from api.testdriver import testdriver, retry
from api.utils import dotify

import time
from datetime import datetime

class deal_preparation(testdriver):
    def __init__(self) -> None:
        super().__init__()
    
    @retry
    def deal_prep_start(self):
        self.initiate_stage('client_boss', 'Подготовка к сделке')
        self.click_menu_item('Активные')

        self.find_object_in_table(
            'app_search', 
            [
                dotify({'type': 'input', 'field': 'app_number', 'value': self.app_params.app_number})
            ],
            3
        )

        self.click_tab('app_tabs', 'deal_prep')

        checkboxes = self.multiselect(self.app_selectors.deal_prep.checkboxes)
        checkboxes[2].click()
        time.sleep(1)

        block = self.multiselect(self.app_selectors.deal_prep.block)[2]
        block.find_element(By.CSS_SELECTOR, self.app_selectors.deal_prep.task_type).send_keys('Запрос документов для открытия расчетного и/или залогового счета')

        # Костыль 
        self.click_element(self.app_selectors.deal_prep.send_button, 2)
        self.click_element(self.app_selectors.deal_prep.send_button, 2)

        self.logout()
    
    @retry
    def deal_prep_req_acc_docs(self, task_type='Запрос документов для открытия расчетного и/или залогового счета'):
        self.initiate_stage('sales_manager', f'{task_type}, подготовка к сделке')
        self.click_menu_item('Мои задачи')

        self.find_object_in_table(
            'task_search', 
            [
                dotify({'type': 'input', 'field': 'app_number', 'value': self.app_params.app_number}),
                dotify({'type': 'dropdown', 'field': 'app_status', 'value': 'Подготовка к сделке'}),
                dotify({'type': 'dropdown', 'field': 'task_type', 'value': task_type})
            ],
            3
        )
        
        self.click_tab('deal_prep', 'task_decision')

        self.print_to_input(self.app_selectors.deal_prep.comment, 'Какой-то комментарий')
        
        self.click_element(self.app_selectors.deal_prep.upload_icon, 0.5)
        self.click_element(self.app_selectors.deal_prep.add_file)
        self.wait_doc_upload(self.app_selectors.deal_prep.save_file)
        time.sleep(0.5)
        self.click_func_button('to_accept')
        time.sleep(0.5)
        self.logout()
    
    @retry
    def deal_prep_accept_req_docs(self):
        self.initiate_stage('sales_boss', 'Акцепт задачи на прикрепление документа, подготовка к сделке')
        self.click_menu_item('На акцепт')
        
        self.find_object_in_table(
            'task_search', 
            [
                dotify({'type': 'input', 'field': 'app_number', 'value': self.app_params.app_number}),
                dotify({'type': 'dropdown', 'field': 'task_status', 'value': 'Требуется акцепт'})
            ],
            3
        )

        self.click_func_button('accept')
        self.logout()
    
    @retry
    def deal_prep_open_acc(self):
        self.initiate_stage('operation_boss', 'Открытие счета, подготовка к сделке')
        self.click_menu_item('Мои задачи')

        self.find_object_in_table(
            'task_search', 
            [
                dotify({'type': 'input', 'field': 'app_number', 'value': self.app_params.app_number}),
                dotify({'type': 'dropdown', 'field': 'app_status', 'value': 'Подготовка к сделке'}),
                dotify({'type': 'dropdown', 'field': 'task_type', 'value': 'Открытие р/с и/или залогового счёта'})
            ],
            1
        )
        
        try:
            self.click_element(self.app_selectors.deal_prep.task_intercept, 3)
        except Exception:
            print('Нет требования по перехвату')
        self.click_tab('deal_prep', 'task_decision')

        self.print_to_input(self.app_selectors.deal_prep.comment, 'Какой-то комментарий')
        self.print_to_input(self.app_selectors.deal_prep.date_input, datetime.now().strftime("%d.%m.%Y"))
        
        self.click_element(self.app_selectors.deal_prep.upload_icon, 0.5)
        self.click_element(self.app_selectors.deal_prep.add_file)
        self.wait_doc_upload(self.app_selectors.deal_prep.save_file)
        time.sleep(0.5)
        self.click_func_button('accept')
        time.sleep(0.5)
        self.logout()
    
    @retry
    def deal_prep_end(self):
        self.initiate_stage('client_boss', 'Подготовка к сделке, финиш')
        self.click_menu_item('Активные')

        self.find_object_in_table(
            'app_search', 
            [
                dotify({'type': 'input', 'field': 'app_number', 'value': self.app_params.app_number})
            ],
            3
        )

        self.click_placeholder_button('accept')
        time.sleep(1)
        self.close_toasts()
        time.sleep(1)

        self.logout()