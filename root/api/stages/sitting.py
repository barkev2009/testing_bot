from selenium.webdriver.common.action_chains import ActionChains

from root.api.testdriver import testdriver, retry
from root.api.utils import dotify

import time
from datetime import datetime
import re

class sitting(testdriver):
    def __init__(self) -> None:
        super().__init__()
    
    @retry
    def sitting_create_task(self):
        self.initiate_stage('secretary_cc', 'Секретарь КК, Создание задачи')

        self.click_menu_item('График')
        self.click_table_button(self.app_selectors.secretary.add_timesheet)
        self.print_to_input(self.app_selectors.secretary.sitting_type, 'Очное заседание')
        self.print_to_input(self.app_selectors.secretary.sitting_date, datetime.now().strftime("%d.%m.%Y"))
        self.print_to_input(self.app_selectors.secretary.sitting_hours, '00')
        self.print_to_input(self.app_selectors.secretary.sitting_minutes, '00')
        self.app_params.sitting_datetime = f'{datetime.now().strftime("%d.%m.%Y")} 00:00'
        self.click_element(self.app_selectors.secretary.save_timesheet)

        self.click_menu_item('Заявки для включения в КК')
        rows = self.multiselect(self.app_selectors.secretary.apps_for_sitting)
        list(filter(lambda x: self.app_params.app_number in x.text, rows))[0].click()
        time.sleep(1)
        self.click_element(self.app_selectors.secretary.add_to_sitting)
        self.print_to_input(self.app_selectors.secretary.add_to_sitting_type, 'Очное заседание')
        self.print_to_input(self.app_selectors.secretary.add_to_sitting_date, self.app_params.sitting_datetime + ':00')
        self.click_element(self.app_selectors.secretary.add_to_sitting_save)

        # self.app_params.sitting_datetime = '21.09.2023 00:00'
        self.click_menu_item('Заседания')
        time.sleep(0.5)
        sittings = self.multiselect(self.app_selectors.secretary.active_sittings)
        sittings = list(filter(lambda x: self.app_params.sitting_datetime.split(' ')[0] in x.text and self.app_params.sitting_datetime.split(' ')[1] in x.text, sittings))
        for sitting in sittings:
            sitting.click()
            time.sleep(1)
            if self.app_params.app_number in ''.join([item.text for item in self.multiselect(self.app_selectors.secretary.apps_for_sitting)]):
                self.click_button_from_group(self.app_selectors.secretary.take_task, 'take_task')
                break
            else:
                print('В данном заседании нет заявки')
        self.close_alert()
        self.logout()
    
    @retry
    def sitting_complete_task(self, datetime=None):
        self.initiate_stage('secretary_cc', 'Секретарь КК, Выполнение задачи')
        if not self.app_params.sitting_datetime:
            self.app_params.sitting_datetime = datetime
        if not self.app_params.sitting_datetime:
            raise ValueError('Отсутствует дата заседания')
        
        self.click_menu_item('Мои задачи')
        self.click_element(self.app_selectors.task_search.clear_button, wait=0.5)
        table_items = self.multiselect(self.app_selectors.task_search.result_table_items)
        list(filter(lambda x: 'Очное' in x.text and self.app_params.sitting_datetime in x.text, table_items))[0].click()
        self.click_table_button(self.app_selectors.task_search.to_work_button)
        time.sleep(3)

        self.click_tab('secretary_task', 'preparation')
        self.click_button_from_group(self.app_selectors.secretary.secretary_task, 'close_sitting')
        self.click_tab('secretary_task', 'results')

        self.select_table_item(self.app_selectors.secretary.task_apps)
        time.sleep(0.5)
        self.click_table_button(self.app_selectors.secretary.decision_button)

        self.print_to_input(self.app_selectors.secretary.decision_option, 'Вопрос принят')
        time.sleep(1)
        self.click_element(self.app_selectors.secretary.popup_title)
        self.click_button_from_group(self.app_selectors.secretary.secretary_decision, 'save')

        self.click_func_button('complete')
        self.logout()
    
    @retry
    def send_to_inform(self, datetime=None):
        self.initiate_stage('secretary_cc', 'Секретарь КК, Отправка на информирование')
        if not self.app_params.sitting_datetime:
            self.app_params.sitting_datetime = datetime
        if not self.app_params.sitting_datetime:
            raise ValueError('Отсутствует дата заседания')
        

        self.click_menu_item('Заседания')
        time.sleep(0.5)
        self.click_tab('sittings', 'completed')

        sittings = self.multiselect(self.app_selectors.secretary.sittings_table)
        target_sittings = list(
            filter( 
                lambda x: 
                    self.app_params.sitting_datetime.split(' ')[0] in x.text \
                    and self.app_params.sitting_datetime.split(' ')[1] in x.text \
                    and len(re.findall('background-color: rgb\(.+\)', x.get_attribute('style'))) > 0 \
                    and '252, 211, 208' in re.findall('background-color: rgb\(.+\)', x.get_attribute('style'))[0], 
                sittings 
            )
        )
        for s in target_sittings:
            s.click()
            time.sleep(1)
            if self.app_params.app_number in ''.join([elem.text for elem in self.multiselect(self.app_selectors.secretary.apps_table)]):
                actions = ActionChains(self.driver)
                actions.move_to_element(s).perform()
                self.select_table_item(self.app_selectors.secretary.apps_table)
                time.sleep(1)
                self.click_table_button(self.app_selectors.secretary.inform_client)
                time.sleep(0.5)
                break
        
        self.logout()
    
    @retry
    def inform_client_to_cod(self):
        self.initiate_stage('sales_manager', 'Информирование клиента, переход на КОД')
        self.click_menu_item('Мои задачи')

        self.find_object_in_table(
            'task_search', 
            [
                dotify({'type': 'input', 'field': 'app_number', 'value': self.app_params.app_number}),
                dotify({'type': 'dropdown', 'field': 'app_status', 'value': 'Информирование клиента'}),
                dotify({'type': 'dropdown', 'field': 'task_type', 'value': 'Согласование условий сделки'})
            ],
            3
        )
        
        self.click_tab('task_decision', 'task_decision')
        self.click_element(self.app_selectors.prescoring.inform_button)
        self.print_to_input(self.app_selectors.prescoring.inform_date, datetime.now().strftime("%d.%m.%Y"))
        
        self.click_element(self.app_selectors.prescoring.client_informed)
        self.print_to_input(self.app_selectors.inform.sm_comment, 'Согласована ' + self.app_params.app_number)
        self.print_to_input(self.app_selectors.inform.inform_date, datetime.now().strftime("%d.%m.%Y"), 0.2)
        self.click_button_from_group(self.app_selectors.inform.inform, 'success')
        time.sleep(1)
        self.logout()