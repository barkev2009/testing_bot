from selenium import webdriver
import json
import os
import time

def get_driver():
    with open(os.path.join('config', 'config.json'), 'r') as file:
        config = json.load(file)

    browser = webdriver.Chrome()
    browser.get(config['app']['url'])
    return browser