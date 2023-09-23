from api.scenario import scenario_tester
import time

if __name__ == '__main__':
    for app_number in ['1395/1160']:
    # driver = scenario_tester()
        driver = scenario_tester(app_number)
        # driver.create_app()
        # driver.draft_app()
        # driver.accept_new_app()
        # driver.prescoring()
        # driver.prescoring_inform()
        # driver.prescoring_documents()
        # driver.expertises()
        # driver.sitting_create_task()    
        # driver.sitting_complete_task()
        # driver.send_to_inform('21.09.2023 00:00')
        # driver.inform_client_to_cod()
        # driver.cod()
        driver.cod_result()