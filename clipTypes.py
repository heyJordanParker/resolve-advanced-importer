from enum import Enum

class ResolveClipTypes(Enum):
    Video = "Video"
    Audio = "Audio"
    VideoAudio = "Video + Audio"
    Still = "Still"
    Multicam = "Multicam"
    Timeline = "Timeline"
    Compound = "Compound"
    Matte = "Matte"
    RefClip = "Ref Clip"
    Stereo = "Stereo"
    VFXConnect = "VFX Connect"
    Generator = "Generator"
    Fusion = "Fusion"
    
    def isAnyType(clip, *types):
        for type in types:
            if(clip.GetClipProperty("Type") == type.value):
                return True
            
        return False
    
    def getImportedTypes():
        return [ResolveClipTypes.Video, ResolveClipTypes.Audio, ResolveClipTypes.VideoAudio, ResolveClipTypes.Still]
    
    def isImported(clip):
        return ResolveClipTypes.isAnyType(clip, *ResolveClipTypes.getImportedTypes())