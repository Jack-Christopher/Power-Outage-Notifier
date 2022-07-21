import re
import os
import json
import seeker
import winsound
from datetime import date, timedelta
from colorama import init, Fore, Back, Style

# check if settings.json exists, then create it
if not os.path.isfile('settings.json'):
    # read districts from districts.txt
    with open("distritos.txt", "r", encoding="utf-8") as f:
        distritos = f.read().splitlines()
        i = 1
        distritos.sort()
        for dist in distritos:
            print(str(i) + ": " + dist)
            i += 1

    district = int(input("\nDistrict: "))
    district = distritos[district-1]
    print("\nDistrict: " + district)

    # add district and yesterday date to settings
    with open("settings.json", "w+") as settings:
        temp_data = {"name": os.getlogin( ), "district": district, "last_check": str(date.today() - timedelta(days=1))}
        json.dump(temp_data, settings, indent=4)
        print("\nSettings file created!")


# if the power outage have not been checked today, check it
with open('settings.json') as reader:
    settings = json.load(reader)
    today = str(date.today())
    if settings['last_check'] == today:
        print("Today is already checked, closing...")
        exit()
    else:
        settings['last_check'] = today
        with open('settings.json', 'w') as writer:
            json.dump(settings, writer, indent=4)


# get district from settings
with open("settings.json", "r") as settings:
    data = json.load(settings)
    district = data["district"]


soup, driver = seeker.access("http://www.seal.com.pe/clientes/SitePages/Cortes.aspx")
os.system("cls")

# remove code blocks
soup.find('head').decompose()
soup.find('noscript').decompose()
soup = soup.find('form', id='aspnetForm')

id_list= []
data = re.findall(r'"Strings":\[.*\]', str(soup))[0]
data = re.findall(r'"\d{4}"', data)

for item in data:
    id_list.append(item.replace('"', ''))

reports = []

# iterate over each power outage report
for id_ in id_list:
    url = "http://www.seal.com.pe/clientes/Lists/Calendario/DispForm.aspx?ID=" + id_
    
    soup, driver = seeker.access(url, driver)
    os.system("cls")
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

driver.close()

# store reports in a file json
# with open("reports.json", "w+") as reports_file:
    # json.dump(reports, reports_file, indent=4)

# color all the appearances of target in the text
def color(text, target):
    return text.replace(target, Fore.CYAN + Back.BLUE + target + Style.RESET_ALL)




if len(reports) > 0:
    for i in range(3):
        winsound.Beep(1000, 250)
    print("\nCorte de luz programado para el distrito de " + district + ":")
    for report in reports:
        print(color(report, district))