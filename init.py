import base64
import tkinter as tk
from PIL import ImageTk, Image
from icon import icon

mainWindow = tk.Tk()

def InitializeTkWindow():
    mainWindow.title("DaVinci Resolve Advanced Importer")
    mainWindow.resizable(False, False)
    mainWindow.call('wm', 'iconphoto', mainWindow._w, ImageTk.PhotoImage(data=base64.b64decode(icon)))
