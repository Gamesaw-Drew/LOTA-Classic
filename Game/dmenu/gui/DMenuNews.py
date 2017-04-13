'''
Created on May 1, 2016

@author: Drew

Updates and news will be shown on this screen
'''

from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import Wait, Func, Sequence, LerpColorScaleInterval, Parallel, LerpScaleInterval
from direct.showbase.DirectObject import DirectObject
from panda3d.core import TransparencyAttrib, Point3, Vec4

from toontown.dmenu import DMenuLocalizer
from toontown.dmenu import DMenuResources
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from toontown.toontowngui.TTGui import btnDn, btnRlvr, btnUp
from toontown.toontowngui import TTDialog

class DMenuNews:

    def __init__(self):
        self.newsOpenSfx = base.loadSfx(DMenuResources.Settings_Open)
        self.newsCloseSfx = base.loadSfx(DMenuResources.Settings_Close)

    def showNews(self):
        base.playSfx(self.newsOpenSfx)
        self.displayNews()
        zoomIn = (LerpScaleInterval(self.newsNode, .4, Vec3(1, 1, 1), Vec3(0, 0, 0), blendType = 'easeInOut')).start()

    def hideNews(self):
        base.playSfx(self.newsCloseSfx)
        zoomOut = (LerpScaleInterval(self.newsNode, .4, Vec3(0, 0, 0), Vec3(1, 1, 1), blendType = 'easeInOut')).start()
        Sequence (
        Wait(.4),
        Func(self.delNews)).start()
