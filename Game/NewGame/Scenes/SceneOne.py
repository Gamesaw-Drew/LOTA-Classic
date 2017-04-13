from direct.actor import Actor
from direct.actor.Actor import Actor
from direct.directbase import DirectStart  
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectGui import *   
from direct.gui.OnscreenText import OnscreenText
from direct.interval.ActorInterval import LerpAnimInterval
from direct.interval.IntervalGlobal import * 
from direct.showbase import ShowBase
from direct.task.TaskManagerGlobal import taskMgr
import os
from panda3d.core import NodePath, PandaNode, LightRampAttrib, Vec4, \
    AmbientLight, DirectionalLight, Vec3, TextNode, CollisionTraverser, CollisionRay, \
    CollisionNode, CollideMask, CollisionHandlerQueue, TransparencyAttrib,\
    BitMask32, RopeNode, NurbsCurveEvaluator
from panda3d.core import Vec3, load_prc_file_data
import sys

from Game import AmdLocalizerEnglish as Localizer
from Game import Globals
from Game import LoadResources as Resources
from Game.NewGame.Player import CreatePlayer
from panda3d.bullet import BulletRigidBodyNode, BulletPlaneShape, BulletWorld,\
    BulletDebugNode, BulletBoxShape, BulletSoftBodyNode,\
    BulletCharacterControllerNode, BulletCapsuleShape, ZUp


# Introduction to the story
class SceneOne:

    def __init__(self):
        self.world = None
        self.worldNP = render.attachNewNode('World')
        self.introaudio = Resources.introaudio
        self.intromusic = Resources.intromusic
        initsequence = Sequence(
            Func(self.introaudio.play),
            Func(self.intromusic.play))
        initsequence.start()

        load_prc_file_data("", """
            stm-max-chunk-count 1024
            stm-max-views 20
        """)

        # Setup everything
        self.setupWorld()
        
        # Get the player
        self.userCharacter = CreatePlayer.CreatePlayer(self.world, self.worldNP)
        
        taskMgr.add(self.update, 'updateWorld')

    def setupWorld(self):
               
        def spawnChrisRoom(*args):
            args[0].reparentTo(render)
            args[0].setPos(0, 0, -0.1)
            args[0].setScale(0.4)

        def spawnChrisLaptop(*args):
            args[0].reparentTo(render)
            args[0].setPosHpr(-5.5, 1.5, 1.0, 90, 0, 0)
            args[0].setScale(0.8)
            
        # Load Chris's Room
        self.chrisRoom = loader.loadModel("Resources/models/ROOMS/ChrisRoom", callback = spawnChrisRoom)

        
        # Load his laptop onto the desk
        self.chrisLaptop = loader.loadModel("Resources/models/OBJ/ChrisLaptop", callback = spawnChrisLaptop)
        
        # Load AMD HQ
        self.showAmdHq()

        
        # TODO: Set the screen texture
        #screenTexture = loader.loadTexture("Resources/maps/skypeChat.png")
        #self.chrisLaptopScreen = self.chrisLaptop.find("**/screen")
        #self.chrisLaptopScreen.setTexture(screenTexture, 1)
        
        self.debugNP = self.worldNP.attachNewNode(BulletDebugNode('Debug'))
        self.debugNP.show()
        self.debugNP.node().showWireframe(True)
        self.debugNP.node().showConstraints(True)
        self.debugNP.node().showBoundingBoxes(True)
        self.debugNP.node().showNormals(True)
        
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))
        #self.world.setDebugNode(self.debugNP.node()) # Used to show physics
        
        self.terrain_np = render.attach_new_node("terrain")

        # Ground
        ground = BulletPlaneShape(Vec3(0, 0, 1), 0)
    
        np = self.worldNP.attachNewNode(BulletRigidBodyNode('Ground'))
        np.node().addShape(ground)
        np.setPos(0, 0, 0)
        np.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(np.node())
        
        info = self.world.getWorldInfo()
        info.setAirDensity(1.2)
        info.setWaterDensity(0)
        info.setWaterOffset(0)
        info.setWaterNormal(Vec3(0, 0, 0))

    def update(self, task):
        dt = globalClock.getDt()

        self.world.doPhysics(dt, 4, 1./240.)
        
        return task.cont
    
    def showAmdHq(self):
        #self.userCharacter.disableKeys() # This will be for disabling keys for amd hq cutscene
        # Load AMD HQ
        def spawnAmdHq(*args):
            args[0].reparentTo(render)
            args[0].setPos(4, 52, -0.1)
            args[0].setScale(0.4)
        self.amdHq = loader.loadModel("Resources/models/ROOMS/AmdHQ", callback = spawnAmdHq)
        pass
        
w = SceneOne()