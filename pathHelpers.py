from pathlib import Path
        
def getFileNameFromPath(path):
    return Path(path).resolve().stem

def getFolderNameFromPath(path):
    return Path(path).resolve().name

def getFileExtensionFromPath(path):
    return Path(path).resolve().suffix

def getPathWithoutFileExtension(path):
    return Path(path).with_suffix('')
