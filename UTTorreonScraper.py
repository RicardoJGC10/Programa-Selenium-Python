import json
import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import pandas as pd

class WebScraper:
    def __init__(self, config_file):
        self.config_file = config_file
        self.load_config()
        self.setup_driver()

    def load_config(self):
        with open(self.config_file) as f:
            config = json.load(f)
        self.site_config = config["uttorreon"]

    def setup_driver(self):
        opts = Options()
        opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
        self.driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))


    def slow_type(self, element, text, delay=0.1):
        for char in text:
            element.send_keys(char)
            time.sleep(delay)

    def perform_actions(self):
        for action in self.site_config.get("actions", []):
            if action["action"] == "slow_type":
                element = self.driver.find_element(By.XPATH, action["selector"])
                self.slow_type(element, action["value"], action["delay"])
            elif action["action"] == "send_keys":
                element = self.driver.find_element(By.XPATH, action["selector"])
                element.send_keys(action["value"])
            elif action["action"] == "click":
                element = self.driver.find_element(By.XPATH, action["selector"])
                element.click()
            time.sleep(2)  # Esperar un poco entre acciones

    def scrape_table(self):
        table_body = self.driver.find_element(By.XPATH, self.site_config["table_selector"])
        data = []

        for tr in table_body.find_elements(By.XPATH, './/tr'):
            row = [item.text for item in tr.find_elements(By.XPATH, './/td')]
            data.append(row)

        return data

    def scrape_data(self):
        self.driver.get(self.site_config["url"])
        self.driver.maximize_window()

        # Realizar acciones si hay alguna
        self.perform_actions()

        # Extraer datos de la tabla
        data = self.scrape_table()
        
        return data

    def export_to_excel(self, data, output_file):
        df = pd.DataFrame(data)
        df.to_excel(output_file, index=False)
        print(f"Data exported to {output_file}")

    def close_driver(self):
        self.driver.quit()

# Ejemplo de uso:
if __name__ == "__main__":
    scraper = WebScraper('uttorreon.json')
    data = scraper.scrape_data()  # Llamada correcta sin parámetros
    scraper.export_to_excel(data, 'UTT.xlsx')
    scraper.close_driver()
