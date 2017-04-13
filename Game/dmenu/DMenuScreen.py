# DMENU VERSION 0.2

from direct.gui.DirectGui import OnscreenImage, DirectButton
from panda3d.core import TransparencyAttrib, Point3, VBase3, Vec4
from direct.interval.IntervalGlobal import Wait, Func, Sequence, LerpColorScaleInterval, Parallel, LerpFunctionInterval
from direct.showbase.DirectObject import DirectObject
import DMenuResources
import DMenuLocalizer
from gui import DMenuOptions
from gui import DMenuQuit

# TT
#from toontown.login import AvatarChooser
#from toontown.toontowngui.TTGui import btnDn, btnRlvr, btnUp
#from toontown.toonbase import TTLocalizer
#from toontown.hood import SkyUtil
from DMenuGlobals import *

# The camera's initial position when first entering main menu
INIT_POS = (-120, 1, 120)
INIT_HPR = (-90, -60, 0)

# The main position
MAIN_POS = (-60, 1, 10)
MAIN_HPR = (-90, 5, 0)

# To be used when entering PAT
TOON_HALL_POS = (110, 1, 8)
TOON_HALL_HPR = (-90, 0, 0)

# To be used when going to menu
HQ_POS = (14, 16, 8)
HQ_HPR = (-48, 0, 0)

#LOTA
from Game import LoadResources as Resources
from Game import LOTASaveMgr
from Game import AmdLocalizerEnglish

class DMenuScreen(DirectObject):
    notify = directNotify.newCategory('DMenuScreen')

    def __init__(self):#, avatarList, parentFSM, doneEvent):
        DirectObject.__init__(self)
        base.disableMouse()
        #base.cr.avChoice = None
        fadeSequence = Sequence(
            Wait(.5),
            Func(base.transitions.fadeIn, .5),
            Wait(1)).start()#,
            #base.camera.posHprInterval(1, Point3(MAIN_POS), VBase3(MAIN_HPR), blendType = 'easeInOut')).start()
        #self.background = loader.loadModel('phase_4/models/neighborhoods/toontown_central_full')
        #self.background.reparentTo(render)
        #for frame in render.findAllMatches('*/doorFrame*'):
        #    frame.removeNode()
        #self.sky = loader.loadModel('phase_3.5/models/props/TT_sky')
        #SkyUtil.startCloudSky(self)

        #base.camera.setPosHpr(INIT_POS, INIT_HPR)
        self.background = OnscreenImage(image = DMenuResources.MenuBackground, parent = aspect2d)
        self.background.setBin('background', 1)
        self.background.reparentTo(aspect2d)
        self.background.setScale(2, 1, 1)
        
        self.logo = OnscreenImage(image = DMenuResources.GameLogo, scale = (1, 1, .5))
        self.logo.reparentTo(aspect2d)
        self.logo.setTransparency(TransparencyAttrib.MAlpha)
        scale = self.logo.getScale()
        self.logo.setPos(0, 0, .5)
        self.logo.setColorScale(Vec4(0, 0, 0, 0))

        #fadeInBackground = (LerpColorScaleInterval(self.background, 1, Vec4(1, 1, 1, 1), Vec4(1, 1, 1, 0))).start()
        fadeInLogo = (LerpColorScaleInterval(self.logo, 1, Vec4(1, 1, 1, 1), Vec4(1, 1, 1, 0))).start()

        self.createButtons()

        self.fadeOut = None
        self.optionsMgr = DMenuOptions.DMenuOptions()
        self.quitConfirmation = DMenuQuit.DMenuQuit()

        # TT: We need these to run the Pick A Toon screen
        #self.patAvList = avatarList
        #self.patFSM = parentFSM
        #self.patDoneEvent = doneEvent
        
        self.transcircle = Resources.transcircle
        self.transcircle.setTransparency(TransparencyAttrib.MAlpha)
        self.transcircle.setScale(VBase3(0.01, 0.01, 0.01))
        self.transcircle.setBin('background', 3)
        
        self.savemgr = LOTASaveMgr.LOTASaveMgr()
        
        # Get the save data
        self.savePos = self.savemgr.loadSaveData()
        
        self.titleMusic = Resources.titleMusic
        self.titleMusic.setLoop(1)
        self.setMusicNormal()

    def skyTrack(self, task):
    #    return SkyUtil.cloudSkyTrack(task)
        pass

    def createButtons(self):
        self.PlayButton = DirectButton(relief = None, text_style = 3, text_fg = (1, 1, 1, 1), text = DMenuLocalizer.PlayGame, text_scale = .1, scale = 0.95, command = self.playGame)
        self.PlayButton.reparentTo(aspect2d)
        self.PlayButton.setPos(PlayBtnHidePos)
        self.PlayButton.show()

        self.OptionsButton = DirectButton(relief = None, text_style = 3, text_fg = (1, 1, 1, 1), text = DMenuLocalizer.Options, text_scale = .1, scale = 0.95, command = self.openOptions)
        self.OptionsButton.reparentTo(aspect2d)
        self.OptionsButton.setPos(OptionsBtnHidePos)
        self.OptionsButton.show()

        self.QuitButton = DirectButton(relief = None, text_style = 3, text_fg = (1, 1, 1, 1), text = DMenuLocalizer.Quit, text_scale = .1, scale = 0.95, command = self.quitGame)
        self.QuitButton.reparentTo(aspect2d)
        self.QuitButton.setPos(QuitBtnHidePos)
        self.QuitButton.show()


        # self.BRButton = DirectButton(text = 'REPORT BUG', text_scale = .1, scale=0.95)
        # self.BRButton.reparentTo(aspect2d)
        # self.BRButton.setPos(-.9, 0, -.9)
        # self.BRButton.show()
        
        self.buttonInAnimation()
        
        # Slap on the saves menu from the old main menu until a proper implementation to DMENU is made
        self.SavesButton = DirectButton(relief = None, text = AmdLocalizerEnglish.LOTA_SAVES, image_scale = 2, text_scale = .1, scale = 0.95, command = self.openSavesMenu)
        self.SavesButton.reparentTo(aspect2d)
        self.SavesButton.setPos(0, 0, -.5)
        self.SavesButton.show()

    def murder(self):
        if self.logo is not None:
            self.logo.destroy()
            self.logo = None

        if self.background is not None:
            self.background.hide()
            self.background.reparentTo(hidden)
            self.background.removeNode()
            self.background = None

        if self.PlayButton is not None:
            self.PlayButton.destroy()
            self.PlayButton = None

        if self.OptionsButton is not None:
            self.OptionsButton.destroy()
            self.OptionsButton = None

        if self.QuitButton is not None:
            self.QuitButton.destroy()
            self.QuitButton = None
            
        if self.SavesButton is not None:
            self.SavesButton.destroy()
            self.SavesButton = None
            
        if self.titleMusic is not None:
            self.titleMusic.stop()

        #taskMgr.remove('skyTrack')
        #self.sky.reparentTo(hidden)

    def openOptions(self):
        self.optionsMgr.showOptions()
        self.closeOptionsButton = DirectButton(relief = None, text = "< Back", text_fg = (0.977, 0.816, 0.133, 1), text_pos = (0, -0.035), scale = .1, command = self.hideOptions)
        self.closeOptionsButton.reparentTo(base.a2dTopLeft)
        self.closeOptionsButton.setPos(0.5, 0, -0.07)
        Parallel(
            self.PlayButton.posInterval(.5, Point3(PlayBtnHidePos), blendType = 'easeInOut'),
            self.OptionsButton.posInterval(.5, Point3(OptionsBtnHidePos), blendType = 'easeInOut'),
            self.QuitButton.posInterval(.5, Point3(QuitBtnHidePos), blendType = 'easeInOut'),
            self.logo.posInterval(0.5, Point3(0, 0, 2.5), blendType = 'easeInOut')).start()
        #base.camera.posHprInterval(0.5, Point3(HQ_POS), VBase3(HQ_HPR), blendType = 'easeInOut').start()
        #self.setMusicCalm()

    def hideOptions(self):
        self.optionsMgr.hideOptions()
        self.closeOptionsButton.hide()
        Parallel(
            self.PlayButton.posInterval(.5, Point3(PlayBtnPos), blendType = 'easeInOut'),
            self.OptionsButton.posInterval(.5, Point3(OptionsBtnPos), blendType = 'easeInOut'),
            self.QuitButton.posInterval(.5, Point3(QuitBtnPos), blendType = 'easeInOut'),
            self.logo.posInterval(.5, Point3(0, 0, .5), blendType = 'easeInOut')).start()
        base.camera.posHprInterval(0.5, Point3(MAIN_POS), VBase3(MAIN_HPR), blendType = 'easeInOut').start()
        #self.setMusicNormal()

    def playGame(self):
        if self.fadeOut is not None:
            self.fadeOut.finish()
            self.fadeOut = None
        self.fadeOut = base.transitions.getFadeOutIval(t = 1)
        #base.camera.posHprInterval(1, Point3(TOON_HALL_POS), VBase3(TOON_HALL_HPR), blendType = 'easeInOut').start()
        Sequence(
            Func(self.doPlayButton),
            #Func(self.fadeOut.start),
            Wait(1),
            Func(self.murder),
            Wait(1),
            Func(self.enterGame)).start()#,
            #Func(base.transitions.fadeIn, 1)).start()

    def enterOptions(self):
        pass

    def enterGame(self):
        #base.cr.avChoice = AvatarChooser.AvatarChooser(self.patAvList, self.patFSM, self.patDoneEvent)
        #base.cr.avChoice.load(1)
        #base.cr.avChoice.enter()
        from Game.NewGame.Scenes import SceneOne
        # Hamburger Menu Button
        #self.hbButton = DirectButton(image = "phase_3/maps/dmenu/dmhbmenu.png", relief = None, text = ' ', command=self.showHamburgerMenu)
        #self.hbButton.reparentTo(base.a2dTopLeft)
        #self.hbButton.setPos(0.05, 0, -0.05)
        #self.hbButton.setScale(0.04)

        # Hamburger Menu Hide Button
        #self.hbHideButton = DirectButton(image = "phase_3/maps/dmenu/close_window.png", relief = None, text = ' ', command=self.hideHamburgerMenu)
        #self.hbHideButton.reparentTo(base.a2dTopLeft)
        #self.hbHideButton.setPos(0.05, 0, -0.05)
        #self.hbHideButton.setScale(0.04)
        #self.hbHideButton.hide()

        # TODO: Add options and stuff to the hamburger menu

    def doPlayButton(self):
        Parallel(
            self.PlayButton.posInterval(1, Point3(PlayBtnHidePos), blendType = 'easeInOut'),
            self.OptionsButton.posInterval(1, Point3(OptionsBtnHidePos), blendType = 'easeInOut'),
            self.QuitButton.posInterval(1, Point3(QuitBtnHidePos), blendType = 'easeInOut'),
            self.logo.posInterval(0.5, Point3(0, 0, 2.5), blendType = 'easeInOut')).start()

    def quitGame(self):
        self.showQuitConfirmation()

    def showQuitConfirmation(self):
        self.quitConfirmation.showConfirmation()
        #base.exitFunc()

    def setMusicNormal(self):
        #LerpFunctionInterval(base.cr.music.setVolume, fromData = 0, toData = .9, duration = 1).start()
        #LerpFunctionInterval(base.cr.musicCalm.setVolume, fromData = .9, toData = 0, duration = 1).start()
        self.titleMusic.play()

    def setMusicCalm(self):
        LerpFunctionInterval(base.cr.music.setVolume, fromData = .9, toData = 0, duration = 1).start()
        LerpFunctionInterval(base.cr.musicCalm.setVolume, fromData = 0, toData = .9, duration = 1).start()

    def openSavesMenu(self):
        self.saveOne = DirectButton(relief=None, text = 'Save One: ' + '(Scene ' + str(self.savePos) + ')', scale=0.3, command=self.saveLoader, parent=aspect2d, pos=(0, 0, -.6), text_scale = .5)
        self.saveOne.hide()
        self.transcircle.show()
        self.exitLoadButton = DirectButton(relief=None, text = '< Back', scale=0.3, command=self.closeSavesMenu, parent=base.a2dBottomCenter, pos=(0, 0, -.4), text_scale = .5)
        self.exitLoadButton.show()

        
        self.openSavesMenuSequence = Parallel(
            self.transcircle.scaleInterval(0.5, VBase3(3, 3, 3), blendType = 'easeInOut'),
            self.exitLoadButton.posInterval(0.5, Point3(0, 0, .4), blendType = 'easeInOut'),
            Func(self.saveOne.show),
            self.saveOne.posInterval(0.5, Point3(0, 0, .2), blendType = 'easeInOut'))
        self.openSavesMenuSequence.start()
        
    def closeSavesMenu(self):
        self.hideThings = Sequence(
            Wait(0.5),
            Func(self.saveOne.hide),
            Func(self.transcircle.hide))
    
        self.closeSavesMenuSequence = Parallel(
            self.saveOne.posInterval(0.5, Point3(0, 0, -.6), blendType = 'easeInOut'),
            self.transcircle.scaleInterval(0.5, VBase3(0.01, 0.01, 0.01), blendType = 'easeInOut'),
            self.exitLoadButton.posInterval(0.5, Point3(0, 0, -.4), blendType = 'easeInOut'),
            Func(self.hideThings.start))
        self.closeSavesMenuSequence.start()
        self.exitLoadButton.removeNode()
        del self.exitLoadButton
        
    def saveLoader(self):
        # this was thrown together in like 10 seconds. how the fuck does this work
        # TODO: Make this save to a file thats not easily editable
        self.saveOne.hide()
        self.background.hide()
        self.transcircle.hide()
        if self.savePos == '1':
            from Game.NewGame.Scenes import SceneOne
        elif self.savePos == '2':
            from Game import SceneTwo
        elif self.savePos == '3':
            from Game import SceneThree
        elif self.savePos == '4':
            from Game import SceneFour
        elif self.savePos == '5':
            from Game import SceneFive
        else:
            print ("\n\n Save data is set to an unknown scene!!\n\n")
            
    def buttonInAnimation(self):
        logo = self.logo.posInterval(.5, Point3(0, 0, .5), blendType = 'easeInOut')
        play = self.PlayButton.posInterval(.5, Point3(PlayBtnPos), blendType = 'easeInOut')
        opt = self.OptionsButton.posInterval(.5, Point3(OptionsBtnPos), blendType = 'easeInOut')
        quit = self.QuitButton.posInterval(.5, Point3(QuitBtnPos), blendType = 'easeInOut')
        
        Sequence(
                 Func(logo.start),
                 Wait(0.1),
                 Func(play.start),
                 Wait(0.2),
                 Func(opt.start),
                 Wait(0.2),
                 Func(quit.start)).start()
                 
    def showHamburgerMenu(self):
        self.hbButton.hide()
        self.hbHideButton.show()
        
    def hideHamburgerMenu(self):
        self.hbButton.show()
        self.hbHideButton.hide()