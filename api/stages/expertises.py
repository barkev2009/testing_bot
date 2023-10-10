from api.testdriver import testdriver, retry
from api.utils import dotify

import time

class expertises(testdriver):
    def __init__(self) -> None:
        super().__init__()
    
    @retry
    def expertises(self):
        self.initiate_stage('ca_boss', 'Экспертизы ДКК')

        self.click_menu_item('Активные')

        self.find_object_in_table(
            'app_search', 
            [
                dotify({'type': 'input', 'field': 'app_number', 'value': self.app_params.app_number})
            ],
            3
        )

        time.sleep(3)
        self.click_tab('app_tabs', 'documents')
        self.click_table_button(self.app_selectors.expertises.add_document_button)
        self.print_to_input(self.app_selectors.expertises.add_document_popup.doc_type, 'Файл Проекта Решения')
        self.print_to_input(self.app_selectors.expertises.add_document_popup.doc_name, 'Файл Проекта Решения')
        self.click_element(self.app_selectors.expertises.add_document_popup.upload)

        self.click_element(self.app_selectors.expertises.add_document_popup.add_file)
        # self.wait_doc_upload(self.app_selectors.expertises.add_document_popup.save_file, self.app_selectors.expertises.add_document_popup.download_file)
        self.wait_doc_upload(self.app_selectors.expertises.add_document_popup.save_file)
        self.click_element(self.app_selectors.expertises.add_document_popup.save_doc)

        self.click_placeholder_button('accept')
        self.click_button_from_group(self.app_selectors.expertises.popup_warning_button_group, 'accept')
        self.logout()