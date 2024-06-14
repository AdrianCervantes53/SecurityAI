from Interface.Scripts.BaseClass import BaseWindow
from Interface.Designs.alertDesign import Ui_alertDialog
from Interface.Designs.detectionDesign import Ui_detectionDialog
from Interface.Designs.messageDesign import Ui_messageDialog

class AlertWindow(BaseWindow, Ui_alertDialog):
    def __init__(self, screen, object):
        super().__init__(screen, object)

class DetectionWindow(BaseWindow, Ui_detectionDialog):
    def __init__(self, screen, object):
        super().__init__(screen, object)

class MessageWindow(BaseWindow, Ui_messageDialog):
    def __init__(self, screen, object):
        super().__init__(screen, object)
