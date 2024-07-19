import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

class WikipediaScraper:
    def __init__(self, config_file):
        self.config_file = config_file
        self.load_config()
        self.setup_driver()

    def load_config(self):
        with open(self.config_file) as f:
            config = json.load(f)
        self.site_config = config["wikipedia"]

    def setup_driver(self):
        opts = Options()
        opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)

    def scrape_data(self):
        self.driver.get(self.site_config["url"])
        self.driver.maximize_window()

        data = {}
        for field, info in self.site_config["fields"].items():
            elements = self.driver.find_elements(By.XPATH, info["selector"])
            data[info["column_name"]] = [getattr(el, info["data_attribute"]) for el in elements]
        
        return data  # Devolver los datos en lugar de exportar directamente

    def export_to_excel(self, data, output_file):
        df = pd.DataFrame(data)
        df.to_excel(output_file, index=False)
        print(f"Data exported to {output_file}")

    def close_driver(self):
        self.driver.quit()

# Ejemplo de uso:
if __name__ == "__main__":
    scraper = WikipediaScraper('wikipedia.json')
    data = scraper.scrape_data()  # Obtener los datos
    scraper.export_to_excel(data, 'wikipedia_data.xlsx')  # Exportar los datos
    scraper.close_driver()
