'''
Created on Sep 4, 2016

@author: Drew
'''
from direct.actor.Actor import Actor
from direct.interval.ActorInterval import LerpAnimInterval
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import NodePath, PandaNode, LightRampAttrib, Vec4,\
    AmbientLight, DirectionalLight, Vec3, TextNode, CollisionTraverser, CollisionRay,\
    CollisionNode, CollideMask, CollisionHandlerQueue, BitMask32
from direct.gui.OnscreenText import OnscreenText
from Game.NewGame.Player import CreatePlayer
import sys
from panda3d.core import Vec3, load_prc_file_data, ShaderTerrainMesh
from panda3d.bullet import BulletWorld, BulletPlaneShape, BulletRigidBodyNode

class TestWorld:

    def __init__(self):
        load_prc_file_data("", """
            stm-max-chunk-count 1024
            stm-max-views 20
        """)
        self.world = None
        self.worldNP = None
        # Setup everything
        self.setupWorld()
        
        # Get the player
        CreatePlayer.CreatePlayer(self.world, self.worldNP)

    def setupWorld(self):
        # Set the background to be black
        base.win.setClearColor((0, 0, 0 ,1))
        
        # Load Chris's Room
        self.chrisRoom = loader.loadModel("Resources/models/ROOMS/ChrisRoom.egg")
        self.chrisRoom.reparentTo(render)
        self.chrisRoom.setPos(0, 0, -0.1)
        self.chrisRoom.setScale(0.4)
        
        # Load his laptop onto the desk
        self.chrisLaptop = loader.loadModel("Resources/models/OBJ/ChrisLaptop.egg")
        self.chrisLaptop.reparentTo(render)
        self.chrisLaptop.setPosHpr(-5.5, 1.5, 1.0, 90, 0, 0)
        self.chrisLaptop.setScale(0.8)
        
        # TODO: Set the screen texture
        #screenTexture = loader.loadTexture("Resources/maps/skypeChat.png")
        #self.chrisLaptopScreen = self.chrisLaptop.find("**/screen")
        #self.chrisLaptopScreen.setTexture(screenTexture, 1)
        
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))
        self.worldNP = render.attachNewNode('World')
        
        self.terrain_np = render.attach_new_node("terrain")

        # Ground
        ground = BulletPlaneShape(Vec3(0, 0, 1), 0)
    
        #img = PNMImage(Filename('models/elevation2.png'))
        #shape = BulletHeightfieldShape(img, 1.0, ZUp)
    
        np = self.worldNP.attachNewNode(BulletRigidBodyNode('Ground'))
        np.node().addShape(ground)
        np.setPos(0, 0, 0)
        np.setCollideMask(BitMask32.allOn())
        self.world.attachRigidBody(np.node())


w = TestWorld()