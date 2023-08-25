from api.scenario import scenario_tester
import time

if __name__ == '__main__':
    driver = scenario_tester()
    driver.create_app('сбербанк')
    driver.accept_new_app()
    