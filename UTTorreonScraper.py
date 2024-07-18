import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

class UTTorreonScraper:
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
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

    def scrape_data(self, output_file):
        self.driver.get(self.site_config["url"])
        self.driver.maximize_window()

        for action in self.site_config["actions"]:
            element = self.driver.find_element(By.XPATH, action["selector"])
            if action["action"] == "slow_type":
                self.slow_type(element, action["value"], delay=action.get("delay", 0.1))
            elif action["action"] == "click":
                element.click()
            sleep(2)

        data = self.extract_table_data(self.site_config["tables"]["table1"]) + \
               self.extract_table_data(self.site_config["tables"]["table2"])

        df = pd.DataFrame(data)
        df.to_excel(output_file, index=False)  # Exportar al archivo especificado

    def slow_type(self, element, text, delay=0.1):
        for char in text:
            element.send_keys(char)
            sleep(delay)

    def extract_table_data(self, table_selector):
        table_data = []
        table_body = self.driver.find_element(By.XPATH, table_selector)
        rows = table_body.find_elements(By.XPATH, './/tr')
        for tr in rows:
            row = [item.text for item in tr.find_elements(By.XPATH, './/td')]
            if any(row):  # Verifica si la fila no está vacía
                table_data.append(row)
        return table_data

    def close_driver(self):
        self.driver.quit()

# Ejemplo de uso:
if __name__ == "__main__":
    scraper = UTTorreonScraper('utt.json')
    scraper.scrape_data('UTT.xlsx')  # Especifica el nombre del archivo de salida
    scraper.close_driver()
