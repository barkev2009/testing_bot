from api.scenario import scenario_tester
import time

def test_new_app(func_list):
    driver = scenario_tester()
    for func in func_list:
        func[0](driver, **func[1])

def test_existing_app(func_list, app_numbers):
    for app_number in app_numbers:
        driver = scenario_tester(app_number)
        for func in func_list:
            func[0](driver, **func[1])

if __name__ == '__main__':
    funcs = [
        # [scenario_tester.create_app, {}],
        # [scenario_tester.draft_app, {'pledges_count': 1, 'parts_count': 1}],
        # [scenario_tester.accept_new_app, {}],
        # [scenario_tester.prescoring, {}],
        # [scenario_tester.prescoring_inform, {}],
        # [scenario_tester.prescoring_documents, {}],
        # [scenario_tester.expertises, {}],
        # [scenario_tester.sitting_create_task, {}],
        # [scenario_tester.sitting_complete_task, {}],
        # [scenario_tester.send_to_inform, {}],
        # [scenario_tester.inform_client_to_cod, {}],
        # [scenario_tester.cod, {}],
        # [scenario_tester.cod_result, {}],
        # [scenario_tester.deal_prep_start, {}],
        # [scenario_tester.deal_prep_req_acc_docs, {}],
        # [scenario_tester.deal_prep_accept_req_docs, {}],
        # [scenario_tester.deal_prep_open_acc, {}],
        # [scenario_tester.deal_prep_req_acc_docs, {'task_type': 'Реквизиты расчетного и/или залогового счета'}],
        # [scenario_tester.deal_prep_accept_req_docs, {}],
        # [scenario_tester.deal_prep_end, {}],
        [scenario_tester.deal, {}],
    ]
    # test_new_app(funcs)
    test_existing_app(funcs, ['1577/1342'])
    # driver = scenario_tester()
    # driver.login('sales_boss')