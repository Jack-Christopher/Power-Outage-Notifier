import re
import seeker

# read distritos.txt
with open("distritos.txt", "r", encoding="utf-8") as f:
    distritos = f.read().splitlines()
    i = 1
    # sort by length
    # distritos.sort(key=len)
    distritos.sort()
    for dist in distritos:
        print(str(i) + ": " + dist)
        i += 1

district = int(input("\nDistrict: "))
district = distritos[district-1]
print("\nDistrict: " + district)


soup, driver = seeker.access("http://www.seal.com.pe/clientes/SitePages/Cortes.aspx")

# remove code blocks
soup.find('head').decompose()
soup.find('noscript').decompose()
soup = soup.find('form', id='aspnetForm')

id_list= []
with open("cortes.txt", "w") as f:
    data = re.findall(r'"Strings":\[.*\]', str(soup))[0]
    data = re.findall(r'"\d{4}"', data)
    
    for item in data:
        id_list.append(item.replace('"', ''))

# file in utf-8
data_file = open("cortes.txt", "w", encoding="utf-8")

for id_ in id_list:
    url = "http://www.seal.com.pe/clientes/Lists/Calendario/DispForm.aspx?ID=" + id_
    
    soup, driver = seeker.access(url, driver)
    table = soup.find('table', class_='ms-formtable')
    data = table.find_all('tr')

    report = ""
    must_show = False
    for item in data:
        title = item.find('span').text + ": "
        content = item.find('td', class_='ms-formbody').text.strip()
        if title == 'Descripción: ':
            # content_ = content.lower()
            # print(content_)
            # reason = re.search(r'motivo(.+)(.+\n)*', content_).group(1)
            # affected = re.search(r'zonas afectadas(.*): (.+)(.+\n)*', content_).group(1)
            # content = "Motivo: " + reason + '\nZonas afectadas: ' + affected 
            # title = ""
            # if district.lower() in affected.lower():
                # must_show = True
            if district.lower() in content.lower():
                must_show = True
        block = title + content + '\n'
        if content != '':
            report += block

    report += '\n'
    # data_file.write(report)

    if must_show:
        print(report)

driver.close()