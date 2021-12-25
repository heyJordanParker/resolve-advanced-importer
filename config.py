import tkinter as tk
from resolveBinTree import *

DOCUMENTATION_URL = "https://neverproductive.notion.site/Resolve-Advanced-Importer-50f1a8a6241d4264824602054c499b31"

sleepBetweenChecks = 5

folderPath = tk.StringVar(value="C:\\Users\\jorda\\Downloads")
importing = tk.BooleanVar(value = False)
importedMessage = tk.StringVar(value = "")

ignoredBinsEntry = tk.StringVar(value = "Master/Video Assets")
removeExtraFiles = tk.BooleanVar(value = True)
removeEmptyBins = tk.BooleanVar(value = True)
ignoreFiles = tk.BooleanVar(value = True)
ignoredFileExtensions = tk.StringVar(value="json,ini")
unzipArchives = tk.BooleanVar(value = True)
deleteUnzippedArchives = tk.BooleanVar(value = True)
removeDeleteFiles = tk.BooleanVar(value = True)

importToBinPath = "Master/Test"
timelinesBinPath = "Master/Timelines"
compountClipsBinPath = "Master/Compound Clips"
fusionCompsBinPath = "Master/Fusion Comps"

# Runtime
importToBin = None
timelinesBin = None
compoundClipsBin = None
fusionCompsBin = None
ignoredBins = []