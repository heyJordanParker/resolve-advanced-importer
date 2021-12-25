import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from resolveBinTree import ResolveBinTree

class BinSelector(ttk.Combobox):
    
    def __init__(self, master, selectedBinLabel, selectBinFunction, allowNoSelection = True, noneLabel = "None", **kw) -> None:
        self.allowNoSelection = allowNoSelection
        self.selectBinFunction = selectBinFunction
        self.noneLabel = noneLabel
        self.binPaths = self.generateBinPaths()
        
        self.selectedBin = self.findSelectedBinFromPath(selectedBinLabel)
        
        self.selectedBinLabelVar = tk.StringVar(value = selectedBinLabel)
        
        self.setSelectedBin(self.selectedBin, selectedBinLabel)
        
        super().__init__(master, textvariable=self.selectedBinLabelVar, **kw)
        
        self["values"] = self.binPaths
        
        self.bind('<FocusIn>', self.onFocusIn)
        self.bind('<<ComboboxSelected>>', self.onItemSelected)
        self.bind('<ButtonPress>', self.onConfigure)
        self["state"] = "readonly"
        
    def getSelectedBin(self):
        return self.selectedBin
    
    def getSelectedBinPath(self):
        return self.selectedBinLabel
    
    def getMasterBin(self):
        return ResolveBinTree.get()
    
    def getDefaultBin(self):
        return None if self.allowNoSelection else self.getMasterBin()
    
    def findSelectedBinFromPath(self, selectedBinPath):
        if self.allowNoSelection and selectedBinPath == self.noneLabel:
            return None
        
        masterBin = ResolveBinTree.get()
        defaultBin = None if self.allowNoSelection else masterBin
        
        bin = masterBin.findBinFromPath(selectedBinPath, defaultBin)
        
        if bin == defaultBin:
            selectedBinPath = masterBin.getPath() if masterBin else ""
            print("[Bin Selector] Failed to find bin")
            
        return bin
        
    
    def setSelectedBin(self, selectedBin, selectedBinLabel = None):
        
        self.selectedBin = selectedBin
        if selectedBin:
            self.selectedBinLabel = selectedBinLabel
            
        self.selectedBinLabelVar.set(selectedBinLabel)
        
    def generateBinPaths(self):
        labels = ResolveBinTree.get().getBinPathsRecursive()
        
        if self.allowNoSelection:
            labels.insert(0, self.noneLabel)
        
        return labels
        
    def onConfigure(self, event):
        style = ttk.Style()

        long = max(self.cget('values'), key=len)

        font = tkfont.nametofont(str(self.cget('font')))
        width = max(0,font.measure(long.strip() + '0') - self.winfo_width())

        style.configure('TCombobox', postoffset=(0,0,width,0))
        
    def onFocusIn(self, event):
        self["values"] = self.binPaths = self.generateBinPaths()
        
    def onItemSelected(self, event):
        selectedBinPath = self.selectedBinLabelVar.get()
        
        bin = self.findSelectedBinFromPath(selectedBinPath)
        
        self.setSelectedBin(bin, selectedBinPath)
        self.selectBinFunction(event)