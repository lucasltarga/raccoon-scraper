from selenium import webdriver
import scraper

'''RAccoon Scraper: A web scraper for extracting complaints from Reclame Aqui.
This script uses Selenium to navigate the Reclame Aqui website, extract complaint links,
and retrieve detailed information about each complaint.'''

def main():
    print("---- RAccoon Scraper ----\n")
    print("Starting scaper...")

    # Base URL for the company complaints on Reclame Aqui
    company_complaints_url = "https://www.reclameaqui.com.br/empresa/NOME_DA_EMPRESA/lista-reclamacoes/"
    
    # Generate URLs for pages 1 to 50 for the company complaints. 
    # Number of pages is limited to 50 as per the website's restrictions. 
    # For better results, consider scraping each category separately by passing a list of categories IDs as a parameter.
    pages = scraper.generate_list_of_pages(company_complaints_url)

    # Sample use
    # Loop through the first 5 pages to get complaint links and print them
    print("Fetching complaint links from the first 5 pages...")
    for page in pages[0:5]:
        # Initialize a new browser instance for each page to avoid session issues
        # This is necessary because Reclame Aqui may restrict automated access if the same session is used
        browser = webdriver.Chrome()
        browser.maximize_window()
        print(f"Getting links from {page}...")
        browser.get(page)
        links = scraper.get_links(browser)
        print(links)
        browser.close()

    #Uncomment the following lines to test with specific complaint links
    '''
    links = []
    # Loop through each complaint link and extract main details
    # Browser is reopened for each complaint to avoid automation restrictions
    for complaint in links:
        browser = webdriver.Chrome()
        browser.maximize_window()
        browser.get(complaint)
        scraper.get_complaint_from_browser(browser)
        browser.close()
    '''

    print("\nScraping done.")

if __name__ == '__main__':
    main()