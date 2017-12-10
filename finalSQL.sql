DROP DATABASE IF EXISTS dad1;
CREATE DATABASE dad1;
USE dad1;

CREATE TABLE ItemType
(
  ITID INT NOT NULL,
  Attack INT,
  Defense INT,
  Money INT,
  Name VARCHAR(50) NOT NULL,
  Intellect INT,
  HP INT,
  Special INT,
  PRIMARY KEY (ITID)
);

CREATE TABLE EnemyType
(
  Name VARCHAR(50) NOT NULL,
  ETID INT NOT NULL,
  Attack INT NOT NULL,
  Defense INT NOT NULL,
  HP INT NOT NULL,
  Intellect INT NOT NULL,
  PRIMARY KEY (ETID)
);

CREATE TABLE Magic
(
  MagicID INT NOT NULL,
  Name VARCHAR(50) NOT NULL,
  Effect INT NOT NULL,
  PRIMARY KEY (MagicID)
);

CREATE TABLE EnemyMagic
(
  MagicID INT NOT NULL,
  ETID INT NOT NULL,
  FOREIGN KEY (MagicID) REFERENCES Magic(MagicID),
  FOREIGN KEY (ETID) REFERENCES EnemyType(ETID)
);

CREATE TABLE NPCType
(
  Name VARCHAR(50) NOT NULL,
  NPCTID INT NOT NULL,
  Attack INT NOT NULL,
  Intellect INT NOT NULL,
  Defense INT NOT NULL,
  HP INT NOT NULL,
  PRIMARY KEY (NPCTID)
);

CREATE TABLE Movement
(
MoID VARCHAR(10) NOT NULL,
Direction VARCHAR(40),
PRIMARY KEY (MoID)
);

CREATE TABLE Tile
(
  TileID INT NOT NULL,
  Name VARCHAR(30) NOT NULL,
  Description VARCHAR(1000) NOT NULL,
  PRIMARY KEY (TileID)
);

DROP TABLE IF EXISTS PASSAGE;
CREATE TABLE Passage
(
  PassID VARCHAR(10) NOT NULL,
  FromTile INT NOT NULL,
  ToTile INT NOT NULL,
  MoID VARCHAR(10) NOT NULL,
  Locked BOOLEAN,
  Locknote VARCHAR(10),
  PRIMARY KEY (PassID),
  FOREIGN KEY (FromTile) REFERENCES Tile(TileID),
  FOREIGN KEY (ToTile) REFERENCES Tile(TileID),
  FOREIGN KEY (MoID) REFERENCES Movement(MoID)
);

drop table if exists player;
CREATE TABLE Player
(
  Name VARCHAR(40) NOT NULL,
  PID INT NOT NULL,
  Money INT NOT NULL,
  TileID INT NOT NULL,
  HP INT,
  Attack INT NOT NULL,
  Intellect INT NOT NULL,
  Charisma INT NOT NULL,
  MagicID INT NOT NULL,
  PRIMARY KEY (PID),
  FOREIGN KEY (TileID) REFERENCES Tile(TileID),
  FOREIGN KEY (MagicID) REFERENCES Magic(MagicID)
  
);


CREATE TABLE Enemy
(
  EID INT NOT NULL,
  SHP INT NOT NULL,
  CH INT NOT NULL,
  ETID INT NOT NULL,
  TileID INT NOT NULL,
  PRIMARY KEY (EID),
  FOREIGN KEY (ETID) REFERENCES EnemyType(ETID),
  FOREIGN KEY (TileID) REFERENCES Tile(TileID)
);

CREATE TABLE NPC
(
  SHP INT NOT NULL,
  NPCID INT NOT NULL,
  NPCTID INT NOT NULL,
  TileID INT NOT NULL,
  PRIMARY KEY (NPCID),
  FOREIGN KEY (NPCTID) REFERENCES NPCType(NPCTID),
  FOREIGN KEY (TileID) REFERENCES Tile(TileID)
);

drop table if exists item;
CREATE TABLE Item
(
  IID INT NOT NULL,
  ITID INT NOT NULL,
  PID INT,
  NPCID INT,
  TileID INT,
  Description VARCHAR(100) NOT NULL,
  FOREIGN KEY (ITID) REFERENCES ItemType(ITID),
  FOREIGN KEY (PID) REFERENCES Player(PID),
  FOREIGN KEY (NPCID) REFERENCES NPC(NPCID),
  FOREIGN KEY (TileID) REFERENCES Tile(TileID)
);

GRANT SELECT, INSERT, UPDATE, DELETE ON dad1.* TO dbuser@localhost;

INSERT INTO Movement VALUES("N", "North");
INSERT INTO Movement VALUES("E", "East");
INSERT INTO Movement VALUES("S","South");
INSERT INTO Movement VALUES("W", "West");

INSERT INTO Tile VALUES(1, "Starting Room", "Dark room with some gear and two doors.");
INSERT INTO Tile VALUES(2, "Goblin Room", "GOBLINS!?!?!?");
INSERT INTO Tile VALUES(3, "Empty Room", "Empty as fuck yo.");
INSERT INTO Tile VALUES(4, "Treasury", "A large monster is blocking your way, but you see a treasure and a door behind it.");
INSERT INTO Tile VALUES(5, "Shop", "Room with an old man and his shop, Doesn't seem like he gets many customers.");
INSERT INTO Tile VALUES(6, "Rope Bridge", "There is a gaping chasm in the middle of the room and a dodgy looking rope bridge to the other side.");
INSERT INTO Tile VALUES(7, "Stairway", "This room seems to have nothing besides the stairway upstairs and an odd fountain.");
INSERT INTO Tile VALUES(8, "The Cells", "A lot of empty cells with some skeletons in them.");
INSERT INTO Tile VALUES(9, "???", "This room feels odd.");

INSERT INTO Passage VALUES("StartR1", 1, 2, "S", FALSE, NULL);
INSERT INTO Passage VALUES("StartR2", 1, 3, "E", FALSE, NULL);
INSERT INTO Passage VALUES("EmptyR1", 3, 4, "S", FALSE, NULL);
INSERT INTO Passage VALUES("EmptyR2", 3, 7, "E", TRUE, "Locked");
INSERT INTO Passage VALUES("EmptyR3", 3, 1, "W", FALSE, NULL);
INSERT INTO Passage VALUES("Treasury", 4, 5, "E", TRUE, "Locked");
INSERT INTO Passage VALUES("TreasuryB", 4, 3, "N", FALSE, NULL);
INSERT INTO Passage VALUES("GoblinR1", 2, 6, "S", FALSE, NULL);
INSERT INTO Passage VALUES("GoblinR2", 2, 1, "N", FALSE, NULL);
INSERT INTO Passage VALUES("Shop", 5, 4, "W", FALSE, NULL);
INSERT INTO Passage VALUES("StairR1", 7, 8, "N", FALSE, NULL);
INSERT INTO Passage VALUES("StairR2", 7, 3, "W", FALSE, NULL);
INSERT INTO Passage VALUES("StairR3", 7, 6, "S", FALSE, NULL);
INSERT INTO Passage VALUES("RopeR1", 6, 2, "W", FALSE, NULL);
INSERT INTO Passage VALUES("RopeR2", 6, 7, "E", FALSE, NULL);
INSERT INTO Passage VALUES("WarpR1", 8, 7, "S", FALSE, NULL);
INSERT INTO Passage VALUES("WarpR2", 8, 9, "W", FALSE , NULL);

INSERT INTO Itemtype VALUES(1, 1, 1, 2, "Coin", 1, 1, 0);
INSERT INTO Itemtype VALUES(2, 5, 1, 1, "Sword", 1, 1, 0);
INSERT INTO Itemtype VALUES(3, 1, 5, 1, "Shield", 1, 25, 0);
INSERT INTO Itemtype VALUES(4, 1, 1, 1, "Spellbook", 3, 1, 0);
INSERT INTO Itemtype VALUES(5, 1, 1, 1, "Key", 1, 1, 1);
INSERT INTO Itemtype VALUES(6, 1, 1, 1, "Piece of paper", 1, 1, 1);
INSERT INTO Itemtype VALUES(999, 999, 999, 1, "Annhiliator", 999, 999, 999);
INSERT INTO Itemtype VALUES(7, 7, 1, 1, "Saber", 1, 1, 0);
INSERT INTO Itemtype VALUES(8, 1, 12, 1, "Greatshield", 1, 75, 0);
INSERT INTO Itemtype VALUES(9, 1, 1, 1, "Magical Tome", 6, 1, 0);
INSERT INTO Itemtype VALUES(10, 1, 1, 1, "Gold Coin", 1, 1, 1);
INSERT INTO Itemtype VALUES(11, 1, 1, 20, "Bag of coins", 1, 1, 0);
INSERT INTO Itemtype VALUES(12, 1, 1, 1, "Thunderbolt", 1, 1, 2);
INSERT INTO Itemtype VALUES(13, 1, 1, 1, "Potion", 1, 1, 0);

INSERT INTO NPCType VALUES("Vagnald", 1, 10, 1, 3, 30);
INSERT INTO NPC VALUES(30, 1, 1, 5);

INSERT INTO EnemyType VALUES("Goblin", 1, 5, 2, 10, 1);
INSERT INTO EnemyType VALUES("Chimera", 2, 8, 4, 25, 1);
INSERT INTO EnemyType VALUES("Living Armor", 3, 20, 10, 30, 3);

INSERT INTO Enemy VALUES(1, 10, 1, 1, 2);
INSERT INTO Enemy VALUES(2, 10, 1, 1, 2);
INSERT INTO Enemy VALUES(3, 10, 1, 1, 2);
INSERT INTO Enemy VALUES(4, 25, 2, 2, 4);
INSERT INTO Enemy VALUES(5, 30, 3, 3, 9);

INSERT INTO Magic VALUES(0, "None", 0);
INSERT INTO Magic VALUES(1, "Will-O-Wisp", 2);
INSERT INTO Magic VALUES(2, "Soul Arrow", 3);
INSERT INTO EnemyMagic VALUES(1, 3);

INSERT INTO Player VALUES("Arce",1, 0, 1, 0, 1, 1, 1, 0);

INSERT INTO Item VALUES(999, 999, NULL, NULL, NULL, "Anhiliator anhiliates!");
INSERT INTO item VALUES(2,2,NULL,NULL,1,"Its a sword.");
INSERT INTO item VALUES(3,3,NULL,NULL,1,"Its a shield.");
INSERT INTO item VALUES(4,4,NULL,NULL,1,"Its a spellbook.");
INSERT INTO item VALUES(5,6,NULL,NULL,3,"Its a piece of paper with the word FEATHER written on it.");
INSERT INTO item VALUES(6,7,NULL,1,NULL,"A mighty saber.");
INSERT INTO item VALUES(7,8,NULL,1,NULL,"A shield with great defensive capabilites.");
INSERT INTO item VALUES(8,9,NULL,1,NULL,"A Book that greatly amplifies magic");
INSERT INTO item VALUES(9,10,NULL,NULL,2,"An odd looking gold coin.");
INSERT INTO item VALUES(10,11,NULL,NULL,4,"A bag of 20 coins!");
INSERT INTO ITEM VALUES(11, 5, NULL, NULL, 3, "An old key, What could I open with this?");
INSERT INTO item VALUES(12, 5, NULL, NULL, 7, "Seems to be a healing potion.");
