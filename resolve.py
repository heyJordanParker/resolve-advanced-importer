import sys
import imp
import os
from init import resolvePath

def GetResolve():
    scriptModule = None
    try:
        import fusionscript as scriptModule
    except ImportError:
        # Look for an auto importer config path
        if resolvePath:
            try:
                scriptModule = imp.load_dynamic("fusionscript", resolvePath)
            except ImportError:
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
    
    
    # try:
    # # The PYTHONPATH needs to be set correctly for this import statement to work.
    # # An alternative is to import the DaVinciResolveScript by specifying absolute path (see ExceptionHandler logic)
    #     import DaVinciResolveScript as bmd
    # except (ImportError, FileNotFoundError) as e:
    #     try:
    #         bmd = imp.load_source('DaVinciResolveScript', str(resolvePath) + "DaVinciResolveScript.py")
    #     except (ImportError, FileNotFoundError) as e:
    #         # No fallbacks ... report error:
    #         print("Unable to find module DaVinciResolveScript - please ensure that the path in your config file is valid.")
    #         print("Based on your config file, the module is expected to be located in: " + str(resolvePath))
            
    #         if sys.platform.startswith("darwin"):
    #             expectedPath="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules/"
    #         elif sys.platform.startswith("win") or sys.platform.startswith("cygwin"):
    #             import os
    #             expectedPath=os.getenv('PROGRAMDATA') + "\\Blackmagic Design\\DaVinci Resolve\\Support\\Developer\\Scripting\\Modules\\"
    #             os.startfile(expectedPath)
    #         elif sys.platform.startswith("linux"):
    #             expectedPath="/opt/resolve/libs/Fusion/Modules/"

    #         # check if the default path has it...
    #         try:
    #             bmd = imp.load_source('DaVinciResolveScript', expectedPath+"DaVinciResolveScript.py")
    #         except (ImportError, FileNotFoundError) as e:
    #             # No fallbacks ... report error:
    #             print("Unable to find module DaVinciResolveScript - please ensure that the module DaVinciResolveScript is discoverable by python")
    #             print("For a default DaVinci Resolve installation, the module is expected to be located in: " + expectedPath)
    #             sys.exit()

resolve = GetResolve()
projectManager = resolve.GetProjectManager()
project = projectManager.GetCurrentProject()
mediaPool = project.GetMediaPool()
mediaStorage = resolve.GetMediaStorage()