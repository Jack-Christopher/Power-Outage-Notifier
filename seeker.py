from selenium import webdriver
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup


# with open("days.txt", "w") as f:
#     dates = re.search(r'"Dates":\["(.*?)"\]', str(soup)).group(1)
#     for date in dates.split(','):
#         f.write(date.replace('"', '') + '\n')

# no all links are rendered
# http://www.seal.com.pe/clientes/Lists/Calendario/DispForm.aspx?ID=2670


def access(url, driver=None):
    print("Starting...")
    options = Options()
    options.add_argument("--headless")

    if driver is None:
        driver = webdriver.Edge(options=options)
    # driver.get("http://www.seal.com.pe/clientes/SitePages/Cortes.aspx")
    driver.get(url)
    
    driver.implicitly_wait(time_to_wait=5)
    print("Ready!")

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    return soup, driver


def closer(driver):
    driver.close()



