from bs4 import BeautifulSoup
import requests
import json

req = requests.get('http://digidb.io/digimon-list/')
soup = BeautifulSoup(req.content, 'html.parser')

fullDat = soup.find('table', id='digiList')
modfDat1 = fullDat.find_all('tr')

# print(len(modfDat1)) #342
column = modfDat1[0]
toScrap = modfDat1[1:]
# print(len(toScrap))

ListDigi= []
for item in toScrap:
    num = int(item.td.string)
    name = item.a
    pict = item.img['src']
    stage = item.center
    tipe = item.td.find_next_sibling().find_next_sibling().find_next_sibling()
    attr = item.td.find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling()
    memo = attr.find_next_sibling()
    equ = memo.find_next_sibling()
    h_p_ = equ.find_next_sibling()
    s_p_ = h_p_.find_next_sibling()
    atk = s_p_.find_next_sibling()
    deff = atk.find_next_sibling()
    inte = deff.find_next_sibling()
    spd = inte.find_next_sibling()
    dictAppend = {'no' : num, 'digimon' : name.string, 'image' : pict,
    'stage': stage.string, 'type' : tipe.string, 'attribute' : attr.string, 'memory' : memo.string,
    'equip' : equ.string, 'HP' : h_p_.string, 'SP' : s_p_.string, 'atk' : atk.string, 
    'def': deff.string, 'int' : inte.string, 'spd' : spd.string} 
    ListDigi.append(dictAppend)
# print(ListDigi)
# print(len(ListDigi))


with open('digimon.json', 'w') as create:
    create.write(str(ListDigi).replace("'", '"'))


# column = soup.find_all('th').string

# print(len(soup.find('table', id='digiList'))) #4
# soup.find_all('body')

#### =============================== ######

# data = soup.find_all('tbody')

# dataDigi = []
# for i in data:
#     noDigi = i.text
#     noDigi_mod = {"id" : noDigi}
#     dataDigi.append(noDigi_mod)

# print(dataDigi)


# data2 = soup.find_all('td')

# dataDigi = []
# for i in data2:
#     noDigi = i.text
#     noDigi_mod = {"id" : noDigi}
#     dataDigi.append(noDigi_mod)

# print(dataDigi[:10])

# data3 = soup.find_all('td')
# print(len(data3)) #4433 data

# dataKuramon = data3[1:13]