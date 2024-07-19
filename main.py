import json
from WikipediaScraper import WikipediaScraper
from AmazonScraper import AmazonScraper
from UTTorreonScraper import WebScraper

def print_menu():
    print("Seleccione una opción:")
    print("1. Wikipedia")
    print("2. Amazon")
    print("3. UTTorreon")
    print("0. Salir")

def main():
    while True:
        print_menu()
        option = input("Ingrese el número de la opción que desea ejecutar: ")

        if option == "1":
            scraper = WikipediaScraper('wikipedia.json')
            data = scraper.scrape_data()  # Llamada sin parámetros
            scraper.export_to_excel(data, 'wikipedia_data.xlsx')  # Exportar datos
            scraper.close_driver()
        elif option == "2":
            scraper = AmazonScraper('amazon.json')
            data = scraper.scrape_data()  # Llamada sin parámetros
            scraper.export_to_excel(data, 'Amazon.xlsx')  # Exportar datos
            scraper.close_driver()
        elif option == "3":
            scraper = WebScraper('utt.json')
            data = scraper.scrape_data()  # Llamada sin parámetros
            scraper.export_to_excel(data, 'UTT.xlsx')  # Exportar datos
            scraper.close_driver()
        elif option == "0":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor, ingrese un número válido.")

if __name__ == "__main__":
    main()
