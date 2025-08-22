import scraper
import file_handler

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
    
    imported_file = file_handler.load_links_from_file()
    print(imported_file)
    if imported_file:
        print(f"Importing {len(imported_file)} links from 'import_links.txt'...")
        # If links are imported from a file, skip the link fetching process
        links = imported_file
    
    else:
        # Generate URLs for pages 1 to 50 for the company complaints.
        print("Generating URLs for pages 1 to 50...")
        pages = scraper.generate_list_of_pages(company_complaints_url, categories)
        
        # Fetch complaint links from the pages
        print(f"Fetching complaint links from {len(pages)} pages...")
        links = scraper.get_links_from_multiple_pages(pages)
        print(f"Found {len(links)} links.")
        file_handler.save_all_links(links)
    
    # Load previously processed links from last_processed_links.txt to avoid duplicates
    processed_links = file_handler.load_processed_links()
    # Filter out links that have already been processed
    links = [link for link in links if link not in processed_links]

    # Scraping complaints data from the links
    complaints_data, processed_links, error_ocurred = scraper.scrape_complaints(links, processed_links)

    # Save the final data to CSV
    if complaints_data:
        if not error_ocurred:
            file_handler.save_to_csv(complaints_data)
        else:
            print("An error occurred during scraping. Saving partial data...")
            file_handler.save_partial_data(complaints_data, processed_links)
    else:
        print("No complaints data to save.")

    print("\nScraping done.")

if __name__ == '__main__':
    main()