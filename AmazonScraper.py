import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

class AmazonScraper:
    def __init__(self, config_file):
        self.config_file = config_file
        self.load_config()
        self.setup_driver()

    def load_config(self):
        with open(self.config_file) as f:
            config = json.load(f)
        self.site_config = config["amazon"]

    def setup_driver(self):
        opts = Options()
        opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

    def scrape_data(self):
        self.driver.get(self.site_config["url"])
        self.driver.maximize_window()

        for action in self.site_config["actions"]:
            if action["action"] == "send_keys":
                element = self.driver.find_element(By.XPATH, action["selector"])
                element.send_keys(action["value"])
            elif action["action"] == "click":
                element = self.driver.find_element(By.XPATH, action["selector"])
                element.click()
                time.sleep(2)

        pg_amount = self.site_config["max_pages"]
        data = []
        for i in range(pg_amount):
            names = self.driver.find_elements(By.XPATH, self.site_config["fields"]["name"])
            prices = self.driver.find_elements(By.XPATH, self.site_config["fields"]["price"])
            links = self.driver.find_elements(By.XPATH, self.site_config["fields"]["link"])

            for name, price, link in zip(names, prices, links):
                data.append({
                    "Nombre": name.text,
                    "Precio": price.text,
                    "Link": link.get_attribute('href')
                })

            try:
                next_btn = self.driver.find_element(By.XPATH, self.site_config["pagination"]["next_button_selector"])
                next_btn.click()
                time.sleep(2)
            except Exception as e:
                print(f"No se pudo encontrar el botón de siguiente página en la página {i+1}: {e}")
                break
        
        return data  # Devolver los datos en lugar de exportar directamente

    def export_to_excel(self, data, output_file):
        df = pd.DataFrame(data)
        df.to_excel(output_file, index=False)
        print(f"Data exported to {output_file}")

    def close_driver(self):
        self.driver.quit()

# Ejemplo de uso:
if __name__ == "__main__":
    scraper = AmazonScraper('amazon.json')
    data = scraper.scrape_data()  # Obtener los datos
    scraper.export_to_excel(data, 'Amazon.xlsx')  # Exportar los datos
    scraper.close_driver()
