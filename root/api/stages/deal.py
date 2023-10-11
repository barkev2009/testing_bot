from selenium.webdriver.common.by import By

from root.api.testdriver import testdriver, retry
from root.api.utils import dotify

import time

class deal(testdriver):
    def __init__(self) -> None:
        super().__init__()
    
    @retry
    def deal(self):
        self.initiate_stage('client_boss', 'Сделка, старт')
        self.click_menu_item('Активные')
        addition = "[data-control-name='Вкладка_кредитный_договор_1'] "

        self.find_object_in_table(
            'app_search', 
            [
                dotify({'type': 'input', 'field': 'app_number', 'value': self.app_params.app_number})
            ],
            3
        )

        self.click_tab('app_tabs', 'cod')

        try:
            if (self.driver.find_element(By.CSS_SELECTOR, addition + self.app_selectors.cod.sign_file_delete)):
                self.driver.find_element(By.CSS_SELECTOR, addition + self.app_selectors.cod.sign_file_delete).click()
        except Exception:
            pass
        self.click_element(addition + self.app_selectors.cod.sign_file)
        # self.wait_doc_upload(addition + self.app_selectors.cod.accounts_title, addition + self.app_selectors.cod.loan_file_delete)
        self.wait_doc_upload(addition + self.app_selectors.cod.accounts_title)
        self.click_button_from_group(self.app_selectors.cod.sign_contract_button_group, 'save', addition)
        self.close_alert()

        # Залоги
        try:
            addition = "[data-control-name='Всплывающее_окно_редактирования_договора'] "
            self.click_tab('cod_contracts', 'pledges')

            pledge_len = len(self.multiselect(self.app_selectors.cod.pledges_table))
            for i in range(pledge_len):
                item = self.multiselect(self.app_selectors.cod.pledges_table)[i]
                item.click()
                time.sleep(0.5)
                self.click_button_from_group(self.app_selectors.cod.pledges_button_group, 'edit')
                
                try:
                    if (self.driver.find_element(By.CSS_SELECTOR, addition + self.app_selectors.cod.sign_file_delete)):
                        self.driver.find_element(By.CSS_SELECTOR, addition + self.app_selectors.cod.sign_file_delete).click()
                except Exception:
                    pass

                self.click_element(addition + self.app_selectors.cod.sign_file)
                # self.wait_doc_upload(addition + self.app_selectors.cod.accounts_title, addition + self.app_selectors.cod.loan_file_delete)
                self.wait_doc_upload(addition + self.app_selectors.cod.accounts_title)
                self.click_button_from_group(self.app_selectors.cod.sign_contract_button_group, 'save', addition)
                self.close_alert()
        except Exception:
            print('Не получилось обработать залоги')
        
        # Поручительства
        try:
            addition = "[data-control-name='Всплывающее_окно_редактирования'] "
            self.click_tab('cod_contracts', 'participants')

            part_len = len(self.multiselect(self.app_selectors.cod.participants_table))
            for i in range(part_len):
                item = self.multiselect(self.app_selectors.cod.participants_table)[i]
                item.click()
                time.sleep(0.5)
                self.click_button_from_group(self.app_selectors.cod.parts_button_group, 'edit')
                
                try:
                    if (self.driver.find_element(By.CSS_SELECTOR, addition + self.app_selectors.cod.sign_file_delete)):
                        self.driver.find_element(By.CSS_SELECTOR, addition + self.app_selectors.cod.sign_file_delete).click()
                except Exception:
                    pass

                self.click_element(addition + self.app_selectors.cod.sign_file)
                # self.wait_doc_upload(addition + self.app_selectors.cod.accounts_title, addition + self.app_selectors.cod.loan_file_delete)
                self.wait_doc_upload(addition + self.app_selectors.cod.accounts_title)
                self.click_button_from_group(self.app_selectors.cod.sign_contract_button_group, 'save', addition)
                self.close_alert()
        except Exception:
            print('Не получилось обработать поручительства')
        
        self.click_placeholder_button('accept')
        self.logout()
    
    @retry
    def deal_abs(self):
        self.initiate_stage('accountant_boss', 'Внесение данных сделки в АБС')
        self.click_menu_item('Мои задачи')

        self.find_object_in_table(
            'task_search', 
            [
                dotify({'type': 'input', 'field': 'app_number', 'value': self.app_params.app_number}),
                dotify({'type': 'dropdown', 'field': 'app_status', 'value': 'На сопровождении'}),
                dotify({'type': 'dropdown', 'field': 'task_type', 'value': 'Принятие в сопровождение'})
            ],
            1
        )