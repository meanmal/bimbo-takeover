import os
import sys
import ctypes
import winreg
import tkinter as tk
from tkinter import Canvas
import random

def set_wallpaper(path):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)

def set_pink_accent():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Accent", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "AccentColor", 0, winreg.REG_DWORD, 0x00B469FF)  # hot pink
        winreg.SetValueEx(key, "ColorPrevalence", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
        key2 = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\DWM", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key2, "AccentColor", 0, winreg.REG_DWORD, 0x00B469FF)
        winreg.CloseKey(key2)
    except:
        pass

def add_to_startup():
    try:
        startup = os.path.join(os.getenv('APPDATA'), r"Microsoft\Windows\Start Menu\Programs\Startup")
        bat = os.path.join(startup, "bimbo_takeover.bat")
        script = os.path.abspath(sys.argv[0])
        with open(bat, "w") as f:
            f.write(f'pythonw "{script}"\n')
    except:
        pass

class BimboOverlay(tk.Tk):
    def __init__(self):
        super().__init__()
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.attributes("-transparentcolor", "#000000")
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        self.geometry(f"{w}x{h}+0+0")
        self.canvas = Canvas(self, bg="#000000", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.hearts = []
        for _ in range(30):
            x = random.randint(0, w)
            y = random.randint(0, h)
            heart = self.canvas.create_text(x, y, text="💖", fill="#FF69B4", font=("Segoe UI Emoji", 28))
            self.hearts.append({"id": heart, "x": x, "y": y, "speed": random.uniform(0.8, 2.8), "drift": random.uniform(-1.2, 1.2)})
        self.animate()
        self.bind("<Escape>", lambda e: self.destroy())

    def animate(self):
        screen_h = self.winfo_screenheight()
        screen_w = self.winfo_screenwidth()
        for h in self.hearts:
            self.canvas.move(h["id"], h["drift"], -h["speed"])
            h["y"] -= h["speed"]
            h["x"] += h["drift"]
            if h["y"] < -20:
                h["x"] = random.randint(0, screen_w)
                h["y"] = screen_h + 30
                self.canvas.coords(h["id"], h["x"], h["y"])
        self.after(35, self.animate)

def main():
    wallpaper = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bimbo_wallpaper.jpg")
    if os.path.exists(wallpaper):
        set_wallpaper(wallpaper)
    set_pink_accent()
    add_to_startup()
    BimboOverlay().mainloop()

if __name__ == "__main__":
    main()
