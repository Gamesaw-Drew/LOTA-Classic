# TLOTTO MAIN MENU:
# MAIN MENU FUNCTIONS
# We want to keep the mainmenuscreen file cleaner so we wont put the functionality in there, we put it in here

from direct.gui.DirectGui import OnscreenImage, OnscreenText, DirectButton
from panda3d.core import TransparencyAttrib, Point3, Vec4, Vec3, TextNode
from direct.interval.IntervalGlobal import LerpPosInterval, Wait, Func, Sequence, LerpColorScaleInterval, LerpScaleInterval, Interval
from direct.showbase.DirectObject import DirectObject
from toontown.toonbase import TTLocalizer, ToontownGlobals
from toontown.ttrigui.OptionsScreen import OptionsScreen
from toontown.mainmenu.MainMenuScreen import MainMenuScreen

class MainMenuFunctions:
    notify = directNotify.newCategory('TTRI_MAIN_MENU_FUNCTIONS')
    
    def __init__(self):
        pass
        
    def openOptions(self):
        pass
    
    def hideOptions(self):
        pass
        
    def enterAvChooser(self):
        if self.fadeToAvChooser is not None:
            self.fadeToAvChooser.finish()
            self.fadeToAvChooser = None
        self.fadeToAvChooser = base.transitions.getFadeOutIval(t=1)

        Sequence(
            Func(self.fadeTrack.start),
            Wait(1),
            Func(MainMenuScreen.murder),
            Func(base.cr.loginFSM.request, 'chooseAvatar', [base.cr.avList]),
            Func(base.transitions.fadeIn, 1)).start()
        
    def useLastPlayedToon(self, lastToon = None):
        pass
        
    def quitGame(self):
        self.doneStatus = {'mode': 'exit'}
        messenger.send(self.doneEvent, [self.doneStatus])