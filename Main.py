import mysql.connector
import time
import random

pelaajaElossa = True;
peliLapaisty = False;  #Kun peli vedetty läpi, niin true
#vihutElossa = True;

def Stats():
    i = 0
    x = 1
    Str = 1
    Cha = 1
    Int = 1
    print("You can now distribute your stats to Strength, Charisma or Intellect, your stats start at 1 and go up to 3.")
    print("You have 3 skill points to distribute.")
    while x == 1:
        SI = input("Which stat will you raise, Str, Cha or Int?: ")
        if SI == "Str":
            if Str == 3:
                print("Your Strength is maxed out")
            if Str < 3:
                Str = Str+1
                i = i+1
                print(Str, Int, Cha)
        elif SI == "Cha":
            if Cha == 3:
                print("Your Charisma is maxed out")
            if Cha < 3:
                Cha = Cha+1
                i = i+1
                print(Str, Int, Cha)
        elif SI == "Int":
            if Int == 3:
                print("Your Intellect is maxed out")
            if Int < 3:
                Int = Int+1
                i = i+1
                print(Str, Int, Cha)
            if Int > 1:
                mag = 2
        if i==3:
            print("Str "+str(Str)+" Cha "+str(Cha)+" Int "+str(Int))
            Ask = input("Do you want these to be your stats yes/no?: ")
            if Ask == "yes":
                x = 0
            if Ask == "no":
                i = 0
                Str = 1
                Cha = 1
                Int = 1
                x = 1
    setPelaajaStats(str(100), str(Str), str(Int), str(Cha))
    return

def setPelaajaName(Name):
    cur=db.cursor()
    sql = "Update player SET Name = '"+Name+"';"
    cur.execute(sql)
    return
    
def Name():
    x = 1
    while x == 1:
        name = input("Insert your name: ")
        Con = input("Your name is "+name+" yes/no?: ")
        if Con == "yes":
            setPelaajaName(name)
            x = 0
        elif Con == "no":
            x = 1
    return

def pelaa():

    pelaaja = getPelaaja()      #pelaaja = pelaaja()  , pelaajan tiedot listana
    for i in range(0,5): #tyhjiä rivejä
        print("")
    print("You wake up in strange dungeon with no memories")
    print("Find your way out while you can!")
    print("")
    print("")
    print("Hotkeys: 'Move [n,s,e,w]', Examine [item name], Pick [item name], Use [item name], Fight")
    Name()
    Stats()
    while pelaajaElossa==True or peliLapaisty==False:

           # Katsotaan uusiksi, sillä huone on voinut muuttaa pelaajan tilannetta        
            if pelaajaElossa==True and peliLapaisty==False:
                suunta = ["n","s","e","w"] #ilmansuunnat
                taistelu = [2, 4]  #Lisää huoneen id jossa vihollisia
                print("")
                location = getPelaajaTile()
                

                pelaajanHuoneID = room()
                nykyinenHuone = mikaHuone(location)
                
                tutkittavatAsiat = nykyinenHuone.tutkittavaa()
                pelaajanTavarat = pelaajanItemit()
                print("")
                print("INFO:")
                introText = huoneenInfo(location)
                
                
                nykyinenHuone.kartta()
                    
                if pelaajanHuoneID == 2: #Jos ollaan goblin huoneessa, niin laitetaan lisä info teksti
                    nykyinenHuone.intro_text()
                print("")
                tavaraLista = nykyinenHuone.tavarat()
                print("")

              #  print("Choose your next action:\n")
                availableActions = nykyinenHuone.available_actions()  #Tehdään lista toiminnoista

                valintaTekematta = True #tämä ruksitaan falseksi kun tehty, jotta voidaan allaoleva lista toteuttaa
                vaarinValinnat = [] #Lista huoneen toiminnoista booleanina, jotta voidaan palauttaa myöhemmin
                for i in range(0, len(availableActions)):
                    vaarinValinnat.append(True)


               # print("Pelaajan tavarat: "+str(pelaajanTavarat))

                
               # print(availableActions)
             #   print("Hotkeys: 'move [n,s,e,w]', Examine [item name], Pick [item name], Use [item name], Fight")
             #   print("Actions you can do:")
                eiTaisteltavaa = True #Booleani ettei there is nothing to fight against tule useampaan kertaan, laitettava ennen looppia ettei resettaa loopin sisällä
                for action in availableActions:
                   print("   -"+action)
                action_input = input("Action?").lower()
               # for action in availableActions:
                if(action_input == "fight"):
                        print("")
                        print("")
                        for i in range(0,len(availableActions)):
                            if (availableActions[i]=="taistele" and i != len(availableActions)): #Katsotaan voiko huoneessa taistella ja ettei i ole viimeinen listassa
                                if eiTaisteltavaa==True:
                                    nykyinenHuone.taistele()
                            elif (availableActions[i]=="taistele"): 
                                if eiTaisteltavaa==True:
                                    nykyinenHuone.taistele()
                            else:
                                if  eiTaisteltavaa==True:
                                        if i == len(availableActions):  #Jos ei viimeisen mennessä ole taistelua listassa niin
                                            print("There is nothing to fight against")
                                            eiTaisteltavaa = False
                        t = "taistele"
                        ta = "taistele"
                        if ta in availableActions:
                                print("")
                        else:
                                print("There is nothing to fight against")
                                '''
                        for t in availableActions:
                            ta = "taistele"
                            if ta in availableActions:
                                print("")
                            else:
                                print("There is nothing to fight against")
                                '''
                        valintaTekematta = False
                for i in range(0, len(tavaraLista)):  #tavaroiden tutkiminen
                    if(action_input == "examine "+tavaraLista[i].lower()):
                        print("")
                        print("Examining "+tavaraLista[i]+"....")
                        time.sleep(1)   
                        tavaranTiedot(tavaraLista[i])
                        time.sleep(1)   
                for i in range(0, len(tutkittavatAsiat)):
                    if(action_input == "examine "+tutkittavatAsiat[i].lower()):
                        print("")       
                        print("Examining "+tutkittavatAsiat[i]+"...")
                        time.sleep(1)  
                        nykyinenHuone.tulos(tutkittavatAsiat[i])
                        time.sleep(1) 

                for i in range(0, len(tavaraLista)):            #Tavaran poimininen
                        if(action_input == "pick "+str(tavaraLista[i].lower())):
                            if pelaajanHuoneID != 1:  #Jos ei olla ekassa huoneessa jossa voi ottaa vain 1:n kolmesta aseesta
                                print("")
                                print("picking "+tavaraLista[i]+"...")
                                time.sleep(1)
                                keraaItem(tavaraLista[i])  #Otetaan pelaajaalle
                            else:
                               print(str(nykyinenHuone.otettuBool)+"   <---- OTETTU BOOL")
                               if nykyinenHuone.otettuBool==False:
                                    print(""+str(i))
                                    print("Picking "+tavaraLista[i]+"...")
                                    keraaItem(tavaraLista[i])  #Otetaan pelaajaalle
                                    time.sleep(1)

                for i in range(0, len(pelaajanTavarat)):  #tavaran käyttäminen
                        if(action_input == "use "+str(pelaajanTavarat[i].lower())):
                            print("")
                            print("Player is dressing up "+pelaajanTavarat[i])
                            pueItem(pelaajanTavarat[i])
                
                for i in range(0,4):  #ilman suuntiin liikkuminen
                        if(action_input == "move "+suunta[0] and i==0):
                            print("")
                            nykyinenHuone.liikuN()
                        elif(action_input == "move "+suunta[1] and i==1):
                            print("")
                            nykyinenHuone.liikuS()
                        elif(action_input == "move "+suunta[2] and i==2):
                            print("")
                            nykyinenHuone.liikuE()
                        elif(action_input == "move "+suunta[3] and i==3):
                            print("")
                            nykyinenHuone.liikuW()
                        valintaTekematta = False
                if action_input == "inventory":
                        print("")
                        print("You have in inventory:"+str(pelaajanTavarat))

                        
                if action_input == "use Rope" and pelaajanHuoneID == 6: #Köydellä ylitys
                         nykyinenHuone.koysi()
                    
                    #for i in range(0,
                
                    #for i in range(0, len(availableActions)):    #Jos komentoa ei voi suorittaa
                          #             if(action_input != availableActions[i]):  #TÄMÄ SE OIKEA TAPA!!
                         #                 vaarinValinnat[i] = False
                       # if any(vaarinValinnat) == False:
                        #    print("")
                         #   print("You can't do that")
def tavaranTiedot(nimi):
    info = ""
    cur = db.cursor()
    sql = "SELECT description From item where itid = (select itid From itemtype Where name = '"+nimi+"');"
    cur.execute(sql)
    result = cur.fetchall()
    for row in result:
            info = row[0]
    print(info)

def keraaItem(itemNimi):  #item id, esim 1 = kirja 2 = taikahattu tms.
   # itemNimi = ""
    itemId = 0
    cur = db.cursor()
    #sqlItemNimi = "SELECT name From  itemtype WHERE itemtype.ITID = "+str(itemId)  #Itemin nimi katsotaan listasta
    sql = "SELECT iid FROM item, itemtype WHERE item.itid = itemtype.ITID AND itemtype.Name = '"+str(itemNimi)+"';"
    cur.execute(sql)
    result = cur.fetchall()
    for row in result:                  #asetetaan itemin nimi id:n mukaan alla olevaan kyselyyn jossa kysytään otetaanko esim kirja haltuun
            print("Item id: "+str(row[0]))
            itemId = str(row[0])
    
    #Kysytään otetaanko kyseinen esine haltuun
    ke = input("ota "+itemNimi+" (k/e)?")    
    if(ke=="k"):
        sql = "UPDATE item SET Pid = 1 WHERE iid = "+str(itemId) #päivitetään itemi pelaajan haltuun
        sql2 = "UPDATE item SET tileID = NULL where iid = "+str(itemId) #Otetaan item pois huoneesta
        cur.execute(sql)
        cur.execute(sql2)
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
    lista = []
    cur = db.cursor()
    sql = "SELECT name From itemtype, item WHERE itemtype.ITID = item.ITID AND item.PID = 1"
    cur.execute(sql)
    result = cur.fetchall()
    lista = [i[j] for i in result for j in range(len(i))] #tuple intiksi

    #for i in range(0,len(result)): #tehdään listasta resultin pituinen
    #   lista.append(result[i])
     #  for row in result:
     #      lista[i] = row[i]           
   # print("You have in your inventory: "+str(lista))
    return lista

def useItem(nimi):
    
    return
    

def pueItem(nimi):  #pukee varusteen tai aseen pelaajalle
    cur = db.cursor()
    sql = "SELECT Attack, defense, Intellect, Hp, Special From itemtype Where name = '"+nimi+"';"
    cur.execute(sql)
    result = cur.fetchall()

    stringList = [i[j] for i in result for j in range(len(i))] #tuple intiksi
    print("New Stats: "+str(stringList))
    attack = str(stringList[0])
    defense = str(stringList[1])
    intellect = str(stringList[2])
    hp = str(stringList[3])
    charisma = "0"
    setPelaajaStats(hp, attack, intellect, charisma)
    p = getPelaaja()
    return stringList

########################################################################################################################################         LIIKKUMINEN

def liiku(tile):  #liikutetaan pelaaja x,y koordniaatteihin
   # print("Tile: "+str(tile)) LAITA TAKAISIN TARKASTUSTA VARTEN
    cur = db.cursor()
    sql = "UPDATE player SET tileID = "+str(tile)+" WHERE pid = 1"
    cur.execute(sql)
    print("Moving...")
    time.sleep(1)
   
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

def setPelaajaName(nimi):
    cur = db.cursor()
    sql = "Update player Set name = '"+nimi+"';"
    cur.execute(sql)
    return


def setPelaajaStats(hp, attack, intellect, charisma):
    cur = db.cursor()
    sql = "Update player Set hp = hp +"+hp+", attack = attack *"+attack+", intellect = intellect *"+intellect+", charisma = charisma*"+charisma+";"
    cur.execute(sql)
    return

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

    def kartta(self):
            print("|-----north-----|")
            print("|               |")
            print("|               |")
            print("|    you        |")
            print("|               |")
            print("|   GOBLINS     |")
            print("|               |")
            print("------south-----|")
            return
    def tutkittavaa(self):
        lista = ["Goblin"]
        return lista
    def tulos(self, string):
        st = ""
        if string == "Goblin":
            print("Goblins wants to kill you, run if you can!")
        return st

    def tavarat(self):  #Mitä tavaroita huoneessa on
        tavaraLista = []
        cur = db.cursor()
        sql = "SELECT name From itemtype where itid = (select itid From item Where tileId = 2);" #antaa esineen nimen joka on kyseisessä tilessä
        cur.execute(sql)
        result = cur.fetchall()
        for row in result:
            tavaraLista.extend(row)
        print("Item description in this room: "+str(tavaraLista))
        return tavaraLista
    
    def taistele(self):
       taistelu(3, 1) #3 vihua, elossa = True
    def intro_text(self):
        elossa = checkAlive()
        if elossa==True:          
           print("Three goblins surround you and fill you with fear!")         
        else:  
            print("The corpses of three goblins lay on the ground. I wonder if they have valuable goods in the pockets?")
    def available_actions(self):
        elossa = checkAlive()
        
        toiminnot = ["liiku", "taistele"]
        if elossa==False:
            toiminnot.remove("taistele")
        return toiminnot
    
    def liikuN(self):
        liiku(1)
    def liikuS(self):
        elossa = checkAlive()        
        if elossa==False:
            liiku(6)
        else:            
            print("Kill Goblins out of your way first!")
            time.sleep(1)
    def liikuE(self):
        print("You cannot move there.")
    def liikuW(self):
        print("You cannot move there.")



def checkAlive():
        elossa = True  #Tarkastetaan onko vihuja elossa huoneessa, jos ei ole, niin poistetaan "taistele" vaihtoehto toiminnoista
        booleanLista = [True,True,True] #vihujen mukaan
        cur = db.cursor()
        sql = "select shp from enemy where tileid = 2;" #huoneen id
        cur.execute(sql)
        result = cur.fetchall()
        for row in result:
            i =row[0]
            if i <= 0:
                   row = 0         
        intList = [i[j] for i in result for j in range(len(i))] #tuple intiksi
        for i in range(0,len(result)):
            if intList[i] <= 0:
                booleanLista[i] = False

        if any(booleanLista)==False: 
            elossa = False
        return elossa
    
class AloitusHuone():

    otettuBool = False

    def kartta(self):
        print("|---------------|")
        print("|               |")
        print("|               |")
        print("|    you       east")
        print("|                ")
        print("|               |")
        print("|               |")
        print("------south-----|")
    
    def tutkittavaa(self):  #Laita asioita mitä haluat tutkia
        lista = ["Gear","Door"]
        return lista
    def tulos(self, string):
        st = ""
        if string == "Gear":
            print("In gear, there is a sword, spellbook and mushroom...")
        elif string == "Door":
            print("Doors are pointing to south and east, both are unlocked...")                
        return st
        
    
    def tavarat(self):  #Mitä tavaroita huoneessa on
        tavaraLista = []
        tavaraOtettu = False #jos pelaaja ottaa yhden tavaran, kaikki katoaa
        cur = db.cursor()
      #  sql = "SELECT name From itemtype where itid = (select itid From item Where tileId = 1);" #antaa esineen nimen joka on kyseisessä tilessä
        sql = "SELECT name FROM itemtype, item WHERE itemtype.ITID = item.ITID AND item.TileID = 1;"
        sql2 = "SELECT pid FROM itemtype, item WHERE itemtype.ITID = item.ITID AND item.TileID = 1;"
        cur.execute(sql)
        result = cur.fetchall()
        for row in result:
            tavaraLista.extend(row)
          
        cur.execute(sql2) #ITEMIN TARKASTUS
        result2 = cur.fetchall()
        lista = [i[j] for i in result2 for j in range(len(i))] #tuple intiksi
        if len(lista)<3:
            tavaraOtettu = True

        if tavaraOtettu == False:
            print("ASDItems in this room: "+str(tavaraLista))
            print("You can only choose one of them...")
        else:
            self.otettuBool = True
            text = "Dark room with two doors"
            sql3 = "UPDATE tile SET description = '"+text+"' WHERE tileID = 1";
            cur.execute(sql3)
            print("Nothing here anymore.")
        return tavaraLista
                                   
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

    def kartta(self):
        print("|---------------|")
        print("|               |")
        print("|               |")
        print("west    you    hole")
        print("                |")
        print("|               |")
        print("|               |")
        print("------south-----|")

    def tutkittavaa(self):
        lista = ["Door"]
        return lista
    def tulos(self, string):
        st = ""
        if string == "Door":
            print("Doors are unclocked!")
        return st

    def tavarat(self):  #Mitä tavaroita huoneessa on
        tavaraLista = []
        cur = db.cursor()
        #sql = "SELECT name From itemtype where itid = (select itid From item Where tileId = 3);" #antaa esineen nimen joka on kyseisessä tilessä
        sql = "SELECT name FROM itemtype, item WHERE itemtype.ITID = item.ITID AND item.TileID = 3;"
        cur.execute(sql)
        result = cur.fetchall()
        for row in result:
            tavaraLista.extend(row)
        print("Items in this room: "+str(tavaraLista))
        return tavaraLista
 
    def available_actions(self):
        toiminnot = ["liiku"]
        return toiminnot

    def liikuN(self):
        print("You cannot move there.")
    def liikuS(self):
        liiku(4)
    def liikuE(self):
        #liiku(7)
        print("There is a hole in eastern wall...")
        time.sleep(1)
    def liikuW(self):
        liiku(1)

class strange():
 
    def available_actions(self):
        toiminnot = ["liiku"]
        return toiminnot

    def liikuP(self):
        liiku(1)

class warpZone():
 
    def available_actions(self):
        toiminnot = ["liiku"]
        return toiminnot

    def liikuP(self):
        liiku(1)

class stairWay(): #id 7

    def kartta(self):
        print("|---------------|")
        print("|   STAIRWAYS   |")
        print("|               |")
        print("west    you     |")
        print("|               |")
        print("|               |")
        print("|               |")
        print("------south-----|")

    def tutkittavaa(self):
        lista = ["Stairway"]
        return lista
    def tulos(self, string):
        st = ""
        if string == "Stairway":
            print("Stairways to hell, do not enter!")
        return st

    def tavarat(self):  #Mitä tavaroita huoneessa on
        tavaraLista = []
        cur = db.cursor()
        sql = "SELECT name From itemtype where itid = (select itid From item Where tileId = 7);" #antaa esineen nimen joka on kyseisessä tilessä
        cur.execute(sql)
        result = cur.fetchall()
        for row in result:
            tavaraLista.extend(row)
        print("Items: "+str(tavaraLista))
        return tavaraLista
 
    def available_actions(self):
        toiminnot = ["liiku"]
        return toiminnot

    def liikuN(self):
        print("You cannot move there.")
    def liikuS(self):
        liiku(6)
    def liikuE(self):
        print("You cannot move there.")
    def liikuW(self):
        liiku(3)
class ropeBridge(): #id 6

    def kartta(self):
        print("|-----------------------|")
        print("|                       |")
        print("|                       |")
        print("east    ---BRIDGE---  west")
        print("|                       |")
        print("|                       |")
        print("|                       |")
        print("------------------------|")
    
    def tutkittavaa(self):
        lista = ["Bridge"]
        return lista
    def tulos(self, string):
        st = ""
        if string == "Bridge":
            print("Bridge, it looks shaky...")
        return st

    def tavarat(self):  #Mitä tavaroita huoneessa on
        tavaraLista = []
        cur = db.cursor()
        sql = "SELECT name From itemtype where itid = (select itid From item Where tileId = 6);" #antaa esineen nimen joka on kyseisessä tilessä
        cur.execute(sql)
        result = cur.fetchall()
        for row in result:
            tavaraLista.extend(row)
        print("AItems in this room: "+str(tavaraLista))
        return tavaraLista
 
    def available_actions(self):
        toiminnot = ["liiku"]
        return toiminnot

    def liikuN(self):
        print("You cannot move there.")
    def liikuS(self):
        print("You cannot move there.")
    def liikuE(self):
        koysi()
        liiku(7)
    def liikuW(self):
        koysi()
        liiku(2)
        
def koysi():
        
        print("You walk through bridge")
        time.sleep(1)
        print("Shaking...")
        time.sleep(1)
        p = 60 #getPelaajaPaino(60)
        if   p < 50:            
            ("You succesfully moved through bridge!")
            time.sleep(1)
        elif p > 50:
            time.sleep(1)
            ("SHAKING!!!")
            time.sleep(1)
            ("BRIDGE BROKED! YOU ARE FALLING IN DEEPS!!")

def getPelaajaPaino(paino):
    p = paino
    return p

class Treasury(): #id 4

    def kartta(self):
        print("|-----north-----|")
        print("|               |")
        print("|      you      |")
        print("|                ")
        print("|     MONSTER   east ")
        print("|               |")
        print("|               |")
        print("----------------|")

    def taistele(self):
        if any(vihuElossa4) == True:
            taisteluYksi(4, 3,4 ) #vihu id 4, , huoneId 4
        else:
            print("The corpse of chimera is laying on floor.")
        return
    def tutkittavaa(self):
        lista = ["Goblin"]
        return lista
    def tulos(self, string):
        st = ""
        if string == "Goblin":
            print("Goblins wants to kill you, run if you can!")
        return st

    def tavarat(self):  #Mitä tavaroita huoneessa on
        tavaraLista = []
        cur = db.cursor()
        sql = "SELECT name From itemtype where itid = (select itid From item Where tileId = 4);" #antaa esineen nimen joka on kyseisessä tilessä
        cur.execute(sql)
        result = cur.fetchall()
        for row in result:
            tavaraLista.extend(row)
        print("Items: "+str(tavaraLista))
        return tavaraLista

    vihujenMaara = 1
     
    def available_actions(self):
        toiminnot = ["liiku", "taistele"]
        return toiminnot

    def liikuN(self):
        liiku(3)
    def liikuS(self):
        print("You cannot move there.")
    def liikuE(self):
        liiku(5)
    def liikuW(self):
        print("You cannot move there.")
        
class shop(): #id 5

    def kartta(self):
        print("|---------------|")
        print("|               |")
        print("|               |")
        print("west    you     |")
        print("                |")
        print("|    shopkeeper |")
        print("|               |")
        print("----------------|")

    def tutkittavaa(self):
        lista = ["Goblin"]
        return lista
    def tulos(self, string):
        st = ""
        if string == "Goblin":
            print("Goblins wants to kill you, run if you can!")
        return st

    def tavarat(self):  #Mitä tavaroita huoneessa on
        tavaraLista = []
        cur = db.cursor()
        sql = "SELECT name From itemtype where itid = (select itid From item Where tileId = 5);" #antaa esineen nimen joka on kyseisessä tilessä
        cur.execute(sql)
        result = cur.fetchall()
        for row in result:
            tavaraLista.extend(row)
        print("AItems in this room: "+str(tavaraLista))
        return tavaraLista
    
 
    def available_actions(self):
        toiminnot = ["liiku"]
        return toiminnot

    def liikuN(self):
        print("You cannot move there.")
    def liikuS(self):
        print("You cannot move there.")
    def liikuE(self):
        print("You cannot move there.")
    def liikuW(self):
        liiku(4)
        

#########################################################################COMBAT
vihuElossa = [True, True, True] #id:n mukaan järjestykseen vihut, jos false niin vihu on kuollut
vihuElossa4 = [True]     #4 huoneen vihu
pelaajaElossa = True

def pelaajaIske(dmg, vihuId, huoneId): #usea = True on useampi vihu
    hp = 0
    print("You hit "+str(dmg))
    time.sleep(1)
    print("")
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
    print("Enemy's current health: "+str(hp))
    if hp <= 0:
        #vihu kuolee
        hp = 0
        print("Enemy is dead")
        if huoneId == 2:  #goblin huone
            vihuElossa[vihuId-1] = False
        elif huoneId == 4:
             vihuElossa4[0] = False
    return

def vihuIske(dmg, vihuId):
    print("                        Enemy nro."+str(vihuId+1)+" hits "+str(dmg))
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
    print("Your current health: "+str(hp))
    if hp <= 0:
        #Pelaaja kuolee
        print("You died")
    pelaajaElossa = False
            
    return

def kaytaTaika():

    #Mitä tapahtuu kun taikakäytetään

    return dmg

def kaytaCharisma():
    
    return

def taisteluYksi(vihuId, escapeId, huoneId): #yksiloVihu jos vain 1

    vihutElossa = True #kun kaikki vihut on kuollu, niin false ja looppi loppuu
    
    while(vihutElossa == True):
        #Pelaajan vuoro
        looppaa = True
        tee = ""
        while looppaa==True:
                tee = input("Attack or Flee?").lower()
                if tee =="Flee" or tee=="f":
                    looppaa=False
                elif tee=="fight" or tee=="a":
                    looppaa=False
        
        if tee=="fight" or "a":

            isku = random.randint(10,50) #int(input("Paljonko isket?"))
            pelaajaIske(isku, vihuId, 4)
            time.sleep(1)                   #odota 1 sekunti
            
            if huoneId == 4:    
                if  any(vihuElossa4) == True:
                    vihuIske(10, vihuId)
                else:
                    vihutElossa = False
                    print("The enemy is dead")
                   
        elif tee=="Flee" or "f":
            print("")
            print("")
            print("")
            print("You escaped!!")
            vihutElossa=False
            liiku(escapeId) #Pakene huoneesee
            
def taistelu(vihujenMaara, escapeId): #yksiloVihu jos vain 1

    vihutElossa = True #kun kaikki vihut on kuollu, niin false ja looppi loppuu
    
    while(vihutElossa == True):
        vihuja = mihinIsketaan(vihuElossa) 
        #Pelaajan vuoro
        looppaa = True
        tee = ""
        while looppaa==True:
                tee = input("fight or Flee?")
                if tee =="Flee" or tee=="f":
                    looppaa=False
                elif tee=="fight" or tee=="a":
                    looppaa=False
        
        if tee=="Fight" or "a":
            vihuId = 0
            while vihuId != "1" and vihuId != "2" and vihuId != "3":
                vihuId = input("Which enemy you would like to hit ("+vihuja+")")
                print(vihuId)
            vihuId = int(vihuId)
            #isku = random.randint(10,50) #int(input("Paljonko isket?"))
            Attack = 0
            isku = "SELECT attack FROM player WHERE PID =1"#int(input("Paljonko isket?"))
            cur=db.cursor()
            cur.execute(isku)
            result = cur.fetchall()
            for row in result:
                Attack = int(row[0])
            Var = random.randint(0,2)
            Attack2 = Attack-Var
            pelaajaIske(Attack2, vihuId, 2)
            time.sleep(1)                   #odota 1 sekunti
                
            for i in range(0,vihujenMaara): #Jokainen vihu iskee vuorollaan, tutkitaan jokainen yksi kerralaan läpi että ovatko ne elossa
                    time.sleep(1)
                    dmg = random.randint(4,13)  #random damagee 
                    if(vihuElossa[i]==True):            
                        vihuIske(dmg, i)
                    else:
                        print("                      Enemy nro."+str(i+1)+" is dead.")
            if any(vihuElossa)==False:  #jos kaikki vihut kuollu niin lopetetaan looppi
                    print("All enemies are dead")
                    vihutElossa = False
                    '''
            else:  #Vihuja on vain 1
                time.sleep(1)
                dmg = random.randint(4,13)  #random damagee
                if  vihutElossa == False:
                    vihuIske(dmg,huoneId)
                    '''
        elif tee=="Flee" or "f":
            print("")
            print("")
            print("")
            print("You escaped!!")
            vihutElossa=False
            liiku(escapeId) #Pakene huoneesee
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
   # print(vaihtoEhdot)
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
