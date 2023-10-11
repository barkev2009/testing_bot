from selenium.webdriver.common.by import By

from root.api.testdriver import testdriver, retry
from root.api.utils import dotify

import time
from datetime import datetime, timedelta

class cod(testdriver):
    def __init__(self) -> None:
        super().__init__()
    
    @retry
    def cod(self):
        self.initiate_stage('accountant_boss', 'Подготовка КОД')
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

        loan_inputs = {
            "loan_number": "ХХХ", "loan_location": "Место", "loan_date": datetime.now().strftime("%d.%m.%Y"),
            "loan_end": (datetime.now() + timedelta(days=30)).strftime("%d.%m.%Y"), "fio": "ФИО", "job": "Работа", 
            "reason": "Причина", "fio2": "ФИО", "job2": "Работа", "reason2": "Причина"
        }

        for k, v in self.app_selectors.cod.loan_inputs.items():
            self.print_to_input(addition + v, loan_inputs[k])
        try:
            if (self.driver.find_element(By.CSS_SELECTOR, addition + self.app_selectors.cod.loan_file_delete)):
                self.driver.find_element(By.CSS_SELECTOR, addition + self.app_selectors.cod.loan_file_delete).click()
        except Exception:
            pass
        self.click_element(addition+ self.app_selectors.cod.loan_file)
        # self.wait_doc_upload(addition + self.app_selectors.cod.accounts_title, addition + self.app_selectors.cod.loan_file_delete)
        self.wait_doc_upload(addition + self.app_selectors.cod.accounts_title)
        self.click_button_from_group(self.app_selectors.cod.save_contract_button_group, 'save', addition)
        self.close_alert()

        # Залоги
        addition = "[data-control-name='Всплывающее_окно_редактирования_договора'] "
        self.click_tab('cod_contracts', 'pledges')

        pledge_len = len(self.multiselect(self.app_selectors.cod.pledges_table))
        for i in range(pledge_len):
            try:
                item = self.multiselect(self.app_selectors.cod.pledges_table)[i]
                item.click()
                time.sleep(0.5)
                self.click_button_from_group(self.app_selectors.cod.pledges_button_group, 'edit')
                for k, v in self.app_selectors.cod.loan_inputs.items():
                    self.print_to_input(addition + v, loan_inputs[k])
                
                try:
                    if (self.driver.find_element(By.CSS_SELECTOR, addition + self.app_selectors.cod.loan_file_delete)):
                        self.driver.find_element(By.CSS_SELECTOR, addition + self.app_selectors.cod.loan_file_delete).click()
                except Exception:
                    pass

                self.click_element(addition + self.app_selectors.cod.loan_file)
                # self.wait_doc_upload(addition + self.app_selectors.cod.accounts_title, addition + self.app_selectors.cod.loan_file_delete)
                self.wait_doc_upload(addition + self.app_selectors.cod.accounts_title)
                self.click_button_from_group(self.app_selectors.cod.save_contract_button_group, 'save', addition)
                self.close_alert()
            except Exception:
                print(f'Не получилось обработать залог {i + 1}')
        
        # Поручительства
        addition = "[data-control-name='Всплывающее_окно_редактирования'] "
        self.click_tab('cod_contracts', 'participants')

        part_len = len(self.multiselect(self.app_selectors.cod.participants_table))
        for i in range(part_len):
            try:
                item = self.multiselect(self.app_selectors.cod.participants_table)[i]
                item.click()
                time.sleep(0.5)
                self.click_button_from_group(self.app_selectors.cod.parts_button_group, 'edit')
                for k, v in self.app_selectors.cod.loan_inputs.items():
                    self.print_to_input(addition + v, loan_inputs[k])
                
                try:
                    if (self.driver.find_element(By.CSS_SELECTOR, addition + self.app_selectors.cod.loan_file_delete)):
                        self.driver.find_element(By.CSS_SELECTOR, addition + self.app_selectors.cod.loan_file_delete).click()
                except Exception:
                    pass

                self.click_element(addition + self.app_selectors.cod.loan_file)
                # self.wait_doc_upload(addition + self.app_selectors.cod.accounts_title, addition + self.app_selectors.cod.loan_file_delete)
                self.wait_doc_upload(addition + self.app_selectors.cod.accounts_title)
                self.click_button_from_group(self.app_selectors.cod.save_contract_button_group, 'save', addition)
                self.close_alert()
            except Exception:
                print(f'Не получилось обработать поручительство {i + 1}')
        
        self.click_placeholder_button('accept')
        self.logout()
    
    @retry
    def cod_result(self, action_type='accept'):
        self.initiate_stage('sales_manager', 'Согласование КОД')
        self.click_menu_item('Мои задачи')

        self.find_object_in_table(
            'task_search', 
            [
                dotify({'type': 'input', 'field': 'app_number', 'value': self.app_params.app_number}),
                dotify({'type': 'dropdown', 'field': 'task_type', 'value': 'Согласование КОД с клиентом'})
            ],
            3
        )
        
        self.click_tab('cod_decision', 'cod_decision')
        self.select_dropdown(self.app_selectors.accept_cod.result_dropdown, 'Согласован клиентом')
        self.click_button_from_group(self.app_selectors.accept_cod.save_result_button_group, 'save')
        time.sleep(1)
        self.close_alert()

        # Залоги
        addition = "[data-control-name='Всплывающее_окно_редактирования_договора'] "
        self.click_tab('cod_contracts', 'pledges')

        pledge_len = len(self.multiselect(self.app_selectors.cod.pledges_table))
        for i in range(pledge_len):
            try:
                item = self.multiselect(self.app_selectors.cod.pledges_table)[i]
                item.click()
                time.sleep(0.5)
                self.click_button_from_group(self.app_selectors.cod.pledges_button_group, 'edit')
                                
                self.select_dropdown(addition + self.app_selectors.accept_cod.result_dropdown, 'Согласован клиентом')
                self.click_button_from_group(self.app_selectors.accept_cod.save_result_button_group, 'save', addition)
                # time.sleep(0.5)
                self.close_alert()
                self.close_popup(addition)
                # self.close_alert()
                time.sleep(0.5)
            except Exception:
                print(f'Не получилось обработать залог {i + 1}')

        # Поручительства
        addition = "[data-control-name='Всплывающее_окно_редактирования'] "
        self.click_tab('cod_contracts', 'participants')

        part_len = len(self.multiselect(self.app_selectors.cod.participants_table))
        for i in range(part_len):
            try:
                item = self.multiselect(self.app_selectors.cod.participants_table)[i]
                item.click()
                time.sleep(0.5)
                self.click_button_from_group(self.app_selectors.cod.parts_button_group, 'edit')
                
                self.select_dropdown(addition + self.app_selectors.accept_cod.result_dropdown, 'Согласован клиентом')
                self.click_button_from_group(self.app_selectors.accept_cod.save_result_button_group, 'save', addition)
                # time.sleep(0.5)
                self.close_alert()
                self.close_popup(addition)
                # self.close_alert()
                time.sleep(0.5)
            except Exception:
                print(f'Не получилось обработать поручительство {i + 1}')

        if action_type == 'accept':
            comment = 'Согласовано по заявке ' + self.app_params.app_number
        if action_type == 'mild_reject':
            comment = 'Разрешимые разногласия по заявке ' + self.app_params.app_number
        if action_type == 'reject':
            comment = 'Неразрешимые разногласия по заявке ' + self.app_params.app_number
        if action_type == 'cod_error':
            comment = 'Ошибки КОД по заявке ' + self.app_params.app_number

        self.print_to_input(self.app_selectors.accept_cod.result_comment, comment, 0.5)
        self.click_button_from_group(self.app_selectors.accept_cod.result_button_group, action_type)
        time.sleep(0.5)
        self.logout()