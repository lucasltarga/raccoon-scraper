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
    
    dictDF = {"id": id,
        "title": title,
        "status": status,
        "user_message": user_message,
        "local": local,
        "date_time": date_time}
    return dictDF

def get_replies_from_browser(browser):
    titles = browser.find_elements(By.CSS_SELECTOR, "h2.sc-1o3atjt-2")
    dates = browser.find_elements(By.CSS_SELECTOR, "span.sc-1o3atjt-3")
    messages = browser.find_elements(By.CSS_SELECTOR, "p.sc-1o3atjt-4")

    # Combine titles, dates and messages into a list of dictionaries
    # Each dictionary contains a title and its corresponding message
    title_message_pairs = []
    for title_elem, date_elem, message_elem in zip(titles, dates, messages):
        # Combine title and date into a single string
        combined_title = f"{title_elem.text} em {date_elem.text}"
        
        title_message_pairs.append({
            "title": combined_title,
            "message": message_elem.text
        })
    
    # Display the title and text pairs on the screen:
    for pair in title_message_pairs:
        print(f"Reply title: {pair['title']}\nReply text: {pair['message']}\n")

    return title_message_pairs