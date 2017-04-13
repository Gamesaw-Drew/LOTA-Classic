from direct.gui.DirectButton import DirectButton
from direct.directbase import DirectStart  
from direct.gui.DirectGui import *   
from direct.interval.IntervalGlobal import * 
from direct.showbase import ShowBase
from panda3d.core import *
from Game import AmdLocalizerEnglish as Localizer
import os

def showText(self, text):
  self.text = OnscreenText(text = text, style=3, fg=(1,1,1,1), scale = 0.07, wordwrap = 30, parent=base.a2dBottomCenter, pos=(0, -1))
  self.text.show()
  self.textUpInterval = Sequence(
      self.text.posInterval(0.2, Point3(0, 0, 1.24)),
      self.text.posInterval(0.09, Point3(0, 0, 1.2)))
  self.textUpInterval.start()

def hideText(self):
  if self.text is not None:
      self.textDownInterval = Sequence(self.text.posInterval(.5, VBase3(0, 0, -1)), Func(self.text.hide))
      self.textDownInterval.start()
      
def showChatBubble(self, chatText, bubbleParent, bubbleX = 0, bubbleY = 0, bubbleZ = 0):
  self.chatBubble = None
  self.bubblePos = (bubbleX, bubbleY, bubbleZ)
  if self.chatBubble is None:
      self.chatBubble = OnscreenImage(image = "Resources/maps/chatbubble.png", parent=bubbleParent)
      self.chatBubble.setTransparency(TransparencyAttrib.MAlpha)
      self.chatBubble.setScale(.006, .006, .003)
      self.chatBubble.setPos(self.bubblePos)
      self.chatBubble.hide()
  self.chatBubbleText = OnscreenText(text = chatText, style=1, fg=(0,0,0,1), scale = 1, wordwrap = 15, pos=(0, .4))
  self.chatBubbleText.setScale(0.11, 0.25)
  self.chatBubbleText.show()
  self.chatBubbleText.reparentTo(self.chatBubble)
  self.chatBubble.show()
  self.bubbleUpInterval = Sequence(
    Sequence(
      self.chatBubble.scaleInterval(.2, VBase3(.72, .72, .36), blendType = 'easeInOut'),
      self.chatBubble.scaleInterval(.09, VBase3(.6, .6, .3), blendType = 'easeInOut')))
  self.bubbleUpInterval.start()

def hideChatBubble(self):
  if self.chatBubble is not None:
      self.bubbleDownInterval = Sequence(self.chatBubble.scaleInterval(.5, VBase3(.006, .006, .003)), Func(self.chatBubble.hide))
      self.bubbleDownInterval.start()
      
def showLocationText(self, text):
  self.locText = OnscreenText(text = text, style=3, fg=(1,1,1,1), scale = 0.08, wordwrap = 30, parent=base.a2dBottomCenter, pos=(0, .5))
  self.locText.setColorScale(1, 1, 1, 0)
  self.locText.show()
  self.locTextFadeIn = LerpColorScaleInterval(self.locText, 1, VBase4(1, 1, 1, 1), blendType = 'easeInOut')
  self.locTextFadeIn.start()

def hideLocText(self):
  if self.locText is not None:
      self.locTextFadeOut = Sequence(LerpColorScaleInterval(self.locText, 1, VBase4(1, 1, 1, 0), blendType = 'easeInOut'), Func(self.locText.hide))
      self.locTextFadeOut.start()
      
def showTip(self, tipMsg, tipDuration = 4):
    self.tipBackground = OnscreenImage(image = "Resources/maps/tipBg.png")
    self.tipBackground.setTransparency(TransparencyAttrib.MAlpha)
    self.tipText = OnscreenText(text = tipMsg)
    self.tipText.reparentTo(self.tipBackground)
    self.tipBackground.hide()
    self.tipBackground.reparentTo(base.a2dTopCenter)
    self.tipBackground.setPos(0, 0, 1)
    self.tipBackground.setScale(.4, .1, .1)
    self.tipText.setScale(.1, .4)
    self.tipSequence = Sequence(
        Func(self.tipBackground.show),
        self.tipBackground.posInterval(0.3, Point3(0, 0, -0.24)),
        self.tipBackground.posInterval(0.2, Point3(0, 0, -0.2)),
        Wait(tipDuration),
        self.tipBackground.posInterval(0.5, Point3(0, 0, 1)),
        Func(self.tipBackground.hide))
    self.tipSequence.start()
    
def saveGame(self, sceneNumber='1'):
    saveFile = open('save.txt','w')
    saveFile.write(sceneNumber)
    
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