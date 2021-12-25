import tkinter as tk
from icon import icon

mainWindow = tk.Tk()

def InitializeTkWindow():
    mainWindow.title("DaVinci Resolve Advanced Importer")
    mainWindow.resizable(False, False)
    mainWindow.call('wm', 'iconphoto', mainWindow._w, tk.PhotoImage(data=icon))
