from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLineEdit
from PyQt5 import QtWidgets

class BaseWindow(QWidget):
    dialogAction = pyqtSignal(str)
    def __init__(self, screen, object):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowModality(Qt.WindowModality.WindowModal)
        #Qt.WindowModality.WindowModal
        self.screenGeometry = screen.availableGeometry()
        self.setupUi(self)
        self.dialogAction.connect(object)
        
    
    def showDialog(self, position) -> None:
        self.position = position
        #x = (self.screenGeometry.width() - self.width()) - 50
        x= 20
        margin = 20
        y = 23 + (position * (self.height() + margin))
        self.setGeometry(x, y+20, self.width(), self.height())
        self.show()

    def updateText(self, text):
        self.messageLabel.setText(text)

    def clearAlert(self):
        self.dialogAction.emit(str(self.position))

    def exit(self) -> None:
        self.close()
        