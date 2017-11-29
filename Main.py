import mysql.connector
import time
import random

pelaajaElossa = True;
peliLapaisty = False;  #Kun peli vedetty läpi, niin true
vihutElossa = True;
'''' HUOM!!!!!!!!!!!!!!!!!!!!!!!!!!!!
LISÄÄ NÄMÄ TIETOKANTAAN VAIN TESTAUSTA VARTEN:
INSERT INTO stats VALUES (1, 50, 20, 10, 10, 1);

INSERT INTO enemytype VALUES ("Goblin", 1, 40, 20, 50, 10);

INSERT INTO enemy VALUES (1, 40, 1, 1,1);
INSERT INTO enemy VALUES (2, 40, 1, 1,1);
INSERT INTO enemy VALUES (3, 40, 1, 1,1);

INSERT INTO player VALUES ("Hilfred", 1,20,1,1);
INSERT INTO environment VALUES (1,1,1);
INSERT INTO environment VALUES (1,2,1);
INSERT INTO envt VALUES (1,"STARTING ROOM", 4);
INSERT INTO envt VALUES (2,"GOBLIN ROOM", 4);
'''


def pelaa():

    pelaaja = getPelaaja()      #pelaaja = pelaaja()  , pelaajan tiedot listana
    for i in range(0,5): #tyhjiä rivejä
        print("")

    while pelaajaElossa==True or peliLapaisty==False:

           # Katsotaan uusiksi, sillä huone on voinut muuttaa pelaajan tilannetta        
            if pelaajaElossa==True and peliLapaisty==False:
                suunta = ["n","s","e","w"] #ilmansuunnat
                print("")
                location = getPelaajaTile()
                introText = huoneenInfo(location)

                pelaajanHuoneID = room()
                nykyinenHuone = mikaHuone(location)
                print("")

                print("Choose your next action:\n")
                availableActions = nykyinenHuone.available_actions()  #Tehdään lista toiminnoista
                
                for action in availableActions:
                    print("   -"+action)
                action_input = input("Action?")
                for action in availableActions:
                    if(action_input == "taistele"):  #Action.Hotkey LISÄTTÄVÄ, TÄMÄ VAIN ESIMerkki
                        taistelu(3)
                    for i in range(0,3):  #ilman suuntiin liikkuminen
                        if(action_input == "move "+suunta[0] and i==0):
                            nykyinenHuone.liikuN()
                        elif(action_input == "move "+suunta[1] and i==1):
                            nykyinenHuone.liikuS()
                        elif(action_input == "move "+suunta[2] and i==2):
                            nykyinenHuone.liikuE()
                        elif(action_input == "move "+suunta[3] and i==3):
                            nykyinenHuone.liikuW()


def liiku(tile):  #liikutetaan pelaaja x,y koordniaatteihin
    print("Tile: "+str(tile))
    cur = db.cursor()
    sql = "UPDATE player SET tileID = "+str(tile)+" WHERE pid = 1"
    cur.execute(sql)
    return

def mikaHuone(tile):  #Katsotaan missä huoneessa ollaan ja sen mukaan tehdään action
    if(tile == 2):
        huone = GoblinHuone()
    if(tile == 1):
        huone = AloitusHuone()
    if(tile == 3):
        huone = VarusteHuone()
    if(tile == 4):
        huone = Treasury()
    if(tile == 5):
        huone = shop()
    if (tile == 6):
        huone = ropeBridge()
    if (tile == 7):
        huone = stairWay()
    if (tile == 8):
        huone = warpZone()
    if (tile == 9):
        huone = strange()
    return huone


def getPelaajaTile():
    tileID = 0
    cur = db.cursor()
    sql = "SELECT tileID FROM player WHERE PID = 1"  #x koordinaatin haku
    cur.execute(sql)
    result = cur.fetchall()
    for row in result:
            tile = row[0]
    return tile


def getPelaaja():
    pelaaja = []
    cur = db.cursor()
    sqlY = "SELECT name, pid, money, tileID, hp, attack, intellect, charisma, magicId FROM player"   #Tiilien lataaminen
    cur.execute(sqlY)
    result = cur.fetchall()
    for row in result:
            pelaaja.append(row)
    print(pelaaja)
    return pelaaja

def room():  #Huoneen id INT
    huone = 0
    cur = db.cursor()
    #valitaan huone missä pelaaja on
    sql = "SELECT tileId FROM player"
    cur.execute(sql)
    result = cur.fetchall()
    for row in result:
            huone = row[0]
    #print("Huoneen id: "+str(huone))
    return huone

def huoneenInfo(huone):  #STRING
    infoTeksi = ""
    cur = db.cursor()
    huoneId = huone  
    sql = "SELECT description FROM tile WHERE tileID = "+str(huoneId)+";"
    cur.execute(sql)
    result = cur.fetchall()
    for row in result:
            infoTeksti = row[0]
    print(infoTeksti)
    return infoTeksti
###############################################################################HUONEEET____________________________________huoneet#########################
class GoblinHuone():
    
    def intro_text(self):
        
        if vihutElossa==True:          
           print("Three goblins surround you and fill you with fear!")         
        else:  
            print("The corpses of three goblins lay on the ground. I wonder if they have valuable goods in the pockets?")
    def available_actions(self):
        toiminnot = ["liiku", "taistele"]
        return toiminnot
    
    def liikuN(self):
        liiku(1)
    def liikuS(self):
        liiku(6)
    def liikuE(self):
        print("You cannot move there.")
    def liikuW(self):
        print("You cannot move there.")
        
class AloitusHuone():
    

    def available_actions(self):
        toiminnot = ["liiku"]
        return toiminnot

    def liikuN(self):
        print("You cannot move there.")
    def liikuS(self):
        liiku(2)
    def liikuE(self):
        liiku(3)
    def liikuW(self):
        print("You cannot move there.")
                
class VarusteHuone():
 
    def available_actions(self):
        toiminnot = ["liiku", "Kerää"]
        return toiminnot

    def liikuN(self):
        print("You cannot move there.")
    def liikuS(self):
        liiku(4)
    def liikuE(self):
        liiku(7)
    def liikuW(self):
        liiku(1)

class strange():
 
    def available_actions(self):
        toiminnot = ["liiku", "Kerää"]
        return toiminnot

    def liikuP(self):
        liiku(1)

class warpZone():
 
    def available_actions(self):
        toiminnot = ["liiku", "Kerää"]
        return toiminnot

    def liikuP(self):
        liiku(1)

class stairWay():
 
    def available_actions(self):
        toiminnot = ["liiku", "Kerää"]
        return toiminnot

    def liikuN(self):
        print("You cannot move there.")
    def liikuS(self):
        liiku(6)
    def liikuE(self):
        print("You cannot move there.")
    def liikuW(self):
        liiku(3)
class ropeBridge():
 
    def available_actions(self):
        toiminnot = ["liiku", "Kerää"]
        return toiminnot

    def liikuN(self):
        print("You cannot move there.")
    def liikuS(self):
        print("You cannot move there.")
    def liikuE(self):
        liiku(7)
    def liikuW(self):
        liiku(2)
class Treasury():
 
    def available_actions(self):
        toiminnot = ["liiku", "Kerää"]
        return toiminnot

    def liikuN(self):
        liiku(3)
    def liikuS(self):
        liiku(2)
    def liikuE(self):
        print("You cannot move there.")
    def liikuW(self):
        print("You cannot move there.")
        
class shop():
 
    def available_actions(self):
        toiminnot = ["liiku", "Kerää"]
        return toiminnot

    def liikuN(self):
        print("You cannot move there.")
    def liikuS(self):
        print("You cannot move there.")
    def liikuE(self):
        liiku(4)
    def liikuW(self):
        print("You cannot move there.")

#########################################################################COMBAT
vihuElossa = [True, True, True] #id:n mukaan järjestykseen vihut, jos false niin vihu on kuollut
pelaajaElossa = True

def pelaajaIske(dmg, vihuId):
    print("Pelaaja iskee "+str(dmg))
    cur = db.cursor()
    #Otetaan nykyinen hp
    sqlHp = "select SHP from enemy where eid = "+str(vihuId)   
    cur.execute(sqlHp)
    result = cur.fetchall()
    for row in result:
            hp = row[0]
    hp = hp-dmg
    #Muutetaan Hp
    sql = "UPDATE enemy SET SHP = "+str(hp)+" WHERE eid = "+str(vihuId)
    cur.execute(sql)
    sql2 = "select SHP from enemy where eid = "+str(vihuId)
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
    sqlHp = "select hp from player"
    cur.execute(sqlHp)
    result = cur.fetchall()
    for row in result:
            hp = row[0]
    hp = hp-dmg
    sql = "UPDATE player SET hp = "+str(hp)
    cur.execute(sql)
    sql2 = "select hp from player where pid = 1"
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

############################################################################################################################COMBAT LOPPUU


    # avataan yhteys tietokantaan
db = mysql.connector.connect(
    host = "localhost",
    user = "dbuser",
    passwd = "dbpass",
    db = "dad1",
    buffered = True)
print("Tietokantayhteys on avattu")

pelaa()

db.close()
print("Tietokantayhteys on suljettu")

