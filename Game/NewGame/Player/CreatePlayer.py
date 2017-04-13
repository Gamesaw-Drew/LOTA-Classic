'''
Created on Sep 8, 2016

@author: Drew
'''

from direct.actor.Actor import Actor
from direct.interval.ActorInterval import LerpAnimInterval
from direct.task.TaskManagerGlobal import taskMgr
from direct.interval.IntervalGlobal import * 
from panda3d.core import NodePath, PandaNode, LightRampAttrib, Vec4,\
    AmbientLight, DirectionalLight, Vec3, TextNode, CollisionTraverser, CollisionRay,\
    CollisionNode, CollideMask, CollisionHandlerQueue, BitMask32
from direct.gui.OnscreenText import OnscreenText
from panda3d.bullet import BulletCharacterControllerNode, BulletCapsuleShape,\
    ZUp, BulletRigidBodyNode, BulletSphereShape

class CreatePlayer:

    def __init__(self, world, worldNP):
        self.diamondbackChar = None
        
        self.world = world
        self.worldNP = worldNP
        
        # Store which keys are being pressed
        self.keyPressed = {"fwd": 0, "back": 0, "left": 0, "right": 0}
        
        # Setup everything
        self.createCharacter()
        self.setupKeys()

        self.isMoving = False
        taskMgr.add(self.move, "moveTask")
        
        self.pos = OnscreenText(
          text="POS",
          style=3, fg=(1,1,1,1), pos=(-0.02, 0.1), scale = .07, parent=base.a2dBottomRight, align=TextNode.ARight)
        
        self.lerpAnimation(self.diamondbackChar, "idle")

    def createCharacter(self):
        charColl = BulletCapsuleShape(0.4, 1.75 - 2 * 0.4, ZUp)
        self.diamondChar = BulletCharacterControllerNode(charColl, 0.4, 'Player')
        self.diamondCharNP = self.worldNP.attachNewNode(self.diamondChar)
        self.diamondCharNP.setPos(0, 0, 0)
        self.diamondCharNP.setH(-90)
        self.diamondCharNP.setCollideMask(BitMask32.allOn())
        self.world.attachCharacter(self.diamondChar)
        
        # Summon the lord Diamondback
        self.diamondbackChar = Actor("Resources/models/CHAR/CHRIS", {"walk": "Resources/models/CHAR/CHRIS-Walk2", "idle": "Resources/models/CHAR/CHRIS-Idle2", "jump": "Resources/models/CHAR/CHRIS-Jump"})
        self.diamondbackChar.reparentTo(self.diamondCharNP)
        self.diamondbackChar.setPos(0, 0, -.83)
        self.diamondbackChar.setScale(1)
        self.diamondbackChar.setBlend(animBlend=True, frameBlend=True)
        
        # Set the camera position tracker
        self.camPos = NodePath(PandaNode("camTracker"))
        self.camPos.reparentTo(self.diamondbackChar)
        
        # Set the camera to track the lord
        base.camera.reparentTo(self.camPos)
        base.camera.setPosHpr(0, 6, 2.5, 180, -5, 0)
        base.camLens.setFov(90)
        
    def doJump(self):
        self.diamondChar.setMaxJumpHeight(1)
        self.diamondChar.setJumpSpeed(4)
        self.diamondChar.doJump()
        self.JUMPSEQ = Sequence(
                 Func(self.lerpAnimation, self.diamondbackChar, "jump", doLoop = False),
                 Wait(2),
                 Func(self.doAnimation)
                 ).start()

    def setupKeys(self):
        base.accept("w", self.keypress, ["fwd", True])
        base.accept("s", self.keypress, ["back", True])
        base.accept("a", self.keypress, ["left", True])
        base.accept("d", self.keypress, ["right", True])
        base.accept('space', self.doJump)

        base.accept("w-up", self.keypress, ["fwd", False])
        base.accept("s-up", self.keypress, ["back", False])
        base.accept("a-up", self.keypress, ["left", False])
        base.accept("d-up", self.keypress, ["right", False])
        
    def disableKeys(self):
        base.ignore("w")
        base.ignore("s")
        base.ignore("a")
        base.ignore("d")
        base.ignore('space')

        base.ignore("w-up")
        base.ignore("s-up")
        base.ignore("a-up")
        base.ignore("d-up")

    def keypress(self, key, value):
        self.keyPressed[key] = value

    def move(self, task):
        dt = globalClock.getDt()

        if (self.keyPressed["fwd"]!=0):
            self.diamondCharNP.setY(self.diamondCharNP, -5 * dt)

        if (self.keyPressed["left"]!=0):
            self.diamondCharNP.setH(self.diamondCharNP.getH() + 150 * dt)

        if (self.keyPressed["right"]!=0):
            self.diamondCharNP.setH(self.diamondCharNP.getH() - 150 * dt)

        if (self.keyPressed["back"]!=0):
            self.diamondCharNP.setY(self.diamondCharNP, +5 * dt)

        if self.keyPressed["fwd"] or self.keyPressed["back"] or self.keyPressed["left"] or self.keyPressed["right"]:
            if self.isMoving is False:
                self.lerpAnimation(self.diamondbackChar, "walk")
                self.isMoving = True
        else:
            if self.isMoving:
                self.lerpAnimation(self.diamondbackChar, "idle")
                self.isMoving = False
                
        self.pos["text"] = str(self.diamondCharNP.getPos())
                
        return task.cont
    
    def doAnimation(self):
        if self.isMoving:
            self.lerpAnimation(self.diamondbackChar, "walk")
        else:
            self.lerpAnimation(self.diamondbackChar, "idle")
        if self.JUMPSEQ:
            self.JUMPSEQ.finish()
        
    def lerpAnimation(self, actor, nextAnim, doLoop = True):
        LerpAnimInterval(actor, 0.4, self.diamondbackChar.getCurrentAnim(), nextAnim).start()
        actor.stop(actor.getCurrentAnim())
        if doLoop:
            actor.loop(nextAnim)
        else:
            actor.play(nextAnim)
            
    def moveTo(self, x, y, z, h):
        self.diamondCharNP.setPosHpr(x, y, z, h, 0, 0)