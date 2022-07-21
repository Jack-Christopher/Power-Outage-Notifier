from selenium import webdriver
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup

def access(url, driver=None):
    # print("Starting...")
    options = Options()
    options.add_argument("--headless")

    if driver is None:
        driver = webdriver.Edge(options=options)
    
    driver.get(url)    
    driver.implicitly_wait(time_to_wait=5)
    # print("Ready!")

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    return soup, driver


def closer(driver):
    driver.close()



