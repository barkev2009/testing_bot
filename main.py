from api.testdriver import testdriver
import time

if __name__ == '__main__':
    driver = testdriver()
    driver.login('sales_manager')
    driver.find_client('name', 'сбербанк')
    driver.logout()
    driver.login('sales_boss')
    driver.find_client('name', 'бтк')
    driver.logout()
    