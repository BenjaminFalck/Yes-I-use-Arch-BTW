import tkinter as tk
import math

#--------------------Alustusmuuttujia-----------------
SCREEN_W=1280
SCREEN_H=720

PLAYER_X=2.5
PLAYER_Y=1.5
PLAYER_A=0
FOV=math.pi/3
RAY_WIDTH=2

GRAPHIC_ADJUST=0.01

MlemToggle=False
AllowMovement=True

#--------------------Level mappi--------------------
MAP_W=10
MAP_H=8
MAP=[
	"##########",
	"###.#.####",
	"#........#",
	"###.#.#.##",
	"######...#",
	"#######..#",
	"#######.##",
	"##########"]

#--------------------Tkinter Setup--------------------
#Luodaan root ikkuna
root=tk.Tk()
root.title("Yes, I Use Arch BTW")
root.geometry(f"{SCREEN_W}x{SCREEN_H}")

#Luodaan canvas gameplaylle root ikkunaan, ja käytetään pack asettelua
GameScreen=tk.Canvas(root,width=SCREEN_W,height=SCREEN_H,bg="#000000")
GameScreen.pack()

mlem_img=tk.PhotoImage(file="cat.png")
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
	GameScreen.delete("all")
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

	root.after(30,DrawScreen)

#--------------------Key bindaukset --------------------------
def keypress(event):
	global PLAYER_X,PLAYER_Y,PLAYER_A,MlemToggle,AllowMovement,GRAPHIC_ADJUST
	#-----------------MENU AKTIVOINNIT----------------------
	if event.keysym.lower()=="m":
		if MlemToggle==True:
			MlemToggle=False
			AllowMovement=True
		else:
			MlemToggle=True
			AllowMovement=False
	#------------------GRAFIIKAN SÄÄTÖ------------------------
	if event.keysym.lower()=="o" and GRAPHIC_ADJUST<0.1:GRAPHIC_ADJUST+=0.01
	if event.keysym.lower()=="p" and GRAPHIC_ADJUST>0.01:GRAPHIC_ADJUST-=0.01
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
DrawScreen()
root.mainloop()
