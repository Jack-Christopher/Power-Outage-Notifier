import re
import os
import json
import seeker
#import winsound
from sys import platform
from playsound import playsound
from datetime import date, timedelta
from colorama import init, Fore, Back, Style

if platform == "win32":
    clearScreenCommand = "cls"
elif platform == "linux" or platform == "linux2":
    clearScreenCommand = "clear"
    
# check if settings.json exists, if not, create it
def checkSettingsFile():
    if not os.path.isfile('settings.json'):
        # read districts from districts.txt
        with open("distritos.txt", "r", encoding="utf-8") as f:
            distritos = f.read().splitlines()
            i = 1
            distritos.sort()
            for dist in distritos:
                print(str(i) + ": " + dist)
                i += 1

        district_number = int(input("\nEnter District Number: "))
        district = distritos[district_number-1]
        print("\nSelected District: " + district)

        # add initial data to settings file
        with open("settings.json", "w+") as settings:
            temp_data = {
                "name": os.getlogin( ), 
                "district": district, 
                "last_check": str(date.today() - timedelta(days=1)),
                "driver_path": ""
            }
            json.dump(temp_data, settings, indent=4)
            print("\nSettings file created!")


# if the power outage have not been checked today, check it
def hasCheckedToday():
    with open('settings.json') as reader:
        settings = json.load(reader)
        today = str(date.today())
        if settings['last_check'] == today:
            print("Today is already checked, closing...")
            exit()


# get district from settings
def getDistrict():
    with open("settings.json", "r") as settings:
        data = json.load(settings)
        district = data["district"]
    return district


# mark today as checked
def checkToday():
    today = str(date.today())
    data = ""
    with open('settings.json', 'r') as settings:
        data = json.load(settings)
    with open('settings.json', 'w') as settings:
        data['last_check'] = today
        json.dump(data, settings, indent=4) 


# color all the appearances of target in the text
def color(text, target):
    return text.replace(target, Fore.CYAN + Back.BLUE + target + Style.RESET_ALL)


def printReports(reports):
    if len(reports) > 0:
        #for i in range(3):
            #winsound.Beep(1000, 250)
        playsound('Something wrong.wav')
        print("\nCorte de luz programado para el distrito de " + district + ":")
        for report in reports:
            print(color(report, district))
    else:
        print("No hay cortes de luz programados para el distrito de " + district + ".")
        playsound('All right.wav')



checkSettingsFile()
hasCheckedToday()
district = getDistrict()

# init source of data
print("Initializing...")
soup, driver = seeker.access("http://www.seal.com.pe/clientes/SitePages/Cortes.aspx")
os.system(clearScreenCommand)

# remove code blocks
soup.find('head').decompose()
soup.find('noscript').decompose()
soup = soup.find('form', id='aspnetForm')

id_list= []
data = re.findall(r'"Strings":\[.*\]', str(soup))[0]
data = re.findall(r'"\d{4}"', data)

for item in data:
    id_list.append(item.replace('"', ''))

# iterate over each power outage report
reports = []
for id_ in id_list:
    url = "http://www.seal.com.pe/clientes/Lists/Calendario/DispForm.aspx?ID=" + id_
    
    soup, driver = seeker.access(url, driver)
    table = soup.find('table', class_='ms-formtable')
    data = table.find_all('tr')

    report = ""
    found_data = False
    has_passed = False
    current_date = ""
    for item in data:
        title = item.find('span').text + ": "
        content = item.find('td', class_='ms-formbody').text.strip()
        if title == 'Hora de inicio: ':
            temp = content[:10].split("/")
            current_date = date(int(temp[2]), int(temp[1]), int(temp[0]))
            if current_date < date.today():
                has_passed = True
        if title == 'Descripción: ':
            if district.lower() in content.lower() and not has_passed:
                found_data = True
        block = title + content + '\n'
        if content != '':
            report += block

    report += '\n'

    if found_data:
        reports.append(report)

    os.system(clearScreenCommand)


driver.close()
checkToday()
printReports(reports)
