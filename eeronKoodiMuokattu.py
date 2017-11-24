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

    location_x = getPelaajaCoordsX()
    location_y = getPelaajaCoordsY()
    
    tiles = loadTiles()        #world.load_tiles()
    pelaaja = getPelaaja()      #pelaaja = pelaaja()  , pelaajan tiedot listana
    # Linjat lataa aloitushuoneen ja näyttää tekstin
   
    pelaajanHuoneID = room()           #
   # huone = world.tile_exists(location_x, location_y)

    introText = huoneenInfo(pelaajanHuoneID)       #print(room.intro_text())
    print(introText)
   # while pelaaja.is_alive() and not pelaaja.victory:
    while pelaajaElossa==True or peliLapaisty==False:
           # huone = world.tile_exists(player.location_x, player.location_y)
           # huone.modify_pelaaja(pelaaja)
           # Katsotaan uusiksi, sillä huone on voinut muuttaa pelaajan tilannetta        
            if pelaajaElossa==True and peliLapaisty==False:
                location_x = getPelaajaCoordsX()
                location_y = getPelaajaCoordsY()
                print("X: "+str(location_x)+" y: "+str(location_y))
                introText = huoneenInfo(pelaajanHuoneID)
                pelaajanHuoneID = room()
                nykyinenHuone = mikaHuone(location_x, location_y)
                nykyinenHuone.intro_text()
                print("Choose your next action:\n")
                availableActions = nykyinenHuone.available_actions()  #Tehdään lista toiminnoista
                
                for action in availableActions:
                    print("   -"+action)
                action_input = input("Action?")
                for action in availableActions:
                    if(action_input == "taistele"):  #Action.Hotkey LISÄTTÄVÄ, TÄMÄ VAIN ESIMerkki
                        taistelu(3)
                    if(action_input == "liiku"):
                         liiku(1,2)   #LIIKKUU GOBLIN HUONEESEEN
                         print("liikuttu")
                '''VANHA VERSIO
            for action in available_actions:
                print(action)
            action_input = input('Action: ')
            for action in available_actions:
                if action_input == action.hotkey:
                    pelaaja.do_action(action, **action.kwargs)
                    break
              '''

def liiku(x,y):
    cur = db.cursor()
    sql = "UPDATE player SET xCo = "+str(x)+"; UPDATE player SET yCo = "+str(y)+";"
    db.commit()
    return

def mikaHuone(x,y):  #Katsotaan missä huoneessa ollaan ja sen mukaan tehdään action
    if(x == 1 and y == 2):
        huone = GoblinHuone()
    if(x == 1 and y == 1):
        huone = AloitusHuone()
    return huone

def getPelaajaCoordsX():
    xC = 0
    cur = db.cursor()
    sqlX = "SELECT xCo FROM player WHERE PID = 1"  #x koordinaatin haku
    cur.execute(sqlX)
    result = cur.fetchall()
    for row in result:
            xC = row[0]
    return xC

def getPelaajaCoordsY():
    yC = 0
    cur = db.cursor()
    sqlY = "SELECT yCo FROM player WHERE PID = 1"   #y koordinaatin haku
    cur.execute(sqlY)
    result = cur.fetchall()
    for row in result:
            yC = row[0]
    return yC

def loadTiles():
    tiles = []
    cur = db.cursor()
    sqlY = "SELECT xCo, yCo FROM environment"   #Tiilien lataaminen
    cur.execute(sqlY)
    result = cur.fetchall()
    for row in result:
            tiles.append(row)
    return tiles

def getPelaaja():
    pelaaja = []
    cur = db.cursor()
    sqlY = "SELECT name, pid, money, xco, yco FROM player"   #Tiilien lataaminen
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
    sql = "SELECT envtid FROM environment, player WHERE environment.XCo = player.XCo and environment.YCo = player.YCo"
    cur.execute(sql)
    result = cur.fetchall()
    for row in result:
            huone = row[0]
    print("Huoneen id: "+str(huone))
    return huone

def huoneenInfo(huone):  #STRING
    infoTeksi = ""
    cur = db.cursor()
    huoneId = huone  
    sql = "SELECT name FROM envt WHERE ENVTID = "+str(huoneId)+";"
    cur.execute(sql)
    result = cur.fetchall()
    for row in result:
            infoTeksti = row[0]
    return infoTeksti

class GoblinHuone():
    
   # def __init__(self, x, y):
    #    super().__init__(x, y, enemies.Goblins())

    
    def intro_text(self):
        
        if vihutElossa==True:          
           print("Three goblins surround you and fill you with fear!")         
        else:  
            print("The corpses of three goblins lay on the ground. I wonder if they have valuable goods in the pockets?")
    def available_actions(self):
        toiminnot = ["liiku", "taistele"]
        return toiminnot
    
class AloitusHuone():
    
    def intro_text(self):

        print("Dark room which holds nothing of value, you must choose a path.")

    def available_actions(self):
        toiminnot = ["liiku"]
        return toiminnot



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
    sqlHp = "select hp from stats"
    cur.execute(sqlHp)
    result = cur.fetchall()
    for row in result:
            hp = row[0]
    hp = hp-dmg
    sql = "UPDATE stats SET hp = "+str(hp)
    cur.execute(sql)
    sql2 = "select hp from stats where pid = 1"
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
'''
class Aloitushuone(MapTile):
    def intro_text(self):
        return """
        Dark room which holds nothing of value, you must choose a path.
        """
 
    def modify_pelaaja(self, pelaaja):
        # Huoneella ei ole funktiota pelaajalle
        pass
 
class GoblinHuone(VihuHuone1):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Goblins())
 
    def intro_text(self):
        if self.enemy.is_alive():
            return """
            Three goblins surround you and fill you with fear!
            """
        else:
            return """
            The corpses of three goblins lay on the ground. I wonder if they have valuable goods in the pockets?
            """
 
class VarusteHuone(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Velhohattu())
 
    def intro_text(self):
        return """
        You notice an object of wizardry on the ground. That could provide a significant boost to your intellect or ego.
"""
'''

    # avataan yhteys tietokantaan
db = mysql.connector.connect(
    host = "localhost",
    user = "dbuser",
    passwd = "dbpass",
    db = "dad",
    buffered = True)
print("Tietokantayhteys on avattu")

pelaa()
#taianOppiminen();
#taistelu(3, vihuElossa)


db.close()
print("Tietokantayhteys on suljettu")

