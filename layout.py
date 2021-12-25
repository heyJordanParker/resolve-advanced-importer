import re
import tkinter as tk
import textwrap
import webbrowser
from init import (mainWindow, InitializeTkWindow)
from resolve import mediaPool
import config as c
from binSelector import BinSelector
from resolveBinTree import ResolveBinTree
from resolveImporter import ResolveImporter
from tkinter import ttk
from tkinter import Grid
from tkinter import messagebox
from tkinter import filedialog
from tkinter.messagebox import showerror, askokcancel, WARNING

mainFrame = ttk.Frame(mainWindow)
folderPathFrame = ttk.LabelFrame(mainFrame, text="Auto Importer")
controlFrame = ttk.Frame(mainFrame)
configFrame = ttk.LabelFrame(mainFrame, text="Auto Importer Configuration")
extraFunctionsFrame = ttk.LabelFrame(mainFrame, text="Extra Functions")

# for during importing
disabledControlsDuringImport = []

def initializeFrames():
    mainFrame.grid(column=0, row=0, padx = 10, pady = 10)

    for i in range(10):
        mainFrame.grid_rowconfigure(i, weight=1)
        mainFrame.grid_columnconfigure(i, weight=1)

    folderPathFrame.grid(row = 0, sticky="nsew", ipady=5)
    configFrame.grid(row = 1, sticky="nsew", ipady=5)
    extraFunctionsFrame.grid(row = 2, sticky="nsew", ipady=5)
    controlFrame.grid(row = 3, sticky="nsew", ipady=5)

    Grid.columnconfigure(controlFrame, 0, weight = 1)
    
def initializeFolderPathFrame():
    importFolderLabel = ttk.Label(folderPathFrame, text="Select Target Directory:")
    importFolderLabel.grid(row = 0, columnspan=3, sticky=tk.W)

    folderPathEntry = ttk.Entry(folderPathFrame, textvariable = c.folderPath)
    folderPathEntry.grid(row = 1, columnspan=2, ipadx = 172, pady = 10, sticky=tk.EW)
    disabledControlsDuringImport.append(folderPathEntry)

    def folderPathEntry_FocusOut(e):
        ResolveImporter.validateImportPath()

    folderPathEntry.bind('<FocusOut>', folderPathEntry_FocusOut)

    def openFolderButton_Click():
        path = filedialog.askdirectory(
            title='Select Target Directory to auto-import',
            initialdir='/')

        if path:
            c.folderPath.set(path)

    openFolderButton = ttk.Button(folderPathFrame, text='Select Folder', command=openFolderButton_Click, width=25)
    disabledControlsDuringImport.append(openFolderButton)
    openFolderButton.grid(column = 2, row = 1, columnspan=1, padx=10)

    rootBinLabel = ttk.Label(folderPathFrame, text="Select a root bin:")
    rootBinLabel.grid(row = 2, column=0, columnspan=2, sticky=tk.W)
    
    def selectRootBin(e):
        c.importToBin = rootBinSelector.getSelectedBin()
        print(f"Initialized Root bin: {c.importToBin}")

    rootBinSelector = BinSelector(folderPathFrame, c.importToBinPath, selectRootBin, False, width=23)
    rootBinSelector.grid(row=2, column=2, columnspan=1, sticky=tk.W, padx=10)
    disabledControlsDuringImport.append(rootBinSelector)
        
    # Update the selected bin
    selectRootBin(None)
    
def initializeConfigFrame():
    currentRow = 0
    
    ignoredFileExtensionsLabel = ttk.Label(configFrame, text="Ignored File Extensions:")
    ignoredFileExtensionsLabel.grid(row=currentRow, column=0, columnspan=1, sticky=tk.EW)

    ignoredFileExtensionsEntry = ttk.Entry(configFrame, textvariable = c.ignoredFileExtensions)
    ignoredFileExtensionsEntry.grid(row=currentRow, column=1, columnspan=2, sticky=tk.EW, padx=(20, 10), ipadx=97)
    disabledControlsDuringImport.append(ignoredFileExtensionsEntry)

    def ignoredFileExtensionsEntry_FocusOut(e):
        extensionsMatcher = re.compile(r'^[\w\-,]+$')
        ignoredExtensionsString = c.ignoredFileExtensions.get().replace('.', '').replace(' ', '')
        if not re.fullmatch(extensionsMatcher, ignoredExtensionsString):
            showerror(title="Error", message="Invalid ignored extensions. Please list one or more file extensions separated by commas.")
            return
        
        c.ignoredFileExtensions.set(ignoredExtensionsString)
        

    ignoredFileExtensionsEntry.bind('<FocusOut>', ignoredFileExtensionsEntry_FocusOut)
    
    currentRow += 1
    
    removeFilesLabel = ttk.Label(configFrame, text="Automatically remove from Resolve:")
    removeFilesLabel.grid(row=currentRow, column=0, sticky=tk.EW, pady = (10,0))

    def removeExtraFiles_Toggle():
        isOn = removeExtraFilesCheckboxString.get() == "1"
        
        c.removeExtraFiles.set(isOn)
        
        if isOn:
            messagebox.showwarning(title="Read before starting the Auto Importer", message=textwrap.dedent("""\
                This will make the Auto Importer remove any unused file that is in Resolve but not in the Target Directory in Resolve.
                
                This is designed to allow you to manage your files only in your filesystem and Resolve to match your changes.
                
                Note: This will never delete files that are already in use."""))

    removeExtraFilesCheckboxString = tk.StringVar(value="1" if c.removeExtraFiles.get() else "0")
    removeExtraFilesCheckbox = ttk.Checkbutton(configFrame, text="Remove Extra Files", command=removeExtraFiles_Toggle, 
                                            variable=removeExtraFilesCheckboxString, onvalue="1", offvalue="0")
    removeExtraFilesCheckbox.grid(row=currentRow, column=1, sticky=tk.W, padx=(20, 0), pady = (10,0))
    disabledControlsDuringImport.append(removeExtraFilesCheckbox)

    def removeEmptyBinsArchives_Toggle():
        isOn = removeEmptyBinsCheckboxString.get() == "1"
        
        c.removeEmptyBins.set(isOn)
        
        if isOn:
            messagebox.showwarning(title="Read before starting the Auto Importer", message=textwrap.dedent("""\
                This will make the Auto Importer look for empty bins in Resolve and remove them.
                
                This is designed to allow you to manage your files only in your filesystem and Resolve to match your changes.
                
                Note: This will never delete folders with items in them.
                Note: If you enabled the \"Remove Extra Files\" option — the Auto Importer will delete any folder that has only unused files in it."""))

    removeEmptyBinsCheckboxString = tk.StringVar(value="1" if c.removeEmptyBins.get() else "0")
    removeEmptyBinsCheckbox = ttk.Checkbutton(configFrame, text="Delete Empty Bins", command=removeEmptyBinsArchives_Toggle, 
                                            variable=removeEmptyBinsCheckboxString, onvalue="1", offvalue="0")
    removeEmptyBinsCheckbox.grid(row=currentRow, column=2, sticky=tk.W, padx=(10, 0), pady = (10,0))
    disabledControlsDuringImport.append(removeEmptyBinsCheckbox)
    
    currentRow += 1
    
    keepBinsLabel = ttk.Label(configFrame, text="Ignored Bins (never delete them):")
    keepBinsLabel.grid(row=currentRow, column=0, sticky=tk.EW, pady = (10,0))
    
    currentRow += 1
    
    ignoredBinsEntry = ttk.Entry(configFrame, textvariable = c.ignoredBinsEntry)
    ignoredBinsEntry.grid(row = currentRow, columnspan=2, ipadx = 172, pady = 10, sticky=tk.EW)
    ignoredBinsEntry["state"] = "readonly"
    
    def updateIgnoredBins(keepBinLabel):
        c.ignoredBins.clear()
        
        addedKeepBin = "," + ignoredBinSelector.getSelectedBin().getPath() if keepBinLabel else ""
        binsEntry = c.ignoredBinsEntry.get() + addedKeepBin
            
        binPaths = list(dict.fromkeys(binsEntry.split(",")))
        binPaths.reverse()
        
        masterBin = ResolveBinTree.get()
        finalPaths = ""
        
        for binPath in binPaths:
            if not binPath:
                continue
            
            bin = masterBin.findBinFromPath(binPath)
            
            if bin:
                c.ignoredBins.insert(0, bin)
                finalPaths = "," + bin.getPath() + finalPaths
        
        if len(finalPaths) > 1:
            finalPaths = finalPaths[1:]
            
        c.ignoredBinsEntry.set(finalPaths)
        
    clearLabel = "Clear"
    
    def addIgnoredBin(e):
        if ignoredBinSelector.getSelectedBin():
            updateIgnoredBins(ignoredBinSelector.getSelectedBin().getPath())
        else:
            c.ignoredBins.clear()
            c.ignoredBinsEntry.set("")
            
        ignoredBinSelector.set(clearLabel)

    ignoredBinSelector = BinSelector(configFrame, clearLabel, addIgnoredBin, True, clearLabel, width=23)
    ignoredBinSelector.grid(row=currentRow, column=2, columnspan=1, sticky=tk.W, padx=10)
    disabledControlsDuringImport.append(ignoredBinSelector)
    
    updateIgnoredBins(None)
    
    currentRow += 1
    
    unzipArchivesLabel = ttk.Label(configFrame, text="Unzip & Delete archives:")
    unzipArchivesLabel.grid(row=currentRow, column=0, sticky=tk.EW)

    def unzipArchives_Toggle():
        isOn = unzipArchivesCheckboxString.get() == "1"
        
        c.unzipArchives.set(isOn)
        
        if isOn:
            messagebox.showwarning(title="Read before starting the Auto Importer", message="This will make the Auto Importer unzip all archives in the specified directory and then import the files inside. Useful when working with B-Roll websites.")

    unzipArchivesCheckboxString = tk.StringVar(value="1" if c.unzipArchives.get() else "0")
    unzipArchivesCheckbox = ttk.Checkbutton(configFrame, text="Unzip Archives", command=unzipArchives_Toggle, 
                                            variable=unzipArchivesCheckboxString, onvalue="1", offvalue="0")
    unzipArchivesCheckbox.grid(row=currentRow, column=1, sticky=tk.W, padx=(20, 0))
    disabledControlsDuringImport.append(unzipArchivesCheckbox)

    def deleteUnzippedArchives_Toggle():
        isOn = deleteUnzippedArchivesCheckboxString.get() == "1"
        c.deleteUnzippedArchives.set(isOn)
        
        if isOn:
            messagebox.showwarning(title="Read before starting the Auto Importer", message="This will make the Auto Importer delete all unzipped archives after extraction from the import folder.")

    deleteUnzippedArchivesCheckboxString = tk.StringVar(value="1" if c.deleteUnzippedArchives.get() else "0")
    deleteUnzippedArchivesCheckbox = ttk.Checkbutton(configFrame, text="Delete Unzipped Archives", command=deleteUnzippedArchives_Toggle, 
                                            variable=deleteUnzippedArchivesCheckboxString, onvalue="1", offvalue="0")
    deleteUnzippedArchivesCheckbox.grid(row=currentRow, column=2, sticky=tk.W, padx=(10, 0))
    disabledControlsDuringImport.append(deleteUnzippedArchivesCheckbox)

def initializeExtraFunctionsFrame():
    currentRow = 0
    
    timelineBinLabel = ttk.Label(extraFunctionsFrame, text = "Automatically move all timelines to bin:")
    timelineBinLabel.grid(row = currentRow, columnspan=2, pady = 10, sticky=tk.EW)
    
    def selectTimelinesBin(e):
        c.timelinesBin = timelineBinSelector.getSelectedBin()
        print(f"Initialized Timelines bin: {c.timelinesBin}")

    timelineBinSelector = BinSelector(extraFunctionsFrame, c.timelinesBinPath, selectTimelinesBin, True, width=23)
    timelineBinSelector.grid(row=currentRow, column=2, columnspan=3, sticky=tk.E)
    disabledControlsDuringImport.append(timelineBinSelector)
    
    selectTimelinesBin(None)
    
    currentRow += 1
    
    compoundClipsBinLabel = ttk.Label(extraFunctionsFrame, text = "Automatically move all compound clips to bin:")
    compoundClipsBinLabel.grid(row = currentRow, columnspan=2, pady = 10, sticky=tk.EW)
    
    def selectCompoundClipsBin(e):
        c.compoundClipsBin = compounClipsBinSelector.getSelectedBin()
        print(f"Initialized Compound clips bin: {c.compoundClipsBin}")
        

    compounClipsBinSelector = BinSelector(extraFunctionsFrame, c.compountClipsBinPath, selectCompoundClipsBin, True, width=23)
    compounClipsBinSelector.grid(row=currentRow, column=2, columnspan=3, sticky=tk.E)
    disabledControlsDuringImport.append(compounClipsBinSelector)
    
    selectCompoundClipsBin(None)
    
    currentRow += 1
    
    fusionCompsBinLabel = ttk.Label(extraFunctionsFrame, text = "Automatically move all fusion comps to bin:")
    fusionCompsBinLabel.grid(row = currentRow, columnspan=2, pady = 10, sticky=tk.EW)
    
    def selectFusionCompsBin(e):
        c.fusionCompsBin = fusionCompsBinSelector.getSelectedBin()
        print(f"Initialized Fusion comps bin: {c.fusionCompsBin}")

    fusionCompsBinSelector = BinSelector(extraFunctionsFrame, c.fusionCompsBinPath, selectFusionCompsBin, True, width=23)
    fusionCompsBinSelector.grid(row=currentRow, column=2, columnspan=3, sticky=tk.E)
    disabledControlsDuringImport.append(fusionCompsBinSelector)
    
    selectFusionCompsBin(None)
    
    currentRow += 1
    
    manuallyRemoveLabel = ttk.Label(extraFunctionsFrame, text="Manually Remove:")
    manuallyRemoveLabel.grid(row=currentRow, column=0, sticky=tk.EW, pady = (10,0), padx=(0, 160))

    def deleteUnusedFilesButton_Click():
        unusedFiles = ResolveBinTree.get().getUnusedFiles()
        
        filePaths = ""
        i = 0
        for unusedFile in unusedFiles:
            if i >= 2:
                filePaths += f"\nand {len(unusedFiles) - i} more...\n"
                break
            filePaths += f"{unusedFile.GetClipProperty()['File Path']}\n"
            i += 1
        
        confirm = askokcancel(title="Confirm Deletion of Unused Files",
                    message=f"{len(unusedFiles)} unused files will be removed from Resolve:\n\n{filePaths}\nThose can easily be found using a Smart Bin.\n\nNote: Use the help button to go to a page that explains that and more.", icon = WARNING)
        
        if confirm:
            print(f"[{c.importToBin.getName()}] Deleting {len(unusedFiles)} unused files.")
            c.importToBin.deleteClips(unusedFiles, deleteFiles=True, refresh=True)
        
    removeUnusedFilesButton = ttk.Button(extraFunctionsFrame, text="Unused Files", command=deleteUnusedFilesButton_Click)
    
    removeUnusedFilesButton.grid(row=currentRow, column=1, sticky=tk.W, padx=(20, 0), pady = (10,0), ipadx=14)
    disabledControlsDuringImport.append(removeUnusedFilesButton)

    def removeMissingClipsButton_Click():
        missingClips = ResolveBinTree.get().getMissingClips()
        
        clipPaths = ""
        i = 0
        for clip in missingClips:
            if i >= 9:
                clipPaths += f"\nand {len(missingClips) - i} more...\n"
                break
            clipPaths += f"{clip.GetClipProperty()['File Path']}\n"
            i += 1
        
        confirm = askokcancel(title="Confirm Deletion of Missing Clips",
                    message=f"{len(missingClips)} missing clips will be removed from Resolve:\n\n{clipPaths}\nThose can easily be found using a Smart Bin.\n\nNote: Use the help button to go to a page that explains that and more.", icon = WARNING)
        
        if confirm:
            print(f"[{c.importToBin.getName()}] Deleting {len(missingClips)} missing clips.")
            c.importToBin.deleteClips(missingClips, refresh=True)
        
    removeMissingClipsButton = ttk.Button(extraFunctionsFrame, text="Missing Clips", command=removeMissingClipsButton_Click)
    removeMissingClipsButton.grid(row=currentRow, column=2, sticky=tk.W, padx=(20, 0), pady = (10,0), ipadx=14)
    disabledControlsDuringImport.append(removeMissingClipsButton)
    
    def removeEmptyBinsButton_Click():
        emptyBins = ResolveBinTree.get().getEmptyChildBins([c.importToBin], recursive=True, delete=False)
        
        binPaths = ""
        i = 0
        for bin in emptyBins:
            if i >= 9:
                binPaths += f"\nand {len(emptyBins) - i} more...\n"
                break
            binPaths += f"{bin.getPath()}\n"
            i += 1
        
        confirm = askokcancel(title="Confirm Deletion of Empty Bins",
                    message=f"{len(emptyBins)} empty bins will be removed from Resolve. \n\n{binPaths}\nRemoving empty bins should not have any significant impact on your project.", icon = WARNING)
        
        if confirm:
            currentBin = mediaPool.GetCurrentFolder()
            ResolveBinTree.get().getEmptyChildBins(recursive=True, delete=True)
            mediaPool.SetCurrentFolder(currentBin)
        
    removeEmptyBinsButton = ttk.Button(extraFunctionsFrame, text="Empty Bins", command=removeEmptyBinsButton_Click)
    removeEmptyBinsButton.grid(row=currentRow, column=3, sticky=tk.W, padx=(20, 0), pady = (10,0), ipadx=14)
    disabledControlsDuringImport.append(removeEmptyBinsButton)

def initializeControlFrame():
    tk.Label(controlFrame).grid(row = 0) # spacer
    tk.Label(controlFrame, textvariable=c.importedMessage).grid(row = 1, sticky=tk.W) # message
    
    progressIndicator = ttk.Progressbar(
        controlFrame,
        orient='horizontal',
        mode='indeterminate',
        length=280,
    )
    progressIndicator.grid(row = 2, column=0, columnspan=2, sticky=tk.W)
    progressIndicator.grid_remove()
    progressIndicator.start()
    
    def helpButton_Click():
        webbrowser.open(c.DOCUMENTATION_URL)
    
    buttonWidth = 28
    
    helpButton = ttk.Button(controlFrame, text="Help", command=helpButton_Click, width = buttonWidth)
    helpButton.grid(row = 2, column=1, padx=(0,15))
    
    startButton = ttk.Button(controlFrame, text='Start Importer', command=ResolveImporter.toggleImport, width=buttonWidth)
    startButton.grid(row = 2, column=2)

    def updateStartButtonText(*args):
        if c.importing.get() == True:
            for control in disabledControlsDuringImport:
                control["state"] = "disabled"
            text = "Stop Auto Importer"
            progressIndicator.grid()
        else:
            for control in disabledControlsDuringImport:
                control["state"] = "readonly" if isinstance(control, BinSelector) else "normal"
            text = "Start Auto Importer"
            progressIndicator.grid_remove()
                
        startButton["text"] = text

    c.importing.trace('w', updateStartButtonText)
        
def showWindow():
    InitializeTkWindow()
    
    def mainWindow_onClose():
        if c.importing.get() == True:
            messagebox.showerror("Quit", "Please stop the importer before quitting")
        elif messagebox.askokcancel("Quit", "Do you want to quit?"):
            mainWindow.destroy()
    
    mainWindow.protocol("WM_DELETE_WINDOW", mainWindow_onClose)
    mainWindow.mainloop()
    
def initializeWindow():
    initializeFrames()
    initializeFolderPathFrame()
    initializeConfigFrame()
    initializeExtraFunctionsFrame()
    initializeControlFrame()
        