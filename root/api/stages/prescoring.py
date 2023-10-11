from root.api.testdriver import testdriver, retry
from root.api.utils import dotify

import time
from datetime import datetime

class prescoring(testdriver):
    def __init__(self) -> None:
        super().__init__()
    
    @retry
    def prescoring(self):
        self.initiate_stage('client_boss', 'Прескоринг')
        self.click_menu_item('Активные')

        self.find_object_in_table(
            'app_search', 
            [
                dotify({'type': 'input', 'field': 'app_number', 'value': self.app_params.app_number})
            ],
            3
        )

        self.click_tab('app_tabs', 'prescoring_decision')
        time.sleep(1)
        self.print_to_input(self.app_selectors.prescoring.prescoring_field, 'Принято')
        time.sleep(0.5)
        self.click_placeholder_button('accept')
        self.logout()

    @retry
    def prescoring_inform(self):
        self.initiate_stage('sales_manager', 'Прескоринг информирование')
        self.click_menu_item('Мои задачи')

        self.find_object_in_table(
            'task_search', 
            [
                dotify({'type': 'input', 'field': 'app_number', 'value': self.app_params.app_number}),
                dotify({'type': 'dropdown', 'field': 'task_type', 'value': 'Информирование клиента'}),
                dotify({'type': 'dropdown', 'field': 'app_status', 'value': 'Информирование клиента'})
            ],
            3
        )

        self.click_tab('task_decision', 'task_decision')
        self.click_element(self.app_selectors.prescoring.inform_button)
        self.print_to_input(self.app_selectors.prescoring.inform_date, datetime.now().strftime("%d.%m.%Y"))
        self.click_button_from_group(self.app_selectors.prescoring.inform, 'success')
        time.sleep(2)
        self.logout()
    
    @retry
    def prescoring_documents(self):
        self.initiate_stage('sales_manager', 'Прескоринг запрос документов')
        self.click_menu_item('Мои задачи')

        self.find_object_in_table(
            'task_search', 
            [
                dotify({'type': 'input', 'field': 'app_number', 'value': self.app_params.app_number}),
                dotify({'type': 'dropdown', 'field': 'task_type', 'value': 'Запрос документов'}),
                dotify({'type': 'dropdown', 'field': 'app_status', 'value': 'Информирование клиента'})
            ],
            3
        )

        
        self.click_tab('app_details', 'documents')

        self.click_element(self.app_selectors.prescoring.documents_requested, 0.5)
        self.click_element(self.app_selectors.prescoring.documents_given, 0.5)
        self.click_element(self.app_selectors.prescoring.task_completed, 0.5)

        self.logout()