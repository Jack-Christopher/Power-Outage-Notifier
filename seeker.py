import os
import json
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager


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
            driver = webdriver.Edge(options=options, service=EdgeService(executable_path=getExecPath()))
        except:
            print("Driver not found. Installing...")
            service = EdgeService(EdgeChromiumDriverManager( path=r"").install())
            setExecPath(service.path)
            driver = webdriver.Edge(service=service, options=options)
            os.system("cls")
    print("Accesing site: '" + url + "'")
    driver.get(url)    
    driver.implicitly_wait(time_to_wait=7)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    return soup, driver

def closer(driver):
    driver.close()
