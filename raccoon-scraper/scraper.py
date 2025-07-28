from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Gets all links for the complaints on the current page and returns them as a list
def get_links(browser):
    complaints = browser.find_elements("id", "site_bp_lista_ler_reclamacao")
    
    link_list = [complaint.get_attribute("href") for complaint in complaints]

    return link_list

# Generates URLs for page from 1 to 50 and returns them as a list
def generate_list_of_pages(base_url, categories = None):
    urls = []
    if categories is not None:
        for category in categories:
            for page in range(1, 51):  # Pages from 1 to 50
                url = f"{base_url}?pagina={page}&categoria={category}"
                urls.append(url)
    else:
        for page in range(1, 51):  # Pages from 1 to 50
            url = f"{base_url}?pagina={page}"
            urls.append(url)
    return urls

def get_complaint_from_browser(browser):
    wait = WebDriverWait(browser, 10)

    id = wait.until(EC.presence_of_element_located(("class name", "sc-lzlu7c-12"))).text
    title = wait.until(EC.presence_of_element_located(("class name", "sc-lzlu7c-3"))).text
    status = wait.until(EC.presence_of_element_located(("class name", "sc-1a60wwz-1"))).text
    user_message = wait.until(EC.presence_of_element_located(("class name", "sc-lzlu7c-17"))).text
    local = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[data-testid='complaint-location']"))).text
    date_time = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[data-testid='complaint-creation-date']"))).text

    print(f"{id}\n"
          f"Title: {title}\n"
          f"Status: {status}\n"
          f"User message: {user_message}\n"
          f"Local: {local}\n"
          f"Date and time: {date_time}\n")
    