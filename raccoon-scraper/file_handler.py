import os
import pandas as pd
from datetime import datetime

# RAccoon Scraper: File Handler Module

# Save all links retrieved from pages to a text file
def save_all_links(links, filename= None):
    if filename and not filename.endswith('.txt'):
        filename += '.txt'

    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"{timestamp}_links.txt"

    with open(filename, "w") as f:
        for link in links:
            f.write(link + "\n")
    print(f"Links saved to '{filename}'.")

# Load links from a file and return them as a list
def load_links_from_file(filepath="import_links.txt"):
    if os.path.exists(filepath):
            with open(filepath, "r") as f:
                return [line.strip() for line in f.readlines()]
    return []

# Load processed links from a file and return them as a list
def load_processed_links(filepath="last_processed_links.txt"):
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return [line.strip() for line in f.readlines()]
    return []

# Save complaints data to a CSV file and processed links to a txt file
def save_partial_data(complaints_data, processed_links):
    df = pd.DataFrame(complaints_data)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename_data = f"{timestamp}_complaints_data_partial.csv"
    df.to_csv(filename_data, index=False)

    with open("last_processed_links.txt", "w") as f:
        for link in processed_links:
            f.write(link + "\n")
    print(f"Partial data saved to '{filename_data}'.")
    print(f"Processed links saved to 'last_processed_links.txt'.")

def save_to_csv(complaints_data, filename = None):
    if filename and not filename.endswith('.csv'):
        filename += '.csv'

    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"{timestamp}_complaints_data.csv"

    df = pd.DataFrame(complaints_data)
    df.to_csv(filename, index=False)
    print(f"Data saved to '{filename}'.")
