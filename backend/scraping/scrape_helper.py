import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup
import scraping.scraping_llm as scraping_llm

def scrape_website(website_url):

    chrome_driver_path = ""  
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        driver.get(website_url)

        time.sleep(5)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser') 
        
        content = soup.get_text()
        modified_content = scraping_llm.extract_information(content)
        return modified_content

    finally:
        driver.quit()

# if __name__ == "__main__":
#     website_url = "https://www.nccu.edu/news/nccu-law-and-technology-symposium-and-summit-oct-10-11"
#     content = scrape_website(website_url)
    
#     print(content)