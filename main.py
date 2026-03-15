import tkinter as tk
import math
import sqlite3
#import simpleaudio as sa


#--------------------Alustusmuuttujia-----------------
SCREEN_W=1280
SCREEN_H=720

PLAYER_X=2.5
PLAYER_Y=2.5

PLAYER_A=0
FOV=math.pi/3
RAY_WIDTH=2

GRAPHIC_ADJUST=0.03

MlemToggle=False
AllowMovement=True
AllowButtons=True
TvActive=False


EscMenuActive=False
NotificationVisible=False

RoomActive=False
RoomDrawn=False
BedroomActive=False
LivingRoomActive=False
OfficeActive=False
KitchenActive=False
StorageRoomActive=False
BathroomActive=False
FrontdoorActive=False


#pelilogiikan muuttujat
DayNum=1
NightTime=True
NotificationText=None
DialogueText=None
SomeoneAtDoor="Linus"
TalkButtonText="PUHU LINUKSELLE"
TalkingToSomeone=False


AllCharacters={
	"Linus":{"huijari":False,"dialogue_1":"Tervehdys koodari! Kuulin että olet järjestämässä Hackathonia!\nHienoa! Olen tullut varmistamaan, että kaikki lähtee hyvin käyntiin,\neikä Windows-koodareita pääse livahtamaan sisään!\nSaako tulla sisään?","dialogue_2":"Tervehdys taas! Tässä on demon loppu. Aika siirtyä\nseuraavan kurssin pariin, joten poistunkin tästä!\nKoodailun iloa!"}
	}
CharactersInside=[]

#--------------------Level mappi--------------------
MAP_W=10
MAP_H=8
MAP=[
	"##########",
	"###.#.####",
	"#........#",
	"###.###.##",
	"######...#",
	"#######..#",
	"#######.##",
	"##########"]

#--------------------- SQL TAULUKOINTI --------------------------
def CreateTablesSQL():
	conn=sqlite3.connect("Data/gamesave.db")
	cursor=conn.cursor()
	#cursor.execute("""DROP TABLE IF EXISTS savedata""")
	cursor.execute(
		"""CREATE TABLE IF NOT EXISTS savedata(
			PLAYER_X REAL,
			PLAYER_Y REAL,
			PLAYER_A REAL)"""
	)
	conn.commit()
	conn.close()

def SaveGame():
	CreateTablesSQL()
	conn=sqlite3.connect("Data/gamesave.db")
	cursor=conn.cursor()
	cursor.execute("""DELETE FROM savedata """)
	cursor.execute(
		"""INSERT INTO savedata (PLAYER_X,PLAYER_Y,PLAYER_A) VALUES (?,?,?)""",
		(PLAYER_X,PLAYER_Y,PLAYER_A)
	)
	for rivi in cursor.execute("SELECT * FROM savedata"):
		print(rivi)

	conn.commit()
	conn.close()

def LoadGame():
	global EscMenuActive,PLAYER_X,PLAYER_Y,PLAYER_A
	conn=sqlite3.connect("Data/gamesave.db")
	cursor=conn.cursor()
	cursor.execute("""SELECT * FROM savedata""")
	data=cursor.fetchone()
	PLAYER_X=data[0]
	PLAYER_Y=data[1]
	PLAYER_A=data[2]
	EscMenuActive=False

def ExitGame():
	root.quit()

#---------------Ummmm more funktions clean later---------------------
def LeaveCurrentState():
	global EscMenuActive,RoomActive,RoomDrawn,BedroomActive,TvActive,LivingRoomActive,OfficeActive,KitchenActive,StorageRoomActive,BathroomActive,FrontdoorActive,AllowMovement,PLAYER_X,PLAYER_Y,PLAYER_A
	if TvActive:
		BedroomActive=True
		RoomActive=True
		TvActive=False
		RoomDrawn=False
	elif BedroomActive:
		BedroomActive=False
		PLAYER_X=2.5
		PLAYER_Y=2.5
		PLAYER_A=0
		AllowMovement=True
	elif LivingRoomActive:
                LivingRoomActive=False
                PLAYER_X=2.8
                PLAYER_Y=3.5
                PLAYER_A=math.pi/2*3
                AllowMovement=True
                RoomActive=False
                LeaveButton.place_forget()

	elif OfficeActive:
                OfficeActive=False
                PLAYER_X=2.2
                PLAYER_Y=3.5
                PLAYER_A=math.pi/2
                AllowMovement=True
                RoomActive=False
                LeaveButton.place_forget()

	elif KitchenActive:
                KitchenActive=False
                PLAYER_X=2.2
                PLAYER_Y=5.5
                PLAYER_A=math.pi/2
                AllowMovement=True
                RoomActive=False
                LeaveButton.place_forget()

	elif StorageRoomActive:
                StorageRoomActive=False
                PLAYER_X=2.5
                PLAYER_Y=7.99
                PLAYER_A=math.pi
                AllowMovement=True
                RoomActive=False
                LeaveButton.place_forget()
	elif BathroomActive:
                BathroomActive=False
                PLAYER_X=4.5
                PLAYER_Y=7.5
                PLAYER_A=0
                AllowMovement=True
                RoomActive=False
                LeaveButton.place_forget()

	elif FrontdoorActive:
		FrontdoorActive=False
		PLAYER_X=5.8
		PLAYER_Y=7.5
		PLAYER_A=math.pi/2*3
		AllowMovement=True
		RoomActive=False
		LeaveButton.place_forget()
	if EscMenuActive:
		EscMenuActive=False

def NotifyPlayer(message,duration):
	global NotificationText
	NotificationText=GameScreen.create_text(SCREEN_W/2,SCREEN_H/2-325,text=message,fill="#ffab23",font=("Courier New",30))
	GameScreen.after(duration, lambda: GameScreen.delete(NotificationText))
def DrawDialogue(message,x,y):
	global DialogueText
	NotificationText=GameScreen.create_text(x,y,text=message,fill="#ffab23",font=("Courier New",22))
def InviteSomeoneIn():
	global CharactersInside, SomeoneAtDoor,TalkButtonText
	#TalkButtonText=f"Kutsu {SomeoneAtDoor} sisään"
	CharactersInside.append(SomeoneAtDoor)
	SomeoneAtDoor=""
	GameScreen.delete(DialogueText) #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<TEMPORARY!!!
	InviteInButton.place_forget()
def TalkToLinus():
	global DialogueText,TalkingToSomeone,TalkButtonText,RoomDrawn
	TalkingToSomeone=not TalkingToSomeone
	DrawDialogue(AllCharacters["Linus"]["dialogue_2"],SCREEN_W/2,SCREEN_H/2-250)
	TalkButtonText="ASIA SELVÄ!"
	TalkButton_Linus.config(text=TalkButtonText)
	if not TalkingToSomeone:
		#CharactersInside=[]
		#RoomDrawn=False
		ExitGame()
#-------------------------------------------Tkinter Setup-------------------------------------------------
#Luodaan root ikkuna
root=tk.Tk()
root.title("Yes, I Use Arch BTW")
root.geometry(f"{SCREEN_W}x{SCREEN_H}")

#Luodaan canvas gameplaylle root ikkunaan, ja käytetään pack asettelua
GameScreen=tk.Canvas(root,width=SCREEN_W,height=SCREEN_H,bg="#000000")
GameScreen.pack()



#------------------------------------KUVAT JA TEKSTÖÖRIT-----------------------------
mlem_img=tk.PhotoImage(file="Images/Other/cat.png")
escmenu_img=tk.PhotoImage(file="Images/Other/EscMenu.png")

bedroom_img=tk.PhotoImage(file="Images/Rooms/Bedroom.png")
living_room_img=tk.PhotoImage(file="Images/Rooms/Living_Room.png")
office_img=tk.PhotoImage(file="Images/Rooms/Office.png")
kitchen_img=tk.PhotoImage(file="Images/Rooms/Kitchen.png")
storage_room_img=tk.PhotoImage(file="Images/Rooms/Storage_Room.png")
bathroom_img=tk.PhotoImage(file="Images/Rooms/Bathroom.png")
frontdoor_img=tk.PhotoImage(file="Images/Rooms/Frontdoor.png")

news_img=tk.PhotoImage(file="Images/Tv/NewsDay1.png")
Linus1_img=tk.PhotoImage(file="Images/Visitors/Linus1.png")
Linus2_img=tk.PhotoImage(file="Images/Visitors/Linus2.png")

#-----------------AUDIO---------------------------
#Kontiovaara_sound1=sa.WaveObject.from_wave_file("KontiovaaraKautattekoHuumeita.wav") #KOKEILE MYÖHEMMIN. LINUX TO WINDOWS DEV AUDIO MENEE LIIAN MONIMUTKAISEKSI NOPEAAN PROJEKTIIN.
#Kontiovaara_play=None                                                      #IMPORT OS SYSTEM CHECK + IMPORT WINSOUND EHKÄ TOIMII WINDOWSILLE MITÄ KOULU TODENNÄK KÄYTTÄÄ
#--------------------------Draw Image Functions ------------------------
def WatchTv():
	global TvActive,AllowButtons
	TvActive=not TvActive
	WatchTvButton.place_forget()
	SleepButton.place_forget()
	LeaveButton.place_forget()

def LoadVisitors():
	global SomeoneAtDoor,visitor_img
	if SomeoneAtDoor!="":
		visitor_img=tk.PhotoImage(file=f"Images/Visitors/{SomeoneAtDoor}1.png")
	print(SomeoneAtDoor)
def BedTime():
	global NightTime,DayNum,news_img,SomeoneAtDoor
	if SomeoneAtDoor!="":
		print("Et voi koodata vielä, joku on ovella!")
		NotifyPlayer("Et voi koodata vielä, joku on ovella!",2000)
		return
	if DayNum==2 and NightTime==False and "Linus" in CharactersInside:
		NotifyPlayer("Et voi koodata, Linusilla on asiaa",2000)
		return
	else:
		print(f"Onko vanha aika yö? {NightTime}")
		NightTime=not NightTime
		print(f"Onko uusi aika yö? {NightTime}")
		print(f"Now is day {DayNum}")
		if NightTime==False:DayNum+=1
		print(f"Now is day {DayNum}")
		if DayNum==2:
			news_img=tk.PhotoImage(file="Images/Tv/NewsDay2.png")
			SomeoneAtDoor=""
			LoadVisitors()
		if DayNum==3:news_img=tk.PhotoImage(file="Images/Tv/NewsDay3.png")



#-----------------------------------------------------BUTTONS----------------------------------------------------------------
#ESC MENU
ResumeButton=tk.Button(root,text="Resume Game",command=LeaveCurrentState)
ResumeButton.place_forget()
SaveButton=tk.Button(root,text="Save Game",command=SaveGame)
SaveButton.place_forget()
LoadButton=tk.Button(root,text="Load Game",command=LoadGame)
LoadButton.place_forget()
HowToPlayButton=tk.Button(root,text="How To Play",command=LoadGame)
HowToPlayButton.place_forget()
ExitButton=tk.Button(root,text="Exit Game",command=ExitGame)
ExitButton.place_forget()
#BEDROOM
WatchTvButton=tk.Button(root,text="KATSO UUTISET TELKKARISTA",command=WatchTv)
WatchTvButton.place_forget()
SleepButton=tk.Button(root,text="KOODAA SÄNGYSSÄ",command=BedTime)
SleepButton.place_forget()
LeaveButton=tk.Button(root,text="TAKAISIN",command=LeaveCurrentState)
LeaveButton.place_forget()
#SOCIAL
InviteInButton=tk.Button(root,text=f"KUTSU {SomeoneAtDoor} SISÄÄN",command=InviteSomeoneIn)
InviteInButton.place_forget()
TalkButton_Linus=tk.Button(root,text=TalkButtonText,command=TalkToLinus)
TalkButton_Linus.place_forget()
#-------------------Raycasteröinti-------------------
def CastRays():
	WALL_HEIGHTS_LISTED=[]
	RAY_COUNT=SCREEN_W//RAY_WIDTH
	for col in range(SCREEN_W//RAY_WIDTH):
		RAY_A=(PLAYER_A-FOV/2)+(col/RAY_COUNT)*FOV
		RAY_D=0
		RAY_D_MAX=7
		RAY_HIT_WALL=False
		RAY_X=math.sin(RAY_A)
		RAY_Y=math.cos(RAY_A)

		while RAY_HIT_WALL==False and RAY_D<RAY_D_MAX:
			RAY_D+=GRAPHIC_ADJUST #Sharpness adjusting, put 0.05 if performance issues
			RAY_CHECK_X=int(PLAYER_X+(RAY_X*RAY_D))
			RAY_CHECK_Y=int(PLAYER_Y+(RAY_Y*RAY_D))
			if MAP[RAY_CHECK_X][RAY_CHECK_Y]=="#":
				RAY_HIT_WALL=True
		WALL_H=int(SCREEN_H/(RAY_D+0.01))
		WALL_HEIGHTS_LISTED.append(WALL_H)
	return WALL_HEIGHTS_LISTED

#--------------------Renderöys-------------------------
def DrawScreen():
	global RoomDrawn,RoomActive,TalkButtonText
	if not RoomActive:
		GameScreen.delete("all")
		#print("Room aint active")
		print(f"Day: {DayNum} | Night? {NightTime} | At the door: {SomeoneAtDoor}")
		WALL_HEIGHTS_LISTED=CastRays()
		for WALL_H_INDEX, WALL_H in enumerate(WALL_HEIGHTS_LISTED): #numeroittaa list itemin indexin muuttujaan WALL_H_INDEX
			X=WALL_H_INDEX*RAY_WIDTH
			WALL_TOP=(SCREEN_H-WALL_H)//2
			WALL_BOTTOM=(SCREEN_H-WALL_TOP)

			if WALL_H>SCREEN_H*0.75:COLOUR_WALL="#40113b"
			elif WALL_H>SCREEN_H*0.4:COLOUR_WALL="#320c2d"
			elif WALL_H>SCREEN_H*0.25:COLOUR_WALL="#23081e"
			else:COLOUR_WALL="#190514"

			GameScreen.create_rectangle(X,WALL_TOP,X+RAY_WIDTH,WALL_BOTTOM,fill=COLOUR_WALL,outline=COLOUR_WALL) #Seinän väritys
			GameScreen.create_rectangle(X,WALL_TOP-((SCREEN_H//2)-(WALL_H//2)),X+RAY_WIDTH,WALL_TOP,fill="#140410",outline="#140410") #Katon väritys
			GameScreen.create_rectangle(X,WALL_BOTTOM,X+RAY_WIDTH,WALL_BOTTOM+((SCREEN_H//2)-(WALL_H//2)),fill="#1c0d03",outline="#1c0d03") #Lattian väritys #47270e


		if MlemToggle:
			GameScreen.create_image(SCREEN_W/2,SCREEN_H/2,image=mlem_img)
		if EscMenuActive:
			GameScreen.create_image(SCREEN_W/2,SCREEN_H/2,image=escmenu_img)
			ResumeButton.place(x=SCREEN_W/2-490,y=SCREEN_H/2-120)
			SaveButton.place(x=SCREEN_W/2-490,y=SCREEN_H/2-50)
			LoadButton.place(x=SCREEN_W/2-490,y=SCREEN_H/2+20)
			HowToPlayButton.place(x=SCREEN_W/2-490,y=SCREEN_H/2+90)
			ExitButton.place(x=SCREEN_W/2-490,y=SCREEN_H/2+160)
		else:
			ResumeButton.place_forget()
			SaveButton.place_forget()
			LoadButton.place_forget()
			HowToPlayButton.place_forget()
			ExitButton.place_forget()

	else:
		if BedroomActive and not RoomDrawn:
			GameScreen.create_image(SCREEN_W/2,SCREEN_H/2,image=bedroom_img)
			WatchTvButton.place(x=SCREEN_W/2-600,y=SCREEN_H/2+150)
			SleepButton.place(x=SCREEN_W/2-600,y=SCREEN_H/2+220)
			LeaveButton.place(x=SCREEN_W/2-600,y=SCREEN_H/2+290)
			RoomDrawn=True
		elif not BedroomActive and RoomDrawn:
			WatchTvButton.place_forget()
			SleepButton.place_forget()
			LeaveButton.place_forget()
			RoomDrawn=False
			RoomActive=False

		if TvActive:
			GameScreen.create_image(SCREEN_W/2,SCREEN_H/2,image=news_img)
			WatchTvButton.place_forget()
			SleepButton.place_forget()
			LeaveButton.place(x=SCREEN_W/2-600, y=SCREEN_H/2+290)

		if LivingRoomActive: #                                                                      <<<ÄLÄ LAITA ELIF SE RIKKOUTUU HELPOSTI TOIMINNALLISUUKSIA LISÄTESSÄ
			GameScreen.create_image(SCREEN_W/2,SCREEN_H/2,image=living_room_img)
			LeaveButton.place(x=SCREEN_W/2-600,y=SCREEN_H/2+290)
		if OfficeActive:
			GameScreen.create_image(SCREEN_W/2,SCREEN_H/2,image=office_img)
			LeaveButton.place(x=SCREEN_W/2-600,y=SCREEN_H/2+290)
		if KitchenActive:
			GameScreen.create_image(SCREEN_W/2,SCREEN_H/2,image=kitchen_img)
			LeaveButton.place(x=SCREEN_W/2-600,y=SCREEN_H/2+290)
			if "Linus" in CharactersInside:
				if not TalkingToSomeone:
					GameScreen.create_image(SCREEN_W/2,SCREEN_H/2,image=Linus2_img)
				else:
					GameScreen.create_image(SCREEN_W/2,SCREEN_H/2,image=Linus1_img)
					#TalkButtonText="PUHU LINUKSELLE"
					#TalkButton_Linus.config(text=TalkButtonText)
				if DayNum==2 and NightTime==False:
					TalkButton_Linus.place(x=SCREEN_W/2-600,y=SCREEN_H/2+220)
					if TalkingToSomeone:
						#TalkButton_Linus.place_forget()
						DrawDialogue(AllCharacters["Linus"]["dialogue_2"], SCREEN_W/2, SCREEN_H/2-250)
		if StorageRoomActive:
			GameScreen.create_image(SCREEN_W/2,SCREEN_H/2,image=storage_room_img)
			LeaveButton.place(x=SCREEN_W/2-600,y=SCREEN_H/2+290)
		if BathroomActive:
			GameScreen.create_image(SCREEN_W/2,SCREEN_H/2,image=bathroom_img)
			LeaveButton.place(x=SCREEN_W/2-600,y=SCREEN_H/2+290)
		if FrontdoorActive:
			GameScreen.create_image(SCREEN_W/2,SCREEN_H/2,image=frontdoor_img)
			LeaveButton.place(x=SCREEN_W/2-600,y=SCREEN_H/2+290)
			if SomeoneAtDoor!="":
				GameScreen.create_image(SCREEN_W/2,SCREEN_H/2,image=visitor_img)
				InviteInButton.place(x=SCREEN_W/2-600,y=SCREEN_H/2+220)
				DrawDialogue(AllCharacters[SomeoneAtDoor]["dialogue_1"],SCREEN_W/2,SCREEN_H/2-250)

	root.after(60,DrawScreen)


#--------------------Key bindaukset --------------------------
def keypress(event):
	global PLAYER_X,PLAYER_Y,PLAYER_A,MlemToggle,AllowMovement,GRAPHIC_ADJUST,EscMenuActive,RoomActive,BedroomActive,LivingRoomActive,OfficeActive,KitchenActive,StorageRoomActive,BathroomActive,FrontdoorActive,TvActive

	#-----------------MENU AKTIVOINNIT----------------------
	if event.keysym.lower()=="m":
		if MlemToggle==True:
			MlemToggle=False
			AllowMovement=True
		else:
			MlemToggle=True
			AllowMovement=False

	if event.keysym.lower()=="escape" and not RoomActive:
		print(EscMenuActive)
		EscMenuActive=not EscMenuActive
		print(EscMenuActive)

	#------------------GRAFIIKAN SÄÄTÖ------------------------
	if event.keysym.lower()=="o" and GRAPHIC_ADJUST<0.1:GRAPHIC_ADJUST+=0.01
	if event.keysym.lower()=="p" and GRAPHIC_ADJUST>0.01:GRAPHIC_ADJUST-=0.01


#------------------ROOM CHECK STUFFS----------------------------------------------------------------------

	if PLAYER_X>=2 and PLAYER_X<=3 and PLAYER_Y>=1 and PLAYER_Y<=2: #         < < < < < BEDROOM
		print("Player in: Bedroom")
		BedroomActive=True
		RoomActive=True
		AllowMovement=False

	if PLAYER_X>=3 and PLAYER_X<=4 and PLAYER_Y>=3 and PLAYER_Y<=4: #         < < < < < LIVING ROOM
		print("Player in: Living Room")
		LivingRoomActive=True
		RoomActive=True
		AllowMovement=False

	if PLAYER_X>=1 and PLAYER_X<=2 and PLAYER_Y>=3 and PLAYER_Y<=4: #         < < < < < OFFICE
		print("Player in: Office")
		OfficeActive=True
		RoomActive=True
		AllowMovement=False

	if PLAYER_X>=1 and PLAYER_X<=2 and PLAYER_Y>=5 and PLAYER_Y<=6: #         < < < < < KITCHEN
		print("Player in: Kitchen")
		KitchenActive=True
		RoomActive=True
		AllowMovement=False

	if PLAYER_X>=2 and PLAYER_X<=3 and PLAYER_Y>=8 and PLAYER_Y<=9: #         < < < < < STORAGE
		#print("Player in: Storage Room")
		StorageRoomActive=True
		RoomActive=True
		AllowMovement=False

	if PLAYER_X>=4 and PLAYER_X<=5 and PLAYER_Y>=6 and PLAYER_Y<=7.3: #         < < < < < BATHROOM
		print("Player in: Bathroom")
		BathroomActive=True
		RoomActive=True
		AllowMovement=False

	if PLAYER_X>=6 and PLAYER_X<=7 and PLAYER_Y>=7 and PLAYER_Y<=8: #         < < < < < FRONTDOOR
		print("Player in: Looking through frontdoor")
		FrontdoorActive=True
		RoomActive=True
		AllowMovement=False


	#------------------UKKO LIIKKUU---------------------------
	if event.keysym.lower()=="w" or event.keysym.lower()=="up":
		if AllowMovement==True:
			PLAYER_X+=math.sin(PLAYER_A)*0.05
			PLAYER_Y+=math.cos(PLAYER_A)*0.05
	elif event.keysym.lower()=="s" or event.keysym.lower()=="down":
		if AllowMovement==True:
			PLAYER_X-=math.sin(PLAYER_A)*0.05
			PLAYER_Y-=math.cos(PLAYER_A)*0.05
	elif event.keysym.lower()=="d" or event.keysym.lower()=="right":
		if AllowMovement==True:
			PLAYER_A+=0.03
	elif event.keysym.lower()=="a" or event.keysym.lower()=="left":
		if AllowMovement==True:
			PLAYER_A-=0.03
	#-----------------------------------------------------------
	print(f"{PLAYER_X},{PLAYER_Y}")

root.bind("<KeyPress>",keypress)




#----------------------GAME LOOP STUFFS-------------------------
#print(SCREEN_W)
CreateTablesSQL()
DrawScreen()
LoadVisitors()
print(SomeoneAtDoor)

root.mainloop()
