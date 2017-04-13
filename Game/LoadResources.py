from direct.showbase import ShowBase
from panda3d.core import *
from Game import AmdLocalizerEnglish as Localizer
from direct.gui.DirectGui import *

# Everywhere
GameFont = base.loader.loadFont('Resources/fonts/sf.ttf', lineHeight=1.0)
background = OnscreenImage('Resources/maps/background.png').hide()
transcircle = OnscreenImage('Resources/maps/circle.png')
transcircle.hide()

# Title Screen
titleMusic = base.loader.loadMusic('Resources/audio/music/title.dmusic')
logo = OnscreenImage(image = "Resources/maps/logo.png", parent=aspect2d)
logo.hide()

# Scene One
introaudio = base.loader.loadSfx('Resources/audio/DIALOG/INTRODUCTION.dsnd')
intromusic = base.loader.loadMusic("Resources/audio/music/INTRO.dmusic")