import mysql.connector
import time
import random

vihuElossa = [True, True, True] #id:n mukaan järjestykseen vihut, jos false niin vihu on kuollut
pelaajaElossa = True

def pelaajaIske(dmg, vihuId):
    print("Pelaaja iskee "+str(dmg))
    cur = db.cursor()
    #Otetaan nykyinen hp
    sqlHp = "select kunto from vihollinen where id = "+str(vihuId)   
    cur.execute(sqlHp)
    result = cur.fetchall()
    for row in result:
            hp = row[0]
    hp = hp-dmg
    #Muutetaan Hp
    sql = "UPDATE vihollinen SET kunto = "+str(hp)+" WHERE id = "+str(vihuId)
    cur.execute(sql)
    sql2 = "select kunto from vihollinen where id = "+str(vihuId)
    cur.execute(sql2)                                  
    result = cur.fetchall()
    # Tulostetaan tuloslistan tiedot rivi kerrallaan
    for row in result:
            hp = int(row[0])
    print("Vihun hp: "+str(hp))
    if hp <= 0:
        #vihu kuolee
        print("KUOLLUT")
        vihuElossa[vihuId-1] = False
    return

def vihuIske(dmg, vihuId):
    print("                        Vihu nro."+str(vihuId+1)+" iskee "+str(dmg))
    cur = db.cursor()
    sqlHp = "select kuntopisteet from pelihahmo"
    cur.execute(sqlHp)
    result = cur.fetchall()
    for row in result:
            hp = row[0]
    hp = hp-dmg
    sql = "UPDATE pelihahmo SET kuntopisteet = "+str(hp)
    cur.execute(sql)
    sql2 = "select kuntopisteet from pelihahmo where id = 1"
    cur.execute(sql2)
    result = cur.fetchall()
    # Tulostetaan tuloslistan tiedot rivi kerrallaan
    for row in result:
            hp = int(row[0])
    print("Pelaajam hp: "+str(hp))
    if hp <= 0:
        #Pelaaja kuolee
        print("kuollu")

            
    return


def taistelu(vihujenMaara):
    print("Huoneessa on 3 goblinia")
    lista = []
    vihutElossa = True #kun kaikki vihut on kuollu, niin false ja looppi loppuu
    
    while(vihutElossa == True):
        vihuja = mihinIsketaan(vihuElossa)    
        #Pelaajan vuoro
        vihuId = int(input("Mihin vihuun haluat iskeä ("+vihuja+")"))
        isku = int(input("Paljonko isket?"))
        pelaajaIske(isku, vihuId)
        print(vihuElossa)
        print("vihuId: "+str(vihuId))
        time.sleep(1)                   #odota 1 sekunti
        for i in range(0,vihujenMaara): #Jokainen vihu iskee vuorollaan, tutkitaan jokainen yksi kerralaan läpi että ovatko ne elossa
            time.sleep(1)
            dmg = random.randint(4,13)  #random damagee 
            if(vihuElossa[i]==True):            
                vihuIske(dmg, i)
            else:
                print("                      Vihu nro."+str(i+1)+" on kuollu")
        if any(vihuElossa)==False:  #jos kaikki vihut kuollu niin lopetetaan looppi
            print("vihut kuollut")
            vihutElossa = False


def mihinIsketaan(lista):  #vaihtoehdot vihollisista, esim. (1,2,3,4) 
    vaihtoEhdot = "";      #alkuun tyhjä
    for i in range(0, len(lista)):        
                if(i == len(lista)-1):     #jos ollaan listan vikassa kohdassa
                    if(lista[i]==True):
                        vaihtoEhdot = vaihtoEhdot+str(i+1)   #jätetään pilkku laittamatta
                    else:
                        vaihtoEhdot = vaihtoEhdot[:-1]  #Otetaan viimeinen pilkku pois jos vika vihu listassa on jo kuollut
                else:
                    if(lista[i]==True):
                          vaihtoEhdot = vaihtoEhdot+str(i+1)+","  #laitetaan pilkku perään niin saadaan (1,2,3,...)
    print(vaihtoEhdot)
    return vaihtoEhdot
# -- Pääohjelma alkaa --

# avataan yhteys tietokantaan
db = mysql.connector.connect(
    host = "localhost",
    user = "dbuser",
    passwd = "dbpass",
    db = "roolipeli",
    buffered = True)
print("Tietokantayhteys on avattu")

taistelu(3)

# tulostetaan vihollistyyppien nimet
# TODO

# lisätään uusi vihollistyyppi kantaan
# TODO

# tulostetaan uudelleen vihollistyyppien nimet
# TODO

# tulostetaan vihollisten lkm
# TODO

# tehdään tietokannan muutokset pysyviksi.
#db.commit()
# TODO

# suljetaan tietokantayhteys
db.close()
print("Tietokantayhteys on suljettu")
