# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Raspberry/Interface/Designs/detectionDesign.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_detectionDialog(object):
    def setupUi(self, detectionDialog):
        detectionDialog.setObjectName("detectionDialog")
        detectionDialog.resize(900, 140)
        detectionDialog.setStyleSheet("*{\n"
"font: 20pt \"Ubuntu\";\n"
"}")
        self.gridLayout = QtWidgets.QGridLayout(detectionDialog)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.widget = QtWidgets.QWidget(detectionDialog)
        self.widget.setStyleSheet("background-color: rgb(230, 230, 230);\n"
"border-left: 40px solid;\n"
"border-color: rgb(255, 210, 47);\n"
"border-color: rgb(200, 25, 13);")
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_2.setContentsMargins(40, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(40)
        font.setBold(False)
        font.setItalic(False)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("QPushButton{\n"
"border:none;\n"
"    font: 40pt \"Arial Rounded MT Bold\";\n"
"}\n"
"QPushButton:hover{\n"
"background-color: rgb(76, 165, 34);\n"
"background-color: rgb(170, 0, 0);\n"
"}")
        self.pushButton.setAutoDefault(True)
        self.pushButton.setDefault(False)
        self.pushButton.setFlat(False)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 0, 2, 1, 1)
        self.widget_2 = QtWidgets.QWidget(self.widget)
        self.widget_2.setStyleSheet("border:none;")
        self.widget_2.setObjectName("widget_2")
        self.messageLabel = QtWidgets.QLabel(self.widget_2)
        self.messageLabel.setGeometry(QtCore.QRect(20, 40, 661, 81))
        self.messageLabel.setStyleSheet("background-color: none;")
        self.messageLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.messageLabel.setObjectName("messageLabel")
        self.label = QtWidgets.QLabel(self.widget_2)
        self.label.setGeometry(QtCore.QRect(80, 10, 141, 31))
        self.label.setStyleSheet("background-color: none;")
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self.widget_2)
        self.label_3.setGeometry(QtCore.QRect(40, 10, 21, 31))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.widget_2, 0, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.widget)
        self.line.setStyleSheet("border:none;\n"
"border-right: 1px solid;\n"
"border-color: rgb(216, 216, 216);\n"
"")
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_2.addWidget(self.line, 0, 1, 1, 1)
        self.gridLayout_2.setColumnStretch(0, 80)
        self.gridLayout_2.setColumnStretch(2, 20)
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)

        self.retranslateUi(detectionDialog)
        self.pushButton.clicked.connect(detectionDialog.clearAlert) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(detectionDialog)

    def retranslateUi(self, detectionDialog):
        _translate = QtCore.QCoreApplication.translate
        detectionDialog.setWindowTitle(_translate("detectionDialog", "Dialog"))
        self.pushButton.setText(_translate("detectionDialog", "X"))
        self.messageLabel.setText(_translate("detectionDialog", "Se detectó {situacion} en cámara: {camaraId}"))
        self.label.setText(_translate("detectionDialog", "Detección"))
        self.label_3.setText(_translate("detectionDialog", "!"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    detectionDialog = QtWidgets.QDialog()
    ui = Ui_detectionDialog()
    ui.setupUi(detectionDialog)
    detectionDialog.show()
    sys.exit(app.exec_())
