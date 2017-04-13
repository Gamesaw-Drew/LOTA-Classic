## Title Screen ##

# TODO: Make this not look like cancer, add better textures and animations

from panda3d.core import *  
loadPrcFile("Config.prc")
vfs = VirtualFileSystem.getGlobalPtr()
vfs.mount(Filename("Resources.mf"), "", VirtualFileSystem.MFReadOnly)
from direct.gui import *
from direct.directbase import DirectStart
from direct.gui.DirectGui import *   
from direct.interval.IntervalGlobal import * 
from direct.showbase import ShowBase
from panda3d.core import loadPrcFileData
from panda3d.core import loadPrcFile
from panda3d.core import WindowProperties
from Game import LoadResources as Resources
from Game import LOTASaveMgr
import sys
props = WindowProperties()
props.setTitle('Legend of the AMD Alpha B100616')
base.win.requestProperties(props)
from Game.dmenu import DMenuScreen

class GameStart:
    def __init__(self):
        self.savemgr = LOTASaveMgr.LOTASaveMgr()
        
        # Get the save data
        self.savePos = self.savemgr.loadSaveData()

        self.buttonImage = ("Resources/maps/button.jpg")
        
        self.GameFont = Resources.GameFont
    
        self.title = OnscreenText(
          text="ALPHA",
          style=3, fg=(1,1,1,1), pos=(-0.02, 0.07), scale = .07, parent=base.a2dBottomRight, align=TextNode.ARight)
        self.startButton = DirectButton(relief=None, text = 'New\nGame', scale=0.3, command=self.startGame, parent=base.a2dBottomCenter, pos=(-.4, 0, .6), text_scale = .5, text_font = self.GameFont, image = self.buttonImage)
        self.startButton.hide()
        self.loadButton = DirectButton(relief=None, text = 'Load\nSave', scale=0.3, command=self.openSavesMenu, parent=base.a2dBottomCenter, pos=(.4, 0, .6), text_scale = .5, text_font = self.GameFont, image = self.buttonImage)
        self.loadButton.hide()
        self.presents = OnscreenText(text = "DREW", style = 3, fg = (1, 1, 1, 1), scale = 0.07, wordwrap = 30, parent = aspect2d)
        self.agameabout = OnscreenText(text = "Made with Panda3D", style = 3, fg = (1, 1, 1, 1), scale = 0.07, wordwrap = 30, parent = aspect2d)
        self.dmenuLoading = OnscreenText(text = "Loading DMenu V0.2", style = 3, fg = (1, 1, 1, 1), scale = 0.07, wordwrap = 30, parent = aspect2d)
        self.dmenuLoading.hide()
        self.logo = Resources.logo
        self.logo.setTransparency(TransparencyAttrib.MAlpha)
        self.logo.setScale(0.005, 0.005, 0.003)
        self.logo.hide()
        self.agameabout.hide()
        self.presents.hide()
        
        self.startPos = Sequence(
            self.startButton.posInterval(.5, Point3(-.4, 0, .6), blendType = 'easeInOut'))

        self.loadButtonPos = Sequence(
            self.loadButton.posInterval(.5, Point3(.4, 0, .6), blendType = 'easeInOut'))

        self.introductionSequence = Sequence(
            Func(self.presents.show),
            Func(base.transitions.fadeIn, .5),
            Wait(2),
            Func(base.transitions.fadeOut, .5),
            Func(self.presents.hide),
            Wait(.5),
            Func(self.agameabout.show),
            Func(base.transitions.fadeIn, .5),
            Wait(2),
            Func(base.transitions.fadeOut, .5),
            Func(self.agameabout.hide),
            Wait(.5),
            Func(self.logo.show),
            Func(base.transitions.fadeIn, .5),
            LerpScaleInterval(self.logo, 1, VBase3(0.5, 0.5, 0.3), blendType = 'easeInOut'),
            Wait(2),
            Func(self.logo.hide),
            Func(base.transitions.fadeOut, .5),
            Wait(.5),
            Func(base.transitions.fadeIn, .5),
            Wait(.4),
            Func(self.dmenuLoading.show),
            Wait(.1),
            Func(self.dmenuLoading.hide),
            Func(self.startNewMenu))
            
        self.introductionSequence.start()
        textRowHeight = 0.145
        leftMargin = -0.72
        buttonbase_xcoord = 0.35
        buttonbase_ycoord = 0.45
        button_image_scale = (0.7, 1, 1)
        button_textpos = (0, -0.02)
        self.defaultMusicVol = 1
        self.Music_toggleSlider = DirectSlider(parent=base.a2dBottomCenter, pos=(0, 0, .8),
                                               value=self.defaultMusicVol*100, pageSize=5, range=(0, 100), command=self.__doMusicLevel)
        self.Music_toggleSlider.setScale(0.3)
        self.Music_toggleSlider.hide()
        
        self.exitLoadButton = DirectButton(relief=None, text = '< Back', scale=0.3, command=self.closeSavesMenu, parent=base.a2dBottomCenter, pos=(0, 0, -.4), text_scale = .5, text_font = self.GameFont)
        self.exitLoadButton.hide()

    def startGame(self):
        self.startGame = Sequence(
            Sequence(
                Func(self.fadeOutMusic),
                Func(self.startButton.hide),
                Func(self.loadButton.hide),
                Func(self.logo.hide),
                Func(self.titleMusic.stop),
                Func(self.startGameImport)))
        self.startGame.start()

    def loadGame(self):
        self.loadGame = Sequence(
            Sequence(
                Func(self.fadeOutMusic),
                Func(self.startButton.hide),
                Func(self.loadButton.hide),
                Func(self.logo.hide),
                Func(self.titleMusic.stop),
                Func(self.saveLoader)))
        self.loadGame.start()

    def openSavesMenu(self):
        self.saveOne = DirectButton(relief=None, text = 'Save One: ' + '(Scene ' + str(self.savePos) + ')', scale=0.3, command=self.loadGame, parent=aspect2d, pos=(0, 0, -.6), text_scale = .5, text_font = self.GameFont)
        self.saveOne.hide()
        self.transcircle.show()
        
        self.openSavesMenuSequence = Parallel(
            self.transcircle.scaleInterval(0.5, VBase3(3, 3, 3), blendType = 'easeInOut'),
            Func(self.loadButton.hide),
            Func(self.exitLoadButton.show),
            Func(self.saveOne.show),
            self.exitLoadButton.posInterval(0.5, Point3(0, 0, .4), blendType = 'easeInOut'),
            self.startButton.posInterval(0.5, Point3(-.4, 0, -.6), blendType = 'easeInOut'),
            self.logo.posHprScaleInterval(0.5, Point3(0, 0, .6), VBase3(0, 0, 0), VBase3(0.25, 0.25, 0.15), blendType = 'easeInOut'),
            self.saveOne.posInterval(0.5, Point3(0, 0, .2), blendType = 'easeInOut'))
        self.openSavesMenuSequence.start()
        
    def closeSavesMenu(self):
        self.hideThings = Sequence(
            Wait(0.5),
            Func(self.exitLoadButton.hide),
            Func(self.saveOne.hide),
            Func(self.transcircle.hide),
            Func(self.loadButton.show))
    
        self.closeSavesMenuSequence = Parallel(
            self.logo.posHprScaleInterval(0.5, Point3(0, 0, .5), VBase3(0, 0, 0), VBase3(0.5, 0.5, 0.3), blendType = 'easeInOut'),
            self.saveOne.posInterval(0.5, Point3(0, 0, -.6), blendType = 'easeInOut'),
            Func(self.startButton.show),
            self.startButton.posInterval(0.5, Point3(-.4, 0, .6), blendType = 'easeInOut'),
            self.exitLoadButton.posInterval(0.5, Point3(0, 0, -0.4), blendType = 'easeInOut'),
            self.transcircle.scaleInterval(0.5, VBase3(0.01, 0.01, 0.01), blendType = 'easeInOut'),
            Func(self.hideThings.start))
        self.closeSavesMenuSequence.start()

    def __doMusicLevel(self):
        vol = self.Music_toggleSlider['value']
        vol = float(vol) / 100
        base.musicManager.setVolume(vol)
        base.musicActive = vol > 0.0

    def getGameFont():
        global GameFont
        if GameFont == None:
            GameFont = loader.loadFont(self.roboto, lineHeight=1.0)
        return GameFont

    def fadeOutMusic(self):
        curVol = self.titleMusic.getVolume()
        self.musicFade = Sequence(LerpFunctionInterval(self.titleMusic.setVolume, fromData=curVol, toData=0, duration=1))
        self.musicFade.start()
        
    def startGameImport(self):
        from Game.NewGame.Scenes import SceneOne

    def saveLoader(self):
        # this was thrown together in like 10 seconds. how the fuck does this work
        # TODO: Make this save to a file thats not easily editable
        self.saveOne.hide()
        self.exitLoadButton.hide()
        self.transcircle.hide()
        if self.savePos == '1':
            from Game.NewGame.Scenes import SceneOne
        else:
            print ("\n\n Save data is set to an unknown scene!!\n\n")
        
        
    def startNewMenu(self):
        self.startButton.show()
        self.loadButton.show()
        self.createPipeline()
        
        # Slap DMENU on over the old menu
        DMenuScreen.DMenuScreen()
        if self.startButton:
            self.startButton.removeNode()
            del self.startButton
        if self.loadButton:
            self.loadButton.removeNode()
            del self.loadButton
            
    def createPipeline(self):
        #sys.path.insert(0, "renderPipeline")
        #from rpcore import RenderPipeline, SpotLight
        
        # Create the rendering pipeline for beautiful graphics - it wont work with the game compiled tho
        #self.renderPipeline = RenderPipeline()
        #self.renderPipeline.pre_showbase_init()
        #self.renderPipeline.create(base)
        
        # Create some lighting
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor(Vec4(.5, .5, .5, 1))
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection(Vec3(-5, -5, -5))
        directionalLight.setColor(Vec4(.8, .8, .8, 1))
        directionalLight.setSpecularColor(Vec4(.8, .8, .8, 1))
        render.setLight(render.attachNewNode(ambientLight))
        render.setLight(render.attachNewNode(directionalLight))

w = GameStart()
base.run()
