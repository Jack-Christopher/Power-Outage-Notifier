import os
import json
from sys import platform
from bs4 import BeautifulSoup

from selenium import webdriver


# using microsoft edge
if platform == "win32":
    from selenium.webdriver.edge.options import Options
    from selenium.webdriver.edge.service import Service as EdgeService
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    DriverCreator = webdriver.Edge
    ServiceProvider = EdgeService
    DriverManager = EdgeChromiumDriverManager
# using firefox
elif platform == "linux" or platform == "linux2":
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.firefox.service import Service as FirefoxService
    from webdriver_manager.firefox import GeckoDriverManager
    DriverCreator = webdriver.Firefox
    ServiceProvider = FirefoxService
    DriverManager = GeckoDriverManager
elif platform == "darwin":
    exit( "MacOS is not supported yet" )



def setExecPath(path):
    with open("settings.json", "r") as settings:
        data = json.load(settings)
        data["driver_path"] = path
    with open("settings.json", "w") as settings:
        json.dump(data, settings, indent=4)

def getExecPath():
    with open("settings.json", "r") as settings:
        data = json.load(settings)
        return data["driver_path"]

options = Options()
options.add_argument("--headless")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-gpu")
# options.add_argument("--allow-insecure-localhost")
options.add_argument("--log-level=3")

def access(url, driver=None):
    if driver is None:
        try :
            driver = DriverCreator(options=options, service=ServiceProvider(executable_path=getExecPath()))
        except:
            print("Driver not found. Installing...")
            service = ServiceProvider(DriverManager( path=r"").install())
            setExecPath(service.path)
            driver = DriverCreator(service=service, options=options)
            os.system("cls")
    print("Accesing site: '" + url + "'")
    driver.get(url)    
    driver.implicitly_wait(time_to_wait=7)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    return soup, driver

def closer(driver):
    driver.close()
