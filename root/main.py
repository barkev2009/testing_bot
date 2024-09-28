from root.api.scenario import scenario_tester
from root.api.utils import exit_with_grace

@exit_with_grace
def test_new_app(func_list):
    try:
        driver = scenario_tester()
        for func in func_list:
            func[1](driver, **func[2])
    except Exception as e:
        pass

@exit_with_grace
def test_existing_app(func_list, app_numbers):
    try:
        for app_number in app_numbers:
            driver = scenario_tester(app_number)
            for func in func_list:
                func[1](driver, **func[2])
    except Exception as e:
        pass

def get_all_functions():
    return [
        ['Создание заявки', scenario_tester.create_app, {}],
        ['Первичное заполнение заявки', scenario_tester.draft_app, {'pledges_count': 0, 'parts_count': 0}],
        ['Акцепт новой заявки', scenario_tester.accept_new_app, {}],
        ['Прескоринг', scenario_tester.prescoring, {}],
        ['Информирование клиента о прескоринге', scenario_tester.prescoring_inform, {}],
        ['Запрос необходимых документов', scenario_tester.prescoring_documents, {}],
        ['Экспертизы (начало)', scenario_tester.expertises, {}],
        ['Заведение задачи на рассмотрение КК', scenario_tester.sitting_create_task, {}],
        ['Завершение задачи на рассмотрение КК', scenario_tester.sitting_complete_task, {}],
        ['Отправка задачи на информирование клиента о проведении КК', scenario_tester.send_to_inform, {}],
        ['Информирование клиента о проведении КК', scenario_tester.inform_client_to_cod, {}],
        ['Подготовка КОД', scenario_tester.cod, {}],
        ['Согласование КОД', scenario_tester.cod_result, {}],
        ['Подготовка к сделке (заведение задачи на запрос документов для открытия счета)', scenario_tester.deal_prep_start, {}],
        ['Запрос документов для открытия счета', scenario_tester.deal_prep_req_acc_docs, {}],
        ['Акцепт задачи на запрос документов для открытия счета', scenario_tester.deal_prep_accept_req_docs, {}],
        ['Открытие счета', scenario_tester.deal_prep_open_acc, {}],
        ['Запрос реквизитов счета', scenario_tester.deal_prep_req_acc_docs, {'task_type': 'Реквизиты расчетного и/или залогового счета'}],
        ['Акцепт запроса реквизитов счета', scenario_tester.deal_prep_accept_req_docs, {}],
        ['Подготовка к сделке (завершение)', scenario_tester.deal_prep_end, {}],
        ['Сделка', scenario_tester.deal, {}],
    ]

if __name__ == '__main__':
    funcs = get_all_functions()
    # test_new_app(funcs)
    # test_existing_app(funcs, ['1611/1376'])

    # driver = scenario_tester()
    # driver.change_application()
