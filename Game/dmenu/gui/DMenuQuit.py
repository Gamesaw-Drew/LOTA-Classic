'''
Created on May 1, 2016

@author: Drew
'''

from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import Wait, Func, Sequence, LerpColorScaleInterval, Parallel, LerpScaleInterval
from direct.showbase.DirectObject import DirectObject
from panda3d.core import TransparencyAttrib, Point3, Vec4, TextNode

from Game.dmenu import DMenuLocalizer
from Game.dmenu import DMenuResources
import sys


#from toontown.toonbase import TTLocalizer
#from toontown.toonbase import ToontownGlobals
#from toontown.toontowngui.TTGui import btnDn, btnRlvr, btnUp
#from toontown.toontowngui import TTDialog
class DMenuQuit:
    
    def __init__(self):
        pass
    
    def showConfirmation(self):
        self.confNode = aspect2d.attachNewNode('confNode')
        self.confNode.reparentTo(aspect2d)

        self.confBox = OnscreenImage(image = 'Resources/maps/button.jpg', scale = 0.5)
        #self.confBox.setTransparency(TransparencyAttrib.MAlpha)
        self.confBox.reparentTo(self.confNode)
        self.confBox.setPos(0, 0, 0)
        self.confBox.setScale(0.4)
        
        self.ask = DirectLabel(parent = self.confNode, relief = None, text = 'Are you sure you want to quit?', text_align = TextNode.ACenter, text_scale = 0.052, pos = (0, 0, .5))
        self.yes = DirectButton(parent = self.confNode, relief = None, text = "yes", text_align = TextNode.ACenter, text_scale = .1, scale = 0.95, command = self.acceptQuit)
        self.yes.setPos(0, 0, -.2)
        self.yes.show()
        
        # Temp:
        #self.acceptQuit()
        
    def acceptQuit(self):
        sys.exit()