from root.api.testdriver import testdriver, retry
from root.api.utils import dotify

import time

class draft_app(testdriver):
    def __init__(self) -> None:
        super().__init__()
    
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
    def draft_app(self, pledges_count=0, parts_count=0):
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
        
        pledges = []
        if pledges_count != 0:
            pledges = [
                dotify({'type': 'Нематериальные активы', 'object_type': 'Залог векселей', 'pledge_descr': f'Заложек {i + 1}'})
                for i in range(pledges_count)
            ]
        if pledges:
            self.create_pledges('альфа', pledges)
        
        participants = []
        if parts_count != 0:
            participants = [
                dotify({'type': f'Поручительство {i + 1}', 'search_value': 'альфа'})
                for i in range(parts_count)
            ]
        if participants:
            self.create_participants(participants)

        self.click_placeholder_button('to_accept')
        time.sleep(2)
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