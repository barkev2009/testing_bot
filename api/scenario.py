from api.testdriver import testdriver, wait
from api.utils import dotify
from datetime import datetime, timedelta
import re
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time
import traceback

def retry(func):
    def wrapper(self, *args, **kwargs):
        counter = 0
        while counter < 5:
            try:
                func(self, *args, **kwargs)
                break
            except Exception as e:
                counter += 1
                print(f'Попыток израсходовано: {counter} | Функция: {func.__name__} | Ошибка: {repr(e)}')
                print(f'Сообщение: {e}')
                print('TRACEBACK')
                traceback.print_exc()
                self.logout()
        if counter >= 5:
            print(f'{func.__name__} | ERROR: Израсходовано максимальное количество попыток')
    return wrapper

class scenario_tester(testdriver):
    def __init__(self, app_number=None) -> None:
        super().__init__()
        self.app_params.app_number = app_number
        print(f'Номер заявки: {app_number}')
    
    def login(self, user):
        self.print_to_input(self.platf_selectors.login_field, self.creds[user].login)
        self.print_to_input(self.platf_selectors.pass_field, self.creds[user].password)
        self.hit_enter(self.platf_selectors.pass_field)
    
    def logout(self):
        self.click_element(self.platf_selectors.profile_icon)
        self.click_element(self.platf_selectors.logout)
    
    
    def fill_app_params(self, sales_channel, product_type, duration_unit, rate_type, rate_kind, rate, repayment_order):
        self.select_dropdown(self.app_selectors.app_creation.sales_channel, sales_channel)
        self.select_dropdown(self.app_selectors.app_creation.product_type, product_type)
        self.select_dropdown(self.app_selectors.app_creation.duration_unit, duration_unit)
        self.select_dropdown(self.app_selectors.app_creation.rate_type, rate_type)
        self.select_dropdown(self.app_selectors.app_creation.rate_kind, rate_kind)
        self.print_to_input(self.app_selectors.app_creation.rate, rate)
        self.select_dropdown(self.app_selectors.app_creation.repayment_order, repayment_order)
    
    def create_pledges(self, search_value, pledges, search_param='name'):
        popup_selector = "[data-control-name='Поиск_клиента_общая_1'] "
        self.click_table_button(self.app_selectors.app_creation.pledge.add_pledge_button)
        self.click_element(self.app_selectors.app_creation.pledge.add_pledge_giver, wait=0.2)
        self.print_to_input(popup_selector + self.app_selectors.client_search.filter[search_param], search_value)
        self.click_element(popup_selector + self.app_selectors.client_search.search_button, wait=0.5)
        self.select_table_item(popup_selector + self.app_selectors.client_search.result_table_items, 0)
        self.click_element(self.app_selectors.app_creation.pledge.save_pledge_giver, wait=0.2)

        if type(pledges) != list:
            pledges = [pledges]
        for pledge in pledges:
            self.click_table_button(self.app_selectors.app_creation.pledge.add_pledge)
            self.select_dropdown(self.app_selectors.app_creation.pledge.pledge_type, pledge.type)
            self.select_dropdown(self.app_selectors.app_creation.pledge.object_type, pledge.object_type)
            self.print_to_input(self.app_selectors.app_creation.pledge.pledge_descr, pledge.pledge_descr)
            self.click_button_from_group(self.app_selectors.app_creation.pledge.pledge_addition_group, 'save')
        
        self.click_element(self.app_selectors.app_creation.pledge.save_pledges, wait=0.5)
    
    def create_participants(self, parts, search_param='name'):
        if type(parts) != list:
            parts = [parts]

        popup_selector = "[data-control-name='Всплывающее_окно_поиск_участника'] "
        for part in parts:
            self.click_table_button(self.app_selectors.app_creation.participant.add_part_button)
            self.select_dropdown(self.app_selectors.app_creation.participant.part_type_input, part.type)
            self.print_to_input(popup_selector + self.app_selectors.client_search.filter[search_param], part.search_value)
            self.click_element(popup_selector + self.app_selectors.client_search.search_button, wait=0.5)
            self.select_table_item(popup_selector + self.app_selectors.client_search.result_table_items, 0)
            self.click_element(self.app_selectors.app_creation.participant.save_participant, wait=0.5)
    
    @retry
    def create_app(self):
        self.login('sales_manager')
        self.click_menu_item('Поиск')
        self.find_object_in_table(
            'client_search', 
            [
                dotify({'type': 'input', 'field': 'name', 'value': 'сбербанк'})
            ],
            1
        )

        self.click_element(self.app_selectors.client_search.create_app_popup.create_new_app)
        time.sleep(0.5)
        self.get_app_number()
        # Небольшой костыль для того, чтобы нормально залоги создавались, можно обойти поумнее, но пока лень
        self.logout()

    
    @retry
    def draft_app(self):
        self.initiate_stage('sales_manager', 'Заполнение новой заявки')
        self.click_menu_item('Активные')
        self.find_object_in_table(
            'app_search', 
            [   
                dotify({'type': 'input', 'field': 'app_number', 'value': self.app_params.app_number})
            ],
            2
        )

        self.fill_app_params(
            'Прямая продажа', 
            'Разовый кредит', 
            'Год', 
            'Фиксированная', 
            'Единая', 
            10, 
            ['Индивидуальный график платежей', 'Аннуитетные платежи']
            )
        
        pledges = [
            dotify({'type': 'Нематериальные активы', 'object_type': 'Залог векселей', 'pledge_descr': 'Заложек'}),
            # dotify({'type': 'Нематериальные активы', 'object_type': 'Залог ценных бумаг', 'pledge_descr': 'ЦБшчка'}),
            # dotify({'type': 'Нематериальные активы', 'object_type': 'Поручительства (гарантии)', 'pledge_descr': 'Гарантия'})
        ]
        if pledges:
            self.create_pledges('альфа', pledges)
        
        participants = [
            dotify({'type': 'Поручительство', 'search_value': 'альфа'})
        ]
        if participants:
            self.create_participants(participants)

        self.click_placeholder_button('to_accept')
        self.logout()
    
    @retry
    def accept_new_app(self):
        self.initiate_stage('sales_boss', 'Акцепт новой заявки')
        self.click_menu_item('На акцепт')
        
        self.find_object_in_table(
            'task_search', 
            [
                dotify({'type': 'input', 'field': 'app_number', 'value': self.app_params.app_number}),
                dotify({'type': 'dropdown', 'field': 'task_status', 'value': 'Требуется акцепт'})
            ],
            3
        )

        self.click_placeholder_button('accept')
        self.logout()
    
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
        self.wait_doc_upload(self.app_selectors.expertises.add_document_popup.save_file, self.app_selectors.expertises.add_document_popup.download_file)
        self.click_element(self.app_selectors.expertises.add_document_popup.save_doc)

        self.click_placeholder_button('accept')
        self.click_button_from_group(self.app_selectors.expertises.popup_warning_button_group, 'accept')
        self.logout()
    
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
    
    @retry
    def sitting_complete_task(self, datetime=None):
        self.initiate_stage('secretary_cc', 'Секретарь КК, Выполнение задачи')
        if not self.app_params.sitting_datetime:
            self.app_params.sitting_datetime = datetime
        if not self.app_params.sitting_datetime:
            raise ValueError('Отсутствует дата заседания')
        
        self.click_menu_item('Мои задачи')
        self.click_element(self.app_selectors.task_search.clear_button, wait=0.2)
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
            time.sleep(0.5)
            if self.app_params.app_number in ''.join([elem.text for elem in self.multiselect(self.app_selectors.secretary.apps_table)]):
                actions = ActionChains(self.driver)
                actions.move_to_element(s).perform()
                self.select_table_item(self.app_selectors.secretary.apps_table)
                time.sleep(1.5)
                self.click_table_button(self.app_selectors.secretary.inform_client)
                time.sleep(0.5)
                break
        
        self.logout()
    
    @retry
    def inform_client_to_cod(self):
        self.initiate_stage('sales_manager', 'Информирование клиента, переход на КОД')
        self.click_menu_item('Все задачи')

        self.find_object_in_table(
            'task_search', 
            [
                dotify({'type': 'input', 'field': 'app_number', 'value': self.app_params.app_number}),
                dotify({'type': 'dropdown', 'field': 'app_status', 'value': 'Информирование клиента'})
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
        self.wait_doc_upload(addition + self.app_selectors.cod.accounts_title, addition + self.app_selectors.cod.loan_file_delete)
        self.click_button_from_group(self.app_selectors.cod.save_contract_button_group, 'save', addition)
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
                for k, v in self.app_selectors.cod.loan_inputs.items():
                    self.print_to_input(addition + v, loan_inputs[k])
                
                try:
                    if (self.driver.find_element(By.CSS_SELECTOR, addition + self.app_selectors.cod.loan_file_delete)):
                        self.driver.find_element(By.CSS_SELECTOR, addition + self.app_selectors.cod.loan_file_delete).click()
                except Exception:
                    pass

                self.click_element(addition + self.app_selectors.cod.loan_file)
                self.wait_doc_upload(addition + self.app_selectors.cod.accounts_title, addition + self.app_selectors.cod.loan_file_delete)
                self.click_button_from_group(self.app_selectors.cod.save_contract_button_group, 'save', addition)
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
                for k, v in self.app_selectors.cod.loan_inputs.items():
                    self.print_to_input(addition + v, loan_inputs[k])
                
                try:
                    if (self.driver.find_element(By.CSS_SELECTOR, addition + self.app_selectors.cod.loan_file_delete)):
                        self.driver.find_element(By.CSS_SELECTOR, addition + self.app_selectors.cod.loan_file_delete).click()
                except Exception:
                    pass

                self.click_element(addition + self.app_selectors.cod.loan_file)
                self.wait_doc_upload(addition + self.app_selectors.cod.accounts_title, addition + self.app_selectors.cod.loan_file_delete)
                self.click_button_from_group(self.app_selectors.cod.save_contract_button_group, 'save', addition)
                self.close_alert()
        except Exception:
            print('Не получилось обработать поручительства')
        
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
        # try:
        addition = "[data-control-name='Всплывающее_окно_редактирования_договора'] "
        self.click_tab('cod_contracts', 'pledges')

        pledge_len = len(self.multiselect(self.app_selectors.cod.pledges_table))
        for i in range(pledge_len):
            item = self.multiselect(self.app_selectors.cod.pledges_table)[i]
            item.click()
            time.sleep(0.5)
            self.click_button_from_group(self.app_selectors.cod.pledges_button_group, 'edit')
                            
            self.select_dropdown(addition + self.app_selectors.accept_cod.result_dropdown, 'Согласован клиентом')
            self.click_button_from_group(self.app_selectors.accept_cod.save_result_button_group, 'save', addition)
            # time.sleep(0.5)
            self.close_alert()
            # self.close_alert()
            time.sleep(0.5)
        # except Exception:
        #     print('Не получилось обработать залоги')

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
                
                self.select_dropdown(addition + self.app_selectors.accept_cod.result_dropdown, 'Согласован клиентом')
                self.click_button_from_group(self.app_selectors.accept_cod.save_result_button_group, 'save', addition)
                # time.sleep(0.5)
                self.close_alert()
                # self.close_alert()
                time.sleep(0.5)
        except Exception:
            print('Не получилось обработать поручительства')

        if action_type == 'accept':
            comment = 'Согласовано по заявке ' + self.app_params.app_number
        if action_type == 'mild_reject':
            comment = 'Разрешимые разногласия по заявке ' + self.app_params.app_number
        if action_type == 'accept':
            comment = 'Неразрешимые разногласия по заявке ' + self.app_params.app_number
        if action_type == 'accept':
            comment = 'Ошибки КОД по заявке ' + self.app_params.app_number

        self.print_to_input(self.app_selectors.accept_cod.result_comment, comment, 0.5)
        self.click_button_from_group(self.app_selectors.accept_cod.result_button_group, action_type)
        time.sleep(0.5)
        self.logout()
