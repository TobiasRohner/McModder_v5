# -*- coding: utf-8 -*-
from source import SrcModInfo




class ModInfo():
    
    
    def __init__(self, name):
        
        self.modid          = name.replace(" ", "_")
        self.name           = name
        self.description    = ""
        self.version        = "1.0"
        self.mcversion      = "1.8"
        self.url            = ""
        self.updateUrl      = ""
        self.authorList     = []
        self.credits        = ""
        self.logoFile       = ""
        self.screenshots    = []
        self.dependencies   = []
        
        
    def generateSrc(self):
        
        src = SrcModInfo.main
        
        src = src.replace("<modid>"       , self.modid                )
        src = src.replace("<name>"        , self.name                 )
        src = src.replace("<description>" , self.description          )
        src = src.replace("<version>"     , self.version              )
        src = src.replace("<mcversion>"   , self.mcversion            )
        src = src.replace("<url>"         , self.url                  )
        src = src.replace("<updateUrl>"   , self.updateUrl            )
        src = src.replace("<authorList>"  , ",".join(self.authorList) )
        src = src.replace("<credits>"     , self.credits              )
        src = src.replace("<logoFile>"    , self.logoFile             )
        src = src.replace("<screenshots>" , ",".join(self.screenshots))
        src = src.replace("<dependencies>", ",".join(self.modid)      )
        
        return src