import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

myList = []
priceList = []
mList = []
ageList = []
locationList = []
floorList = []
roomm=[]

for i in range(2, 2400):      #sayfa aralığı
    page = "?page=" + str(i)  #urlye göre sayfalama
    myList.append(page)
    
for otherUrl in myList:
    url = "https://www.hepsiemlak.com/istanbul-satilik" + otherUrl  #sayfa sayfa atlama
    page = requests.get(url)
    html = page.content
    soup = BeautifulSoup(html, "html.parser")
    mylist = soup.find("ul", {"class": "list-items-container"})
    if mylist is not None:
        mylist = mylist.find_all("li")
        for item in mylist:
            try:
                price = item.find_next("span", {"class": "list-view-price"}).text.replace("\n", "").replace("TL", "").replace(".", "")
                m = int(item.find_next("span", {"class": "celly squareMeter list-view-size"}).text.strip().replace("m2", ""))
                age = int(item.find_next("span", {"class": "celly buildingAge"}).text.replace("Sıfır Bina", "0"))
                room = item.find_next("span", {"class": "celly houseRoomCount"}).text
                location = item.find_next("div", {"class": "list-view-location"}).find_all_next("span")[0].text.strip().replace(",", "")
                floor = int(item.find_next("span", {"class": "celly floortype"}).text.strip().replace(". Kat", "").replace("Zemin Kat", "0"))
                roomm.append(room)
                priceList.append(price)
                mList.append(m)
                ageList.append(age)
                locationList.append(location)
                floorList.append(floor)
            except:
                continue

myData = {"PRICE": priceList,"ROOM":room , "AREA": mList, "AGE": ageList, "LOCATION": locationList, "FLOOR": floorList}
myFrame = pd.DataFrame(myData)

# Dosyaya yazma
file_path = "satilik_evler.csv"
myFrame.to_csv(file_path, index=False,mode="a") # En yukardaki döngüyü 2-2400 arası olarak çalıştırdığımda çok zaman sürdü
                                                 #bu yüzden 2-300 ,300-600... el ile kısa sayı aralıkları bırakarak csv dosyasının sonuna eklemesini istedim

# Dosyanın kaydedildiğinden emin olmak için kontrol mesajı yazdırma
if os.path.exists(file_path):
    print(f"Dosya başarıyla kaydedildi: {os.path.abspath(file_path)}")
else:
    print("Dosya kaydedilemedi!")
