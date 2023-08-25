from api.testdriver import testdriver, wait
from api.utils import dotify

import time

class scenario_tester(testdriver):
    def __init__(self) -> None:
        super().__init__()
    
    def login(self, user):
        self.print_to_input(self.platf_selectors.login_field, self.creds[user].login)
        self.print_to_input(self.platf_selectors.pass_field, self.creds[user].password)
        self.hit_enter(self.platf_selectors.pass_field)
    
    def logout(self):
        self.click_element(self.platf_selectors.profile_icon)
        self.click_element(self.platf_selectors.logout)
    
    @wait(2)
    def find_client(self, search_value, search_param='name'):
        self.click_menu_item('Поиск')
        self.click_element(self.app_selectors.client_search.clear_button)
        time.sleep(1)
        self.print_to_input(self.app_selectors.client_search.filter[search_param], search_value)
        self.click_element(self.app_selectors.client_search.search_button)
    
    def fill_app_params(self, sales_channel, product_type, duration_unit, rate_type, rate_kind, rate, repayment_order):
        self.select_dropdown(self.app_selectors.app_creation.sales_channel, sales_channel)
        self.select_dropdown(self.app_selectors.app_creation.product_type, product_type)
        self.select_dropdown(self.app_selectors.app_creation.duration_unit, duration_unit)
        self.select_dropdown(self.app_selectors.app_creation.rate_type, rate_type)
        self.select_dropdown(self.app_selectors.app_creation.rate_kind, rate_kind)
        self.print_to_input(self.app_selectors.app_creation.rate, rate)
        self.select_dropdown(self.app_selectors.app_creation.repayment_order, repayment_order)
    
    def create_new_app(self, client_name, client_param='name', table_index=0):
        self.find_client(client_name, client_param)
        self.select_table_item(self.app_selectors.client_search.result_table_items, table_index)
        self.click_table_button(self.app_selectors.client_search.create_app_button)
        self.click_element(self.app_selectors.client_search.create_app_popup.create_new_app)

    def create_pledges(self, search_value, pledges, search_param='name'):
        self.click_table_button(self.app_selectors.app_creation.pledge.edit_pledge_button)
        self.click_element(self.app_selectors.app_creation.pledge.add_pledge_giver)
        self.print_to_input(self.app_selectors.client_search.filter[search_param], search_value)
        self.click_element(self.app_selectors.client_search.search_button)
        time.sleep(0.5)
        self.select_table_item(self.app_selectors.client_search.result_table_items, 0)
        self.click_element(self.app_selectors.app_creation.pledge.save_pledge_giver)

        if type(pledges) != list:
            pledges = [pledges]
        for pledge in pledges:
            self.click_table_button(self.app_selectors.app_creation.pledge.add_pledge)
            self.select_dropdown(self.app_selectors.app_creation.pledge.pledge_type, pledge.type)
            self.select_dropdown(self.app_selectors.app_creation.pledge.object_type, pledge.object_type)
            self.print_to_input(self.app_selectors.app_creation.pledge.pledge_descr, pledge.pledge_descr)
            self.click_button_from_group(self.app_selectors.app_creation.pledge.pledge_save_button, 0)
        
        self.click_element(self.app_selectors.app_creation.pledge.save_pledges)
    
    def create_app(self, client_name, client_param='name', table_index=0):
        self.login('sales_manager')
        # self.create_new_app(client_name, client_param, table_index)
        self.setup_stage('Заведение заявки')
        self.get_app_number()
        self.fill_app_params(
            'Прямая продажа', 
            'Разовый кредит', 
            'Год', 
            'Фиксированная', 
            'Единая', 
            10, 
            ['Индивидуальный график платежей', 'Аннуитетные платежи']
            )
        
        self.create_pledges(
            'альфа', 
            [
                dotify({'type': 'Нематериальные активы', 'object_type': 'Залог векселей', 'pledge_descr': 'Заложек'}),
                dotify({'type': 'Нематериальные активы', 'object_type': 'Залог ценных бумаг', 'pledge_descr': 'ЦБшчка'})
            ]
            )

        self.click_placeholder_button('to_accept')
        time.sleep(1)
        self.logout()
    
    @wait(5)
    def accept_new_app(self, app_number=None):
        self.login('sales_boss')
        if not self.app_params.app_number:
            self.app_params.app_number = app_number
        if not app_number:
            app_number = self.app_params.app_number
        if not app_number:
            raise 'Номер заявки пустой'
        
        self.setup_stage('Акцепт новой заявки')
        self.click_menu_item('На акцепт')
        self.click_element(self.app_selectors.task_search.clear_button)
        time.sleep(1)
        self.print_to_input(self.app_selectors.task_search.filter.app_number, app_number)
        self.select_dropdown(self.app_selectors.task_search.filter.task_status, 'Требуется акцепт')
        self.click_element(self.app_selectors.task_search.search_button)
        time.sleep(1)
        self.select_table_item(self.app_selectors.task_search.result_table_items, 0)
        self.click_table_button(self.app_selectors.task_search.to_work_button)
        time.sleep(1)
        self.click_placeholder_button('accept')
        time.sleep(1)
        self.logout()



    