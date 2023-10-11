from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import os
import time

def get_driver():
    with open(os.path.join('config', 'config.json'), 'r', encoding='utf-8') as file:
        config = json.load(file)

    options = Options()
    options.add_argument("--start-maximized")

    browser = webdriver.Chrome(options)
    browser.get(config['app']['url'])
    return browser