import tkinter as tk

#--------------------Alustusmuuttujia-----------------
SCREEN_W=1280
SCREEN_H=720


#--------------------Tkinter Setup--------------------
#Luodaan root ikkuna
root=tk.Tk()
root.title("Yes, I Use Arch BTW")
root.geometry(f"{SCREEN_W}x{SCREEN_H}")

#Luodaan canvas gameplaylle root ikkunaan, ja käytetään pack asettelua
GameScreen=tk.Canvas(root,width=SCREEN_W,height=SCREEN_H,bg="#000000")
GameScreen.pack()

#--------------------Renderöys-------------------------
mlem=tk.PhotoImage(file="cat.png")
GameScreen.create_image(SCREEN_W/2,SCREEN_H/2,image=mlem)
#--------------------Key bindaukset --------------------------


#----------------------GAME LOOP STUFFS-------------------------
#print(SCREEN_W)
root.mainloop()
