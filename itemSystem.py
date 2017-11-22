import mysql.connector
import time
import random

def keraaItem(itemId):  #item id, esim 1 = kirja 2 = taikahattu tms.
    itemNimi = ""
    cur = db.cursor()
    sqlItemNimi = "SELECT name From  itemtype WHERE itemtype.ITID = "+str(itemId)  #Itemin nimi katsotaan listasta
    cur.execute(sqlItemNimi)
    result = cur.fetchall()
    for row in result:                  #asetetaan itemin nimi id:n mukaan alla olevaan kyselyyn jossa kysytään otetaanko esim kirja haltuun
            print("Item nimi: "+row[0])
            itemNimi = str(row[0])

    #Kysytään otetaanko kyseinen esine haltuun
    ke = input("ota "+itemNimi+" (k/e)?")    
    if(ke=="k"):
        sql = "UPDATE item SET Pid = 1 WHERE iid = "+str(itemId) #päivitetään itemi pelaajan haltuun
        cur.execute(sql)
        sql
    return



#annetaan itemin nimi joka opettaa taian
def itemTaiaksi(itemNimi, taikaNimi):
    print(itemNimi+" opettaa "+taikaNimi+":n")
    #tulostaa pelaajan tämän hetkiset itemit
    lista = pelaajanItemit()  
    print("Pelaajalla hallussa:")
    print(lista)
    #tarkastetaan omistaako pelaaja tämän itemin ja sen mukaan annetaan taianoppiminen
    for i in range(0,len(lista)):
        if(lista[i] == itemNimi):
            taianOppiminen(taikaNimi)
    return


def taianOppiminen(taianNimi):  #Lisätään pelaajan osaamiin taikoihin uusi taika
    cur = db.cursor()
    sql = "INSERT INTO playermagic values ( (SELECT MagicId FROM magic WHERE name = "+taianNimi+",1);" #Pelaajan osaamiseen lisätään haluttu taian nimi
    cur.execute(sql)
    print("Taika lisätty!")
    return






def pelaajanItemit(): #Pelaajan hallussa olevat itemit
    cur = db.cursor()
    sql = "SELECT name From itemtype, item WHERE itemtype.ITID = item.ITID AND item.PID = 1"
    cur.execute(sql)
    result = cur.fetchall()
    return result



# avataan yhteys tietokantaan
db = mysql.connector.connect(
    host = "localhost",
    user = "dbuser",
    passwd = "dbpass",
    db = "dad",
    buffered = True)
print("Tietokantayhteys on avattu")

keraaItem(1)
itemTaiaksi("Kirja","FrosBolt")

# suljetaan tietokantayhteys
db.close()
print("Tietokantayhteys on suljettu")
