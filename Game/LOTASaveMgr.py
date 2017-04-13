# TODO: Make this use a more secure and better format so its not just a txt with a number in it
# Possibly use json or use some file type that the data is non readable from

from direct.gui import *
from panda3d.core import *  
from direct.gui.DirectGui import *   
from direct.interval.IntervalGlobal import * 

class LOTASaveMgr:

    def __init__(self):
        self.saveFile = StreamReader(vfs.openReadFile('save.txt', 1), 1)
    
    def loadSaveData(self):
        self.lastScene = self.saveFile.readline()
        return self.lastScene
    
    def saveSaveData(self, scene = 'Introduction'):
        saveFile = open('save.txt','w')
        saveFile.write(scene)
        
        # Show a little visual to show that it's saving
        self.saveMsgBackground = OnscreenImage(image = "Resources/maps/tipBg.png")
        self.saveMsgBackground.setTransparency(TransparencyAttrib.MAlpha)
        self.saveMsgText = OnscreenText(text = 'Saving Game...')
        self.saveMsgText.reparentTo(self.saveMsgBackground)
        self.saveMsgBackground.hide()
        self.saveMsgBackground.reparentTo(base.a2dTopCenter)
        self.saveMsgBackground.setPos(0, 0, 1)
        self.saveMsgBackground.setScale(.2, .05, .05)
        self.saveMsgBackground.setColorScale(1, 1, 1, 0.5)
        self.saveMsgText.setScale(.2, .8)
        self.saveMsgSequence = Sequence(
            Func(self.saveMsgBackground.show),
            self.saveMsgBackground.posInterval(0.3, Point3(0, 0, -0.16)),
            self.saveMsgBackground.posInterval(0.2, Point3(0, 0, -0.13)),
            Wait(2),
            self.saveMsgBackground.posInterval(0.5, Point3(0, 0, 1)),
            Func(self.saveMsgBackground.hide))
        self.saveMsgSequence.start()
