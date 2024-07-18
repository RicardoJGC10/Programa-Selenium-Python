import json
from WikipediaScraper import WikipediaScraper
from AmazonScraper import AmazonScraper
from UTTorreonScraper import UTTorreonScraper

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
            scraper.scrape_data('wikipedia_data.xlsx')
            scraper.close_driver()
        elif option == "2":
            scraper = AmazonScraper('amazon.json')
            scraper.scrape_data('Amazon.xlsx')
            scraper.close_driver()
        elif option == "3":
            scraper = UTTorreonScraper('utt.json')
            scraper.scrape_data('UTT.xlsx')
            scraper.close_driver()
        elif option == "0":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor, ingrese un número válido.")

if __name__ == "__main__":
    main()
