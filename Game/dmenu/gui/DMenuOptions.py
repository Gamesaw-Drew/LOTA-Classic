'''
Created on Apr 2, 2016

@author: Drew

# TODO: Make the Options screen a more 3d interactive screen, so it doesnt look 2d, and so it is inside of the HQ building
# Also do the same for Pick-A-Toon

'''

from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import Wait, Func, Sequence, LerpColorScaleInterval, Parallel, LerpScaleInterval
from direct.showbase.DirectObject import DirectObject
from panda3d.core import TransparencyAttrib, Point3, Vec3, Vec4, TextNode

from Game.dmenu import DMenuLocalizer
from Game.dmenu import DMenuResources
#from toontown.toonbase import TTLocalizer
#from toontown.toonbase import ToontownGlobals
#from toontown.toontowngui.TTGui import btnDn, btnRlvr, btnUp
#from toontown.toontowngui import TTDialog

resolution_table = [
    (800, 600),
    (1024, 768),
    (1280, 1024),
    (1600, 1200),
    (1280, 720),
    (1920, 1080)]

AspectRatios = [
              0,
             1.33333,
             1.77777 ]

class DMenuOptions:

    def __init__(self):
        self.optionsOpenSfx = base.loadSfx(DMenuResources.Settings_Open)
        self.optionsCloseSfx = base.loadSfx(DMenuResources.Settings_Close)

    def showOptions(self):
        base.playSfx(self.optionsOpenSfx)
        self.displayOptions()
        zoomIn = (LerpScaleInterval(self.optionsNode, .4, Vec3(1, 1, 1), Vec3(0, 0, 0), blendType = 'easeInOut')).start()

    def hideOptions(self):
        base.playSfx(self.optionsCloseSfx)
        zoomOut = (LerpScaleInterval(self.optionsNode, .4, Vec3(0, 0, 0), Vec3(1, 1, 1), blendType = 'easeInOut')).start()
        Sequence (
        Wait(.4),
        Func(self.delOptions)).start()

    def displayOptions(self):
        self.optionsNode = aspect2d.attachNewNode('optionsNode')
        self.optionsNode.reparentTo(aspect2d)


        #gui = loader.loadModel('phase_3/models/gui/pick_a_toon_gui')
        #guiButton = loader.loadModel('phase_3/models/gui/quit_button')
        #quitHover = gui.find('**/QuitBtn_RLVR')


        self.optionsBox = OnscreenImage(image = 'Resources/maps/button.jpg')
        self.optionsBox.setTransparency(TransparencyAttrib.MAlpha)
        self.optionsBox.setPos(0, 0, 0)
        self.optionsBox.setScale(0.7)
        self.optionsBox.reparentTo(self.optionsNode)
        # Music Label

    def delOptions(self):
        self.optionsBox.hide()
        del self.optionsBox
        self.optionsNode.removeNode()
        del self.optionsNode
