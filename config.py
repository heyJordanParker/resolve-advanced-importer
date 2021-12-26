import sys
import os
import json
import tkinter as tk

DOCUMENTATION_URL = "https://neverproductive.notion.site/Resolve-Advanced-Importer-50f1a8a6241d4264824602054c499b31"

sleepBetweenChecks = 5

folderPath = tk.StringVar(value="C:\\Users\\jorda\\Downloads")

ignoredBinsEntry = tk.StringVar(value = "Master/Video Assets")
removeExtraFiles = tk.BooleanVar(value = True)
removeEmptyBins = tk.BooleanVar(value = True)
ignoredFileExtensions = tk.StringVar(value="json,ini")
unzipArchives = tk.BooleanVar(value = True)
deleteUnzippedArchives = tk.BooleanVar(value = True)

importToBinPath = "Master/Test"
timelinesBinPath = "Master/Timelines"
compoundClipsBinPath = "Master/Compound Clips"
fusionCompsBinPath = "Master/Fusion Comps"

# Runtime
importing = tk.BooleanVar(value = False)
importedMessage = tk.StringVar(value = "")
importToBin = None
timelinesBin = None
compoundClipsBin = None
fusionCompsBin = None
ignoredBins = []

def getConfigPath():
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(application_path, 'config.json')

def loadCache():
    global sleepBetweenChecks, folderPath, ignoredBinsEntry, ignoredFileExtensions, removeExtraFiles, removeEmptyBins, unzipArchives, deleteUnzippedArchives, importToBinPath, timelinesBinPath, compoundClipsBinPath, fusionCompsBinPath
    with open(getConfigPath(), "r") as configFile:
        data = json.load(configFile)
        sleepBetweenChecks = data["sleepBetweenChecks"]
        folderPath.set(data["folderPath"])
        ignoredBinsEntry.set(data["ignoredBinsEntry"])
        removeExtraFiles.set(data["removeExtraFiles"])
        removeEmptyBins.set(data["removeEmptyBins"])
        ignoredFileExtensions.set(data["ignoredFileExtensions"])
        unzipArchives.set(data["unzipArchives"])
        deleteUnzippedArchives.set(data["deleteUnzippedArchives"])
        importToBinPath = data["importToBinPath"]
        timelinesBinPath = data["timelinesBinPath"]
        compoundClipsBinPath = data["compoundClipsBinPath"]
        fusionCompsBinPath = data["fusionCompsBinPath"]

def saveCache():
    data = None
    with open(getConfigPath(), "r") as configFile:
        data = json.load(configFile)
        data["folderPath"] = folderPath.get()
        data["ignoredBinsEntry"] = ignoredBinsEntry.get()
        data["removeExtraFiles"] = removeExtraFiles.get()
        data["removeEmptyBins"] = removeEmptyBins.get()
        data["ignoredFileExtensions"] = ignoredFileExtensions.get()
        data["unzipArchives"] = unzipArchives.get()
        data["deleteUnzippedArchives"] = deleteUnzippedArchives.get()
        data["importToBinPath"] = importToBinPath
        data["timelinesBinPath"] = timelinesBinPath
        data["compoundClipsBinPath"] = compoundClipsBinPath
        data["fusionCompsBinPath"] = fusionCompsBinPath

    with open(getConfigPath(), "w") as configFile:
        json.dump(data, configFile, indent=4)

def getResolvePath():
    with open(getConfigPath(), "r") as file:
        data = json.load(file)
        resolvePath = data["resolvePath"]

    return resolvePath

loadCache()


