from direct.gui.DirectButton import DirectButton
from direct.directbase import DirectStart  
from direct.gui.DirectGui import *   
from direct.interval.IntervalGlobal import * 
from direct.showbase import ShowBase
from panda3d.core import *
import AmdLocalizerEnglish as Localizer
import os
import Globals
from Game import LoadResources as Resources
# Introduction to the story

class GameStart:

    def __init__(self):
        Globals.saveGame(self, '1')
    
        self.music = Resources.bgMusic
        self.music.setLoop(1)
        self.music.play()
        self.amdCard = Resources.amdCard
        self.amdCard.setTransparency(TransparencyAttrib.MAlpha)
        self.amdCard.setScale(1, 1, .9)
        self.amdCard.hide()
        self.amdCard.setColorScale(1, 1, 1, 0)
        self.amdCard.setBin('background', 2)
        self.amdHq = Resources.amdHq
        self.amdHq.setScale(1.33, 1, 1)
        self.amdHq.setBin('background', 2)
        self.amdHq.setColorScale(1, 1, 1, 0)
        self.amdHq.hide()
        self.saul = Resources.saul
        self.saul.setTransparency(TransparencyAttrib.MAlpha)
        self.saul.setScale(.5, .5, .5)
        self.saul.setColorScale(1, 1, 1, 0)
        self.saul.setPos(-.5, 0, 0)
        self.saul.hide()
        self.boss = Resources.boss
        self.boss.setTransparency(TransparencyAttrib.MAlpha)
        self.boss.setScale(.5, .5, .5)
        self.boss.setColorScale(1, 1, 1, 0)
        self.boss.setPos(.5, 0, 0)
        self.boss.hide()
        self.sip1 = Resources.sip1
        self.sip2 = Resources.sip2
        self.cardQuestion = Resources.cardQuestion
        self.cardAnswer = Resources.cardAnswer
        self.errorSnd = Resources.errorSnd
        self.errorMsg = Resources.errorMsg
        self.errorMsg.setTransparency(TransparencyAttrib.MAlpha)
        self.errorOkButton = DirectButton(relief=None, text = 'OK', scale=0.2, command=self.nextScene, parent=self.errorMsg, pos=(.6, 0, -.9), text_scale = .3)
        self.errorOkButton.setScale(.6, 1, 1)
        self.errorMsg.setScale(0.004, 0.0014, 0.0014)
        self.errorMsg.hide()

        self.errorSequence = Sequence(
            Func(self.errorMsg.show),
            Func(self.errorSnd.play),
            self.errorMsg.scaleInterval(0.2, VBase3(.4, .15, .15), blendType = 'easeInOut'),
            Wait(3),
            Func(self.errorSnd.stop))
            
        
        self.sequence = Sequence(
            Func(Globals.showText, self, Localizer.storyIntroPart1),
            Func(self.sip1.play),
            Wait(6),
            Func(Globals.hideText, self),
            Func(self.sip1.stop),
            Func(self.sip2.play),
            Func(Globals.showText, self, Localizer.storyIntroPart2),
            Wait(8),
            Func(self.sip2.stop),
            Func(Globals.hideText, self),
            Wait(3),
            Func(Globals.showLocationText, self, Localizer.amdHqArea),
            Wait(2),
            Func(Globals.hideLocText, self),
            Wait(2),
            Func(self.cardQuestion.play),
            Wait(5),
            Func(self.cardQuestion.stop),
            Wait(2),
            Func(self.cardAnswer.play))
        self.sequence.start()

        self.visualSequence = Sequence(
            Wait(7),
            Func(self.amdCard.show),
            LerpColorScaleInterval(self.amdCard, 1, VBase4(1, 1, 1, 1), blendType = 'easeInOut'),
            Wait(8),
            LerpColorScaleInterval(self.amdCard, 1, VBase4(1, 1, 1, 0), blendType = 'easeInOut'),
            Func(self.amdCard.hide),
            Wait(2),
            Func(self.amdHq.show),
            LerpColorScaleInterval(self.amdHq, 1, VBase4(1, 1, 1, 1), blendType = 'easeInOut'),
            Func(self.saul.show),
            Func(self.boss.show),
            LerpColorScaleInterval(self.saul, 1, VBase4(1, 1, 1, 1), blendType = 'easeInOut'),
            LerpColorScaleInterval(self.boss, 1, VBase4(1, 1, 1, 1), blendType = 'easeInOut'),
            Func(Globals.showChatBubble, self, Localizer.newCardQuestion, self.saul, -.6, 0, 1.2),
            Wait(4),
            Func(Globals.hideChatBubble, self),
            Func(Globals.showChatBubble, self, Localizer.newCardAnswer, self.boss, -.6, 0, 1.2),
            Wait(8),
            Func(Globals.hideChatBubble, self),
            Func(self.amdHq.hide),
            Func(self.saul.hide),
            Func(self.boss.hide),
            Func(self.errorSequence.start))
        self.visualSequence.start()
            
        
    def showText(self, text):
      self.text = OnscreenText(text = text, style=3, fg=(1,1,1,1), scale = 0.07, wordwrap = 30, parent=base.a2dBottomCenter, pos=(0, -1))
      self.text.show()
      self.textUpInterval = self.text.posInterval(.5, VBase3(0, 0, 1.2))
      self.textUpInterval.start()

    def hideText(self):
      if self.text is not None:
          self.textDownInterval = Sequence(self.text.posInterval(.5, VBase3(0, 0, -1)), Func(self.text.hide))
          self.textDownInterval.start()
          
    def showLocationText(self, text):
      self.locText = OnscreenText(text = text, style=3, fg=(1,1,1,1), scale = 0.08, wordwrap = 30, parent=base.a2dBottomCenter, pos=(0, .3))
      self.locText.setColorScale(1, 1, 1, 0)
      self.locText.show()
      self.locTextFadeIn = LerpColorScaleInterval(self.locText, 1, VBase4(1, 1, 1, 1), blendType = 'easeInOut')
      self.locTextFadeIn.start()

    def hideLocText(self):
      if self.locText is not None:
          self.locTextFadeOut = Sequence(LerpColorScaleInterval(self.locText, 1, VBase4(1, 1, 1, 1), blendType = 'easeInOut'), Func(self.locText.hide))
          self.locTextFadeOut.start()
          
    def nextScene(self):
        self.nextSceneSequence = Sequence(
        Func(self.errorMsg.hide),
        Wait(0.3),
        Func(self.importNextScene))
        self.nextSceneSequence.start()

    def importNextScene(self):
        self.nextSceneSequence.finish()
        import SceneTwo
w = GameStart()