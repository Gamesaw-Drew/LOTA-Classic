from direct.fsm import ClassicFSM, State
from direct.gui.DirectGui import *

class UnsupportedDialog:

    def __init__(self, text = "Warning: This is an old an unsupported version of Legend of the AMD."):
        self.dialog = DirectDialog.DirectDialog(
            dialogName='ControlRemap', doneEvent='exitDialog', style=Acknowledge,
            text=text, text_wordwrap=24,
            text_pos=(0, 0, -0.8), suppressKeys = True, suppressMouse = True
        )
        self.dialog.accept('exitDialog', self.exitDialog)
        base.transitions.fadeScreen(.5)
        
    def exitDialog(self):
        base.transitions.noFade()
        self.dialog.cleanup()
        del self.dialog