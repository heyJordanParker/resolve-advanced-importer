import tkinter as tk
from icon import icon

# load yaml to initialize config with
# load resolve path form yaml separately
resolvePath = None

mainWindow = tk.Tk()

def InitializeTkWindow():
    mainWindow.title("DaVinci Resolve Advanced Importer")
    mainWindow.resizable(False, False)
    mainWindow.call('wm', 'iconphoto', mainWindow._w, tk.PhotoImage(data=icon))

def initializeConfig():
    pass