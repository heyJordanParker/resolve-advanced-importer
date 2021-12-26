import sys
import imp
import os
import json
import config as c

def GetResolve():
    scriptModule = None
    try:
        import fusionscript as scriptModule
    except ImportError:
        resolvePath = c.getResolvePath()
        # Look for an auto importer config path
        if resolvePath:
            try:
                scriptModule = imp.load_dynamic("fusionscript", resolvePath)
            except ImportError:
                print("[Resolve Importer] Failed to load resolve at config path: " + resolvePath)
                pass

        if not scriptModule:
            # Look for installer based environment variables:
            libPath=os.getenv("RESOLVE_SCRIPT_LIB")
            if libPath:
                try:
                    scriptModule = imp.load_dynamic("fusionscript", libPath)
                except ImportError:
                    pass

        if not scriptModule:
            # Look for default install locations:
            ext=".so"
            if sys.platform.startswith("darwin"):
                path = "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/"
            elif sys.platform.startswith("win") or sys.platform.startswith("cygwin"):
                ext = ".dll"
                path = "C:\\Program Files\\Blackmagic Design\\DaVinci Resolve\\"
            elif sys.platform.startswith("linux"):
                path = "/opt/resolve/libs/Fusion/"
            try:
                scriptModule = imp.load_dynamic("fusionscript", path + "fusionscript" + ext)
            except ImportError:
                pass

    if scriptModule:
        sys.modules["DaVinciResolveScript"] = scriptModule
        import DaVinciResolveScript as bmd
    else:
        raise ImportError("Could not locate module dependencies")

    return bmd.scriptapp("Resolve")

resolve = GetResolve()
projectManager = resolve.GetProjectManager()
project = projectManager.GetCurrentProject()
mediaPool = project.GetMediaPool()
mediaStorage = resolve.GetMediaStorage()