import mysql.connector
import time
import random

pelaajaElossa = True;
peliLapaisty = False;  #Kun peli vedetty läpi, niin true
originalData = []
ogEnemy = []
ogItem = []
ase = ""
lock1 = True

def Stats():
    i = 0
    x = 1
    Str = 1
    Cha = 1
    Int = 1
    mag = 0
    print("You can now distribute your stats to Strength, Charisma or Intellect, your stats start at 1 and go up to 3.")
    print("You have 3 skill points to distribute.")
    while x == 1:
        SI = input("Which stat will you raise, Str, Cha or Int?: ").lower()
        if SI == "str":
            if Str == 3:
                print("Your Strength is maxed out")
            if Str < 3:
                Str = Str+1
                i = i+1
                print(Str, Cha, Int)
        elif SI == "cha":
            if Cha == 3:
                print("Your Charisma is maxed out")
            if Cha < 3:
                Cha = Cha+1
                i = i+1
                print(Str, Cha, Int)
        elif SI == "int":
            if Int == 3:
                print("Your Intellect is maxed out")
            if Int < 3:
                Int = Int+1
                i = i+1
                mag = mag+1
                print(Str, Cha, Int, mag)
                
        if i==3:
            print("Str "+str(Str)+" Cha "+str(Cha)+" Int "+str(Int))
            Ask = input("Do you want these to be your stats yes/no?: ").lower()
            if Ask == "yes":
                x = 0
            if Ask == "no":
                i = 0
                Str = 1
                Cha = 1
                Int = 1
                mag = 0
                x = 1
            
            
    createPelaajaStats(str(100), str(Str), str(Int), str(Cha), str(mag))
    return

def getOriginalDataPlayer():
    lista = []
    cur = db.cursor()
    sql  = "SELECT * FROM PLAYER;"
    cur.execute(sql)
    result = cur.fetchall()
    for row in result:
        for i in range (0,9):            
             lista.append(row[i])
    return lista

def getOriginalDataEnemy():

    pituus = 5
    korkeus = 5
    lista = [[0 for x in range(pituus)] for y in range(korkeus)]
    lista2 = []
    cur = db.cursor()
    sql  = "SELECT * FROM ENEMY;"
    cur.execute(sql)
    result = cur.fetchall()
    for row in result:
        lista2.append(row)
    for i in range(0,korkeus):
        for j in range(0,pituus):
            lista[i][j] = lista2[i][j]
    return lista

def getOriginalDataItem():

    pituus = 6
    korkeus = 10
    lista = [[0 for x in range(pituus)] for y in range(korkeus)]
    lista2 = []
    cur = db.cursor()
    sql  = "SELECT * FROM ITEM;"
    cur.execute(sql)
    result = cur.fetchall()
    for row in result:
        lista2.append(row)
    for i in range(0,korkeus):  
        for j in range(0,pituus):
            if str(lista2[i][j]) == "None":  #Null vaihtaminen
                lista[i][j] = "NULL"  
            else:
                lista[i][j] = lista2[i][j] 
    return lista


def resetAll():
    cur = db.cursor()

    #pelaajan resettaus
    global originalData    
    p = originalData
    print(p)
    sql = "UPDATE player SET name = '"+p[0]+"', pid = "+str(p[1])+", money = "+str(p[2])+",tileId = "+str(p[3])+", hp = "+str(p[4])+",attack = "+str(p[5])+", intellect = "+str(p[6])+",charisma= "+str(p[7])+",magicid = 0;"
    print(sql)
    cur.execute(sql)

    #vihun resettaus
    global ogEnemy
    lista2 = ogEnemy
    for i in range(0, 5): #ENEMY ID:n määrä
        text1 = "UPDATE enemy SET EID = "+str(lista2[i][0])+", SHP = "+str(lista2[i][1])+" , CH = "+str(lista2[i][2])+" , ETID = "+str(lista2[i][3])+", TileID = "+str(lista2[i][4])+" WHERE EID = "+str(i+1)+";"
        print(text1)
        cur.execute(text1)

    #itemin resettaus
    global ogItem
    lista2 = ogItem
    for i in range(1,10):
        text2 = "UPDATE item SET IID = "+str(lista2[i][0])+", ITID = "+str(lista2[i][1])+" , PID = "+str(lista2[i][2])+" , NPCID = "+str(lista2[i][3])+", TileID = "+str(lista2[i][4])+" , Description = '"+str(lista2[i][5])+"' WHERE IID = "+str(i+1)+";"
        print(text2)
        cur.execute(text2)
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

def gameOver():
    time.sleep(1)
    print("You died.")
    x = input("Retry  y/n?")
    if x == "y":
        resetAll()
        global pelaajaElossa
        pelaajaElossa = True
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("THE GAME IS RESTARTING...")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        time.sleep(3)
        pelaa()
    else:
        print("Game really over.")
    return










def pelaa():
    global originalData
    global ogEnemy
    global ogItem
    originalData = getOriginalDataPlayer()
    ogEnemy = getOriginalDataEnemy()
    ogItem = getOriginalDataItem()

    #GAME OVERIN JÄLKEEN RESETETAAN MÄMÄ
    global ase
    global pelaajaElossa
    global vihuElossa
    global vihuElossa4
    global vihuElossa5
    global lock1  #1 huoneen lukko
    vihuElossa = [True, True, True] #id:n mukaan järjestykseen vihut, jos false niin vihu on kuollut
    vihuElossa4 = True    #4 huoneen vihu
    vihuElossa5 = True
    pelaajaElossa = True
    ase = ""
    lock1 = True
    
    pelaaja = getPelaaja()      #pelaaja = pelaaja()  , pelaajan tiedot listana
    for i in range(0,5): #tyhjiä rivejä
        print("")
    print("You wake up in strange dungeon with no memories")
    print("Find your way out while you can!")
    print("")
    print("")
    Name()
    Stats()
    while pelaajaElossa==True and peliLapaisty==False:
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
                
                eiTaisteltavaa = True #Booleani ettei there is nothing to fight against tule useampaan kertaan, laitettava ennen looppia ettei resettaa loopin sisällä
                for action in availableActions:
                   print("   -"+action)
                print("")
                print("Hotkeys: 'Move [n,s,e,w]', Examine [item name], Pick [item name], Use [item name], Fight, Inventory, Talk [name]")
                print("")
                action_input = input("Action?").lower()

                
                if(action_input == "fight"):
                        print("")
                        print("")
                        for i in range(0,len(availableActions)):
                            if (availableActions[i]=="Fight" and i != len(availableActions)): #Katsotaan voiko huoneessa taistella ja ettei i ole viimeinen listassa
                                if eiTaisteltavaa==True:
                                    nykyinenHuone.taistele()
                            elif (availableActions[i]=="Fight"): 
                                if eiTaisteltavaa==True:
                                    nykyinenHuone.taistele()
                            else:
                                if  eiTaisteltavaa==True:
                                        if i == len(availableActions):  #Jos ei viimeisen mennessä ole taistelua listassa niin
                                            print("There is nothing to fight against")
                                            eiTaisteltavaa = False
                        ta = "Fight"
                        if ta in availableActions:
                                print("")
                        else:
                                print("There is nothing to fight against")
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
                            if action_input =="use key":
                                if(pelaajanHuoneID==1):
                                    print("You succesfully opened the door!")
                                    time.sleep(1)
                                    global lock1
                                    lock1 = False
                                else:
                                    print("You cant wear a key")
                                    time.sleep(1)
                            elif action_input =="use bag of coins":
                                print("Bag of coins won't suit you")
                                time.sleep(1)
                            else:
                                print("")
                                print("You are dressing up "+pelaajanTavarat[i])
                                time.sleep(1)
                                pueItem(pelaajanTavarat[i])
                for i in range(0, len(pelaajanTavarat)):  #tavaran käyttäminen
                        if(action_input == "drop "+str(pelaajanTavarat[i].lower())):
                            print("")
                            print("You are dropping "+pelaajanTavarat[i])
                            time.sleep(1)
                            riisuItem(pelaajanTavarat[i])
                
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
                        
                if action_input == "talk shopkeeper":      
                       if pelaajanHuoneID == 5: #KAUPPA                   
                               kauppa()
                    #for i in range(0,
                
                    #for i in range(0, len(availableActions)):    #Jos komentoa ei voi suorittaa
                          #             if(action_input != availableActions[i]):  #TÄMÄ SE OIKEA TAPA!!
                         #                 vaarinValinnat[i] = False
                       # if any(vaarinValinnat) == False:
                        #    print("")
                         #   print("You can't do that")
                #GAME OVER
                global pelaajaElossa
                if pelaajaElossa == False:
                    gameOver()
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
    itemId = 0
    cur = db.cursor()
    sql = "SELECT iid FROM item, itemtype WHERE item.itid = itemtype.ITID AND itemtype.Name = '"+str(itemNimi)+"';"
    cur.execute(sql)
    result = cur.fetchall()
    for row in result:                  #asetetaan itemin nimi id:n mukaan alla olevaan kyselyyn jossa kysytään otetaanko esim kirja haltuun
            itemId = str(row[0])
    
    #Kysytään otetaanko kyseinen esine haltuun
    ke = input("Take "+itemNimi+" (y/n)?").lower()
    if(ke=="y"):
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
    return lista

def useItem(nimi):
    
    return
    

def pueItem(nimi):  #pukee varusteen tai aseen pelaajalle
    cur = db.cursor()
    sql = "SELECT Attack, defense, Intellect, Hp, Special From itemtype Where name = '"+nimi+"';"
    cur.execute(sql)
    result = cur.fetchall()

    charisma = "1"
    stringList = [i[j] for i in result for j in range(len(i))] #tuple intiksi
    print("New Stats: "+str(stringList))
    attack = str(stringList[0])
    defense = str(stringList[1])
    intellect = str(stringList[2])
    hp = str(stringList[3])
    setPelaajaStats(hp, attack, intellect, charisma)
    p = getPelaaja()
    global ase
    ase = nimi
    return stringList

def riisuItem(nimi):
    ke = input("Drop "+nimi+" (y/n)?").lower()
    if(ke=="y"):
            cur = db.cursor()
            iid = 0
            sql3 = "select item.iid from itemtype, item where itemtype.ITID = item.ITID and name = '"+nimi+"';"
            cur.execute(sql3)
            result = cur.fetchall()
            for row in result:
                iid = row[0]
            lista = pelaajanItemit()
            for i in range(0,len(lista)):
                if lista[i] == nimi:
                    sql2 = "UPDATE item SET pid = NULL where iid = "+str(iid)+";"
                    global ase
                    if ase==nimi:  #tarkastetaan että pelaajalla on tämä päällä                   
                            sql = "SELECT Attack, defense, Intellect, Hp, Special From itemtype Where name = '"+nimi+"';"
                            cur.execute(sql)
                            result = cur.fetchall()

                            stringList = [i[j] for i in result for j in range(len(i))] #tuple stringiksi
                            print("New Stats: "+str(stringList))
                            attack = int(stringList[0])
                            defense = int(stringList[1])
                            intellect = int(stringList[2])
                            hp = int(stringList[3])
                            charisma = "1"

                            newHp = str(0 - hp)
                            newAttack = str(0-attack)
                            newDefense = str(0-defense)
                            newIntellect = str(0-intellect)
    
                            setPelaajaStats(newHp, newAttack, newIntellect, charisma)
                            p = getPelaaja()  #tulostaa uudet statsit
                            cur.execute(sql2)
                    else:
                            cur.execute(sql2)
                        
    return 
########################################################################################################################################         LIIKKUMINEN

def liiku(tile):  #liikutetaan pelaaja x,y koordniaatteihin
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

def createPelaajaStats(hp, attack, intellect, charisma, MagicID):
    cur = db.cursor()
    sql = "Update player Set hp = hp +"+hp+", attack = attack *"+attack+", intellect = intellect *"+intellect+", charisma = charisma*"+charisma+", MagicID = MagicID +"+MagicID+";"
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
        elossa = checkAlive()
        if elossa == True:
            print("|-----north-----|")
            print("|               |")
            print("|               |")
            print("|    you        |")
            print("|               |")
            print("|   GOBLINS     |")
            print("|               |")
            print("------south-----|")
        else:
            print("|-----north-----|")
            print("|               |")
            print("|               |")
            print("|    you        |")
            print("|               |")
            print("|               |")
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
        #print("Item description in this room: "+str(tavaraLista))
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
        
        toiminnot = ["Move", "Fight"]
        if elossa==False:
            toiminnot.remove("Fight")
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

def checkAliveYksi(huoneId):
    elossa = True
    booleani = True
    cur = db.cursor()
    sql = "select shp from enemy where tileid = "+str(huoneId)+";"
    cur.execute(sql)
    result = cur.fetchall()
    intList = [i[j] for i in result for j in range(len(i))] #tuple intiksi
    if intList[0] <= 0:
        elossa = False
    sqlCH = "SELECT CH FROM enemy WHERE TileID = "+str(huoneId)+";"
    cur.execute(sqlCH)
    result = cur.fetchall()
    for row in result:
            CH = row[0] # Ehkä väärin, vaatii testausta
    if CH == 0:
        elossa = False
    return elossa

def checkAlive():  #usea vihu
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
            
        sqlCH = "SELECT CH FROM enemy WHERE TileID = 2;"
        cur.execute(sqlCH)
        result = cur.fetchall()
        for row in result:
            CH = row[0]
            if CH == 0:
                row = 0
        intList = [CH[j] for CH in result for j in range(len(CH))] #tuple intiksi
        for CH in range(0,len(result)):
            if intList[CH] == 0:
                booleanLista[CH] = False

        if any(booleanLista)==False: 
            elossa = False
        
        return elossa
    
class AloitusHuone():

    otettuBool = False

    def kartta(self):
        print("|---------------|")
        print("|    gear       |")
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
            print("In gear, there is a sword, spellbook and shield...")
        elif string == "Door":
            print("Doors are pointing to south and east...")                
        return st
        
    
    def tavarat(self):  #Mitä tavaroita huoneessa on
        tavaraLista = []
        tavaraOtettu = False #jos pelaaja ottaa yhden tavaran, kaikki katoaa
        cur = db.cursor()
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
            print("Items in this room: "+str(tavaraLista))
            print("You can only choose one of them...")
        else:
            self.otettuBool = True
            text = "Dark room with two doors"
            sql3 = "UPDATE tile SET description = '"+text+"' WHERE tileID = 1";
            cur.execute(sql3)
            print("Nothing here anymore.")
        return tavaraLista
                                   
    def available_actions(self):
        toiminnot = ["Move"]
        return toiminnot

    def liikuN(self):
        print("You cannot move there.")
    def liikuS(self):
        global lock1
        if lock1==True:
            print("")
            print("Door is locked")
            time.sleep(1)
        else:
            liiku(2)
    def liikuE(self):
        liiku(3)
    def liikuW(self):
        print("You cannot move there.")
                
class VarusteHuone():

    def kartta(self):
        print("|----|----------|")
        print("| broken tile   |")
        print("|               |")
        print("west    you    hole")
        print("                |")
        print("|               |")
        print("|               |")
        print("------south-----|")

    def tutkittavaa(self):
        lista = ["Hole", "Broken Tile"]
        return lista
    def tulos(self, string):
        st = ""
        if string == "Hole":
            print("I sense there is something evil behind this wall.")
        elif string == "Broken Tile":
            print("Here's something...")
            time.sleep(1)
            print("")
            print("")
            print("")
            print("Oh, a key!")
            keraaItem("key")
        return st

    def tavarat(self):  #Mitä tavaroita huoneessa on
        tavaraLista = []
        cur = db.cursor()
        sql = "SELECT name FROM itemtype, item WHERE itemtype.ITID = item.ITID AND item.TileID = 3;"
        cur.execute(sql)
        result = cur.fetchall()
        for row in result:
            tavaraLista.extend(row)
      #  print("Items in this room: "+str(tavaraLista))
        return tavaraLista
 
    def available_actions(self):
        toiminnot = ["Move"]
        return toiminnot

    def liikuN(self):
        print("You cannot move there.")
    def liikuS(self):
                liiku(4)
    def liikuE(self):
        print("There is a hole on the eastern wall...")
        kuiskaus = input ("Maybe you should try whispering a keyword to the other side? This works in movies sometimes:")
        if kuiskaus == "1337ES":
            print ("The wall shakes violently and as it erupts, a pathway opens up before you.")
            liiku(7)
    def liikuW(self):
        liiku(1)

class strange():  #ID 9, BOSS HUONE
    
    def taistele(self):
        global vihuElossa5
        if vihuElossa5 == True:
            taisteluYksi(5, 7 ,9 ) #vihu id 4, , huoneId 4
        else:
            print("Corpse of the MONSTER BOSS is laying on floor.")
        return

    def kartta(self):
        print("|-----north-----|")
        print("|               |")
        print("|    Living     |")
        print("|    Armor      |")
        print("|               |")
        print("|    you        |")
        print("|  STAIRWAYS    |")
        print("----------------|")

    def tutkittavaa(self):
        lista = ["Monster"]
        return lista
    def tulos(self, string):
        st = ""
        if string == "Monster":
            print("This is a super monster, beaware!")
        return st

    def tavarat(self):  #Mitä tavaroita huoneessa on
        tavaraLista = []
        cur = db.cursor()
        sql = "SELECT name From itemtype where itid = (select itid From item Where tileId = 7);" #antaa esineen nimen joka on kyseisessä tilessä
        cur.execute(sql)
        result = cur.fetchall()
        for row in result:
            tavaraLista.extend(row)
      #  print("Items: "+str(tavaraLista))
        return tavaraLista
     
    def available_actions(self):
        elossa = checkAliveYksi(9)
        
        toiminnot = ["Move", "Fight"]
        if elossa==False:
                toiminnot.remove("Fight")
        return toiminnot

    def liikuN(self):
        elossa = checkAliveYksi(9)
        if elossa==True:
             print("")
             print("")
             print("")
             print("")
             print("The monster is blocking your way.")
             time.sleep(1)
        else:
            time.sleep(1)
            print("")
            print("")
            print("")
            print("Light?")
            print("")
            print("")
            print("")
            time.sleep(3)
            print("")
            print("")
            print("")
            print("")
            print("Walking....")
            print("")
            print("")
            print("")
            print("")
            time.sleep(3)
            print("")
            print("")
            print("")
            print("")
            print("Congratulations you find the way out of dungeon!!")
            time.sleep(3)
            global peliLapaisty
            peliLapaisty = True
    def liikuS(self):
        liiku(7)
    def liikuE(self):
        print("You cannot move there.")
    def liikuW(self):
        print("You cannot move there.")

class warpZone():
 
    def available_actions(self):
        toiminnot = ["Move"]
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
      #  print("Items: "+str(tavaraLista))
        return tavaraLista
 
    def available_actions(self):
        toiminnot = ["Move"]
        return toiminnot

    def liikuN(self):
        liiku(9)
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
        print("west    ---BRIDGE--- east")
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
            print("Bridge, it looks like it will broke any second. I need to make sure I don't have any extra weight along me...")
        return st

    def tavarat(self):  #Mitä tavaroita huoneessa on
        tavaraLista = []
        cur = db.cursor()
        sql = "SELECT name From itemtype where itid = (select itid From item Where tileId = 6);" #antaa esineen nimen joka on kyseisessä tilessä
        cur.execute(sql)
        result = cur.fetchall()
        for row in result:
            tavaraLista.extend(row)
       # print("AItems in this room: "+str(tavaraLista))
        return tavaraLista
 
    def available_actions(self):
        toiminnot = ["Move"]
        return toiminnot

    def liikuN(self):
        print("You cannot move there.")
    def liikuS(self):
        print("You cannot move there.")
    def liikuE(self):
        putoa = koysi()
        if putoa == False:
            liiku(7)
    def liikuW(self):
        putoa = koysi()
        if putoa == False:
            liiku(2)
        
def koysi():
        putoaa = False
        print("You walk through bridge")
        time.sleep(1)
        print("Shaking...")
        time.sleep(1)
        p = getPelaajaPaino()
        if   p < 50:            
            print("You succesfully moved through bridge!")
            time.sleep(1)
        elif p > 50:
            putoaa = True
            time.sleep(1)
            print("SHAKING!!!")
            time.sleep(1)
            print("BRIDGE BROKED! YOU ARE FALLING IN DEEPS!!")   
            global pelaajaElossa
            pelaajaElossa = False
        return putoaa

def getPelaajaPaino():
    p = 40
    itemit = pelaajanItemit()
    if len(itemit)>1:
        p = 100
    return p

class Treasury(): #id 4

    def kartta(self):
        elossa = checkAliveYksi(4)  #jos chimeraa ei olla tapettu
        if elossa == True:
            print("|-----north-----|")
            print("|               |")
            print("|      you      |")
            print("|               |")
            print("|    Chimera    |")
            print("|            east")
            print("|               |")
            print("----------------|")
        else:
            print("|-----north-----|")
            print("|               |")
            print("|      you      |")
            print("|               |")
            print("|               |")
            print("|            east")
            print("|               |")
            print("----------------|")

    def taistele(self):
        global vihuElossa4
        if  vihuElossa4 == True:
            taisteluYksi(4, 3,4 ) #vihu id 4, , huoneId 4
        else:
            print("Corpse of the chimera is laying on floor.")

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
      #  print("Items: "+str(tavaraLista))
        return tavaraLista

    vihujenMaara = 1
     
    def available_actions(self):
        elossa = checkAliveYksi(4)
        
        toiminnot = ["Move", "Fight"]
        if elossa==False:
                toiminnot.remove("Fight")
        return toiminnot

    def liikuN(self):
            liiku(3)
    def liikuS(self):
        print("You cannot move there.")
    def liikuE(self):
        elossa = checkAliveYksi(4)
        if elossa == False:
            cur = db.cursor()
            text = "The corpse of chimera is laying on floor. There is still door towards east"
            sql3 = "UPDATE tile SET description = '"+text+"' WHERE tileID = 4";  #Päivitetään huoneen info teksti kun chimera on tapettu
            cur.execute(sql3)
            liiku(5)
        else:
            print("The chimera is blocking your way to door")
    def liikuW(self):
        print("You cannot move there.")
        
class shop(): #id 5

    def kartta(self):
        print("|---------------|")
        print("|   painting    |")
        print("|               |")
        print("west    you     |")
        print("                |")
        print("|    shopkeeper |")
        print("|               |")
        print("----------------|")

    def tutkittavaa(self):
        lista = ["Shopkeeper", "Painting"]
        return lista
    def tulos(self, string):
        st = ""
        if string == "Shopkeeper":
            print("This guy wants money")
        if string == "Painting":
            print("|---------------|")
            print("|12345678ABYPEFG|")
            print("|13345678ABCDEFG|")
            print("|12345678ABCDEFG|")
            print("|12375678ABGMEFG|")
            print("|1234E678ABCDFTG|")
            print("|12345S78ABCDEFG|")
            print("|---------------|")
        return st

    def tavarat(self):  #Mitä tavaroita huoneessa on
        tavaraLista = []
        cur = db.cursor()
        sql = "SELECT name From itemtype where itid = (select itid From item Where tileId = 5);" #antaa esineen nimen joka on kyseisessä tilessä
        cur.execute(sql)
        result = cur.fetchall()
        for row in result:
            tavaraLista.extend(row)
      #  print("Items in this room: "+str(tavaraLista))
        return tavaraLista
    
 
    def available_actions(self):
        toiminnot = ["Move"]
        return toiminnot

    def liikuN(self):
        print("You cannot move there.")
    def liikuS(self):
        print("You cannot move there.")
    def liikuE(self):
        print("You cannot move there.")
    def liikuW(self):
        liiku(4)

###########################################################################                                 KAUPPA

def kauppa():
    time.sleep(1)
    print("")
    print("")
    print("Hello there. I've some goods if you need, just check them out")
    print("")
    print("You have "+str(getPelaajaRaha())+" gold.")
    print("Buy stuff or ask about that strange painting on wall")
    x = input("Buy/Ask/Exit: ").lower()
    if x == "buy":
        lista = kaupanItemit()
        hinnasto = ["20", "30", "10"]
        for i in range(0,3):
            print(lista[i]+" costs "+hinnasto[i])
        x = input("Buy [itemname] or exit: ").lower()
        for i in range(0,3):
                  if x == "buy "+lista[i].lower():
                      print(hinnasto[i])
                      varaa = katsoOnkoVaraa(int(hinnasto[i]))
                      if varaa == True:
                          keraaItem(lista[i])
                          print("Thanks!")
    elif x =="ask":
        print("")
        print("")
        print("Shopkeeper: That's my dearest treasure. Stay away from it, it's not for sold!")
        time.sleep(1)
        print("")
        print("")
        print(" (1.) Okay no problem, just wanted to ask")
        print(" (2.) You have any idea how to out of this place?")
        vastaus = True
        while vastaus==True:
            x = input("Your option (1/2): ")
            if x=="1":
                print("")
                print("")
                print("I have other stuff thought if you need")
                time.sleep(1)
                vastaus=False
            elif x=="2":
                print("")
                print("")
                print("Actually I have, but you know, nothing is free...")
                time.sleep(1)
                vastaus=False
        if x=="2":
            vastaus = True
            vastaus2 = True
            while vastaus==True:
                print("(1.)Give money for him")
                print("(2.)Fuck this jew")
                x = input("Your option (1/2): ")
                if x=="1":
                    print("")
                    print("")
                    x = input("How many gold?")
                    while vastaus2 == True:
                        rahoja = []
                        for i in range(0,100):
                            rahoja.append(str(i))
                        if x =="0":
                            print("Shopkeeper: MORE!")
                            vastaus2 = False
                        for i in range(10,19):
                            if x == str(i):
                                varaa = katsoOnkoVaraa(i)
                                if varaa == True:
                                    print("Shopkeeper: There is a secret path somewhere...")
                            vastaus2 = False
                        for i in range(20,100):
                             if x == str(i):
                                varaa = katsoOnkoVaraa(i)
                                if varaa == True:
                                     print("Tell the secret words in that painting to the hole and the wall will open.")
                             vastaus2 = False
                    time.sleep(2)
                    vastaus=False
                elif x=="2":
                    print("")
                    print("")
                    print("Well hope you get out of here someday")
                    time.sleep(1)
                    vastaus=False
    
    else:
        time.sleep(1)
        print("")
        print("")
        print("I'm fine thanks")

def katsoOnkoVaraa(hinta):
    cur = db.cursor()
    onVaraa = False
    raha = getPelaajaRaha()            
    if hinta>raha:
         time.sleep(1)
         print("")
         print("")
         print("Shopkeeper: Not enough, get fuck out")
    else:
        time.sleep(1)
        print("")
        print("")
        print("Shopkeeper: You are welcome!")
        raha = raha-hinta
        print("You have "+str(raha)+" gold left")
        sql2 = "UPDATE player SET money = "+str(raha)+";"
        cur.execute(sql2)
        onVaraa = True
    return onVaraa

def getPelaajaRaha():
    raha = 0
    cur = db.cursor()
    sql = "SELECT money FROM player"
    cur.execute(sql)
    result = cur.fetchall()
    for row in result:
        raha = row[0]
    return raha

def setPelaajaRaha(raha):
    cur = db.cursor()
    sql = "UPDATE player SET money = money + "+str(raha)+";"
    cur.execute(sql)
    return
                 
def kaupanItemit():

    cur = db.cursor()
    sql = "SELECT name FROM item, itemtype where item.ITID = itemtype.ITID and item.NPCID = 1;"
    cur.execute(sql)
    result = cur.fetchall()
    itemList = [i[j] for i in result for j in range(len(i))] #tuple stringiksi
    return itemList
#########################################################################COMBAT
vihuElossa = [True, True, True] #id:n mukaan järjestykseen vihut, jos false niin vihu on kuollut
vihuElossa4 = True    #4 huoneen vihu
vihuElossa5 = True
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
    if hp <= 0:
        #vihu kuolee
        hp = 0
        print("Enemy's current health: "+str(hp))
        print("Enemy is dead")
        if huoneId == 2:  #goblin huone
            vihuElossa[vihuId-1] = False
            print("You acquired 5 gold!")
            setPelaajaRaha(5)
        elif huoneId == 4:
             global vihuElossa4
             vihuElossa4 = False
             print("You acquired 20 gold!")
             setPelaajaRaha(20)
        elif huoneId == 9:
             global vihuElossa5
             vihuElossa5 = False
    return
def pelaajaCH(eff, vihuId, huoneId):
    CH = 0
    var = random.randint(1,11)
    if var == 1:
        print("You told the monster it's mother is dissapointed in it.")
    elif var == 2:
        print("You told the monster that your uncle works for nintendo and can ask the devs to hardcode it out of the way for you.")
    elif var == 3:
        print("You told the monster you just want to be friends.")
    elif var == 4:
        print("You told the monster you have a disability and that it wouldnt want to be caught beating up an disabled person.")
    elif var == 5:
        print("You suggest to the monster to get a drink with you instead of fighting.")
    elif var == 6:
        print("You told the monster to go fuck itself.")
    elif var == 7:
        print("You told the monster it can't keep channeling it's aggression to adventurers since it isn't healthy.")
    elif var == 8:
        print("You flip the monster off.")
    elif var == 9:
        print("You ask the monster to let you progress.")
    elif var == 10:
        print("You told the monster about the bugs in your python code")
    elif var == 11:
        print("You tell the monster that monsters aren't real.")
    if eff == 0:
        print("The  monster didn't care")
    elif eff > 0:
        print("Monster is reconsidering it's life choises.")
    cur = db.cursor()
    sqlCH = "SELECT CH FROM enemy WHERE EID = "+str(vihuId)
    cur.execute(sqlCH)
    result = cur.fetchall()
    for row in result:
            CH = row[0] # Ehkä väärin, vaatii testausta
    CH = CH-eff
    sql = "UPDATE enemy SET CH = "+str(CH)+" WHERE eid = "+str(vihuId)
    cur.execute(sql)
    sql2 = "select CH from enemy where eid = "+str(vihuId)
    cur.execute(sql2)                                  
    result = cur.fetchall()
    for row in result:
            CH = int(row[0])
    if CH == 0:
        print("The monster got confused and gave up.")
        if huoneId == 2:  #goblin huone
            print(vihuElossa)
            vihuElossa[vihuId] = False
        elif huoneId == 4:
             global vihuElossa4
             vihuElossa4 = False
        elif huoneId == 9:
             global vihuElossa5
             vihuElossa5 = False
    return

def vihuIske(vihuId):
    cur = db.cursor()
    sql2 = "SELECT name FROM enemytype, enemy WHERE enemy.etid = enemytype.etid;"
    cur.execute(sql2)
    result2 = cur.fetchall()
    stringList = [i[j] for i in result2 for j in range(len(i))] #tuple intiksi    
    
    sqlHp = "select hp from player"
    cur.execute(sqlHp)
    result = cur.fetchall()
    for row in result:
            hp = row[0]

    sqlDmg = "SELECT attack FROM enemytype, enemy WHERE enemy.etid = enemytype.etid;"
    dmg = 0
    cur.execute(sqlDmg)
    result3 = cur.fetchall()
    for row in result3:
        dmg = row[0]
    for i in range(0,len(stringList)):
        if i == vihuId-1:
            print("                               "+stringList[i]+" hits "+str(dmg)+" dmg")
    hp = hp-dmg
    sql = "UPDATE player SET hp = "+str(hp)
    cur.execute(sql)
    sql2 = "select hp from player where pid = 1"
    cur.execute(sql2)
    result = cur.fetchall()
    # Tulostetaan tuloslistan tiedot rivi kerrallaan
    for row in result:
            hp = int(row[0])
   
    if hp <= 0:
        hp = 0
        #Pelaaja kuolee
        print("You died")
        global pelaajaElossa
        pelaajaElossa = False
    else:
         print("Your current health: "+str(hp))
    return

def kaytaTaika():
    taikaNimi = getTaikaNimi()
    effect = 0
    intellect = 0
    print("Used '"+taikaNimi+"'")
    cur = db.cursor()
    sql = "SELECT Effect FROM magic WHERE name = '"+taikaNimi+"';"
    sql2 = "SELECT intellect FROM player;"
    cur.execute(sql)
    result = cur.fetchall()
    intList = [i[j] for i in result for j in range(len(i))] #tuple intiksi
    effect = intList[0]
    
    cur.execute(sql2)
    result2 = cur.fetchall()
    intList2 = [i[j] for i in result2 for j in range(len(i))] #tuple intiksi
    intellect = intList2[0]

    dmg = effect*intellect  #DMG on intellect * taian efekti
    
    return dmg


def getTaikaNimi():
    nimi = ""
    cur = db.cursor()
    sql = "SELECT magic.Name FROM magic, player WHERE magic.MagicID = player.MagicID;"
    cur.execute(sql)
    result = cur.fetchall()
    for row in result:
        nimi = row[0]
    return nimi
    
def kaytaCharisma():
    CHA = 0
    eff = 0
    cur = db.cursor()
    sql = "SELECT Charisma FROM player;"
    cur.execute(sql)
    result = cur.fetchall()
    intList = [i[j] for i in result for j in range(len(i))] #tuple intiksi
    CHA = intList[0]
    if CHA == 1:
        var = random.randint(1,4)
        if var == 2:
            eff = 1
        else:
            eff = 0
    elif CHA == 2:
        var = random.randint(1,3)
        if var == 2:
            eff = 1
        else:
            eff = 0
    elif CHA == 3:
        var = random.randint(1,2)
        if var == 2:
            eff = 1
        else:
            eff = 0
    return eff

def taisteluYksi(vihuId, escapeId, huoneId): #yksiloVihu jos vain 1

    vihutElossa = True #kun kaikki vihut on kuollu, niin false ja looppi loppuu
    global pelaajaElossa
    while(vihutElossa == True and pelaajaElossa==True):
        #Pelaajan vuoro
        looppaa = True
        tee = ""
        while looppaa==True:
                tee = input("Fight or Flee?").lower()                
                if tee =="flee":# or tee=="f":
                    looppaa=False
                elif tee=="fight" or tee=="f":
                    looppaa=False
        
        if tee=="fight": # or "f":

            Attack = 0
            isku = "SELECT attack FROM player WHERE PID =1"#int(input("Paljonko isket?"))
            cur=db.cursor()
            cur.execute(isku)
            result = cur.fetchall()
            for row in result:
                Attack = int(row[0])
            Var = random.randint(0,2)
            Attack2 = Attack-Var

            dmg = 0
            
            x = input("Hit, spell or charisma?").lower()

            if x == "hit":
                dmg = Attack2
                pelaajaIske(dmg, vihuId, 4)
                time.sleep(1)
            elif x == "spell":
                dmg = kaytaTaika()
                pelaajaIske(dmg, vihuId, 4)
                time.sleep(1)
            elif x == "charisma":
                eff = kaytaCharisma()
                pelaajaCH(eff, vihuId, 4)
                time.sleep(1)
                
                               #odota 1 sekunti
            
            if huoneId == 4:
                global vihuElossa4
                if  vihuElossa4 == True:
                    vihuIske(vihuId)
                else:
                    vihutElossa = False
                    print("The enemy is dead")
            if huoneId == 9:
                global vihuElossa5
                if  vihuElossa5 == True:
                    vihuIske(vihuId)  #BOSSEN DAMAGE TÄNNE
                else:
                    vihutElossa = False
                    print("The enemy is dead")
                   
        elif tee=="flee": # or "f":
            print("")
            print("")
            print("")
            print("You escaped!!")
            vihutElossa=False
            liiku(escapeId) #Pakene huoneesee
            
def taistelu(vihujenMaara, escapeId): #yksiloVihu jos vain 1

    vihutElossa = True #kun kaikki vihut on kuollu, niin false ja looppi loppuu
    global pelaajaElossa
    while(vihutElossa == True and pelaajaElossa==True):
        vihuja = mihinIsketaan(vihuElossa) 
        #Pelaajan vuoro
        looppaa = True
        tee = ""
        while looppaa==True:
                tee = input("Fight or Flee?").lower()
                print(tee)
                if tee =="flee": # or tee=="f":
                    looppaa=False
                if tee =="fight":# and tee=="f":
                    looppaa=False
        
        if tee=="fight":# and "f":
            vihuId = 0
            while vihuId != "1" and vihuId != "2" and vihuId != "3":
                vihuId = input("Which enemy you would like to hit ("+vihuja+")")
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

            dmg = 0
            
            x = input("Hit, spell or charisma?").lower()

            if x == "hit":
                dmg = Attack2
                pelaajaIske(dmg, vihuId, 2)
                time.sleep(1) 
            elif x == "spell":
                dmg = kaytaTaika()
                pelaajaIske(dmg, vihuId, 2)
                time.sleep(1) 
            elif x == "charisma":
                eff = kaytaCharisma()
                pelaajaCH(eff, vihuId, 2)
                time.sleep(1)
                
                
                              #odota 1 sekunti
                
            for i in range(0,vihujenMaara): #Jokainen vihu iskee vuorollaan, tutkitaan jokainen yksi kerralaan läpi että ovatko ne elossa                    
                    if(vihuElossa[i]==True):            
                        vihuIske(i)
                        time.sleep(1)
                    else:
                        print("                        Enemy nro."+str(i+1)+" is dead.")
            if any(vihuElossa)==False:  #jos kaikki vihut kuollu niin lopetetaan looppi
                    print("All enemies are dead")
                    vihutElossa = False

        elif tee=="flee": # or "f":
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
