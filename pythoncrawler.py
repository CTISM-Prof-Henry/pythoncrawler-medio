from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os


def main():
    if os.name == 'nt':
        path = './geckodriver.exe'
    else:
        path = './geckodriver'

    with webdriver.Firefox(executable_path=path) as driver:
        # abre o site
        driver.get('https://www.netshoes.com.br/tenis-asics-gelbackhand-feminino-azul+roxo-2FV-8420-977%27')

        precotenis1 = driver.find_element_by_tag_name("strong")
        print(precotenis1.text)
        time.sleep(10)  # dorme uns 10 segundos, para dar tempo de ver a página


if __name__ == '__main__':
    main()