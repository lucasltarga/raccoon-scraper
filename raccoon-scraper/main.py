from selenium import webdriver
import scraper
import pandas as pd
import time
import random

'''RAccoon Scraper: A web scraper for extracting complaints from Reclame Aqui.
This script uses Selenium to navigate the Reclame Aqui website, extract complaint links,
and retrieve detailed information about each complaint.'''

def main():
    print("---- RAccoon Scraper ----\n")
    print("Starting scaper...")

    # Base URL for the company complaints on Reclame Aqui
    company_complaints_url = "https://www.reclameaqui.com.br/empresa/NOME_DA_EMPRESA/lista-reclamacoes/"
    
    # Categories for the complaints. You can specify categories by their IDs.
    categories = []

    # Generate URLs for pages 1 to 50 for the company complaints. 
    # Number of pages is limited to 50 as per the website's restrictions. 
    # For better results, consider scraping each category separately by passing a list of categories IDs as a parameter.
    pages = scraper.generate_list_of_pages(company_complaints_url, categories)
    links = []

    # Sample use
    # Loop through the first 5 pages to get complaint links and print them
    print("Fetching complaint links from the first 50 pages...")
    for page in pages[0:50]:
        # Initialize a new browser instance for each page to avoid session issues
        # This is necessary because Reclame Aqui may restrict automated access if the same session is used
        options = webdriver.ChromeOptions()
        options.page_load_strategy = "none"
        browser = webdriver.Chrome(options=options)
        browser.maximize_window()
        print(f"Getting links from {page}...")
        browser.get(page)
        new_links = scraper.get_links(browser)
        browser.close()

        if not new_links: 
            print("No new links found. Stopping page search.")
            break

        links += new_links

    # Loop through each complaint link and extract main details
    # Browser is reopened for each complaint to avoid automation restrictions
    complaints_data = []
    replies = []
    processed_links = []
    
    try:
        for complaint in links:
            options = webdriver.ChromeOptions()
            options.page_load_strategy = "none"
            browser = webdriver.Chrome(options=options)
            browser.maximize_window()
            browser.get(complaint)
            time.sleep(random.uniform(6, 10))  # Wait a random time to avoid being blocked
            complaint_data = scraper.get_complaint_from_browser(browser)
            replies = scraper.get_replies_from_browser(browser)

            formatted_replies = "\n-----------------------------\n".join(
                f"{reply['title']}\n\n{reply['message']}" for reply in replies
            )

            complaint_data['replies'] = formatted_replies
            complaints_data.append(complaint_data)
            processed_links.append(complaint)
            browser.close()
    except Exception as e:
        print(f"An error occurred: {e}")

        # Save data collected so far
        df = pd.DataFrame(complaints_data)
        df.to_csv("complaints_data_partial.csv", index=False)
        with open("processed_links.txt", "w") as f:
            for link in processed_links:
                f.write(link + "\n")
        print("Partial data saved to complaints_data_partial.csv")
        print("Processed links saved to processed_links.txt")
        return

    df = pd.DataFrame(complaints_data)
    df.to_csv("complaints_data.csv", index=False)
    print("Data saved to complaints_data.csv")
    print("\nScraping done.")

if __name__ == '__main__':
    main()