import tkinter as tk

#--------------------Alustusmuuttujia-----------------
SCREEN_W=500
SCREEN_H=500

#--------------------Tkinter Setup--------------------
root=tk.Tk()
root.title("Yes, I Use Arch BTW")
GameScreen=tk.Canvas(root,width=SCREEN_W,height=SCREEN_H,bg="#000000")
GameScreen.pack()

root.mainloop()
