import tkinter as tk
import math

#--------------------Alustusmuuttujia-----------------
SCREEN_W=1280
SCREEN_H=720

PLAYER_X=1
PLAYER_Y=0
PLAYER_A=0
Pi=3.141592
FOV=Pi/3

#--------------------Level mappi--------------------
MAP_W=8
MAP_H=6
MAP=[
	"########",
	"#......#",
	"#......#",
	"#......#",
	"#......#",
	"########"]

#--------------------Tkinter Setup--------------------
#Luodaan root ikkuna
root=tk.Tk()
root.title("Yes, I Use Arch BTW")
root.geometry(f"{SCREEN_W}x{SCREEN_H}")

#Luodaan canvas gameplaylle root ikkunaan, ja käytetään pack asettelua
GameScreen=tk.Canvas(root,width=SCREEN_W,height=SCREEN_H,bg="#000000")
GameScreen.pack()

#-------------------Raycasteröinti-------------------
#def raycast():
#--------------------Renderöys-------------------------














#mlem=tk.PhotoImage(file="cat.png")
#GameScreen.create_image(SCREEN_W/2,SCREEN_H/2,image=mlem)
#--------------------Key bindaukset --------------------------
def keypress(event):
	global PLAYER_X,PLAYER_Y
	if event.keysym.lower()=="w":
		PLAYER_X+=1
		#print(PLAYER_X)
	elif event.keysym.lower()=="s":
		PLAYER_X-=1
		#print(PLAYER_X)
	elif event.keysym.lower()=="d":
		PLAYER_Y+=1
		#print(PLAYER_Y)
	elif event.keysym.lower()=="a":
		PLAYER_Y-=1
		#print(PLAYER_Y)
	print(f"{PLAYER_X}, {PLAYER_Y}")
root.bind("<KeyPress>",keypress)

#----------------------GAME LOOP STUFFS-------------------------
#print(SCREEN_W)
root.mainloop()
