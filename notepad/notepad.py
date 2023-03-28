import os
import sys
from PyQt5.QtWidgets import qApp
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtWidgets import QLabel, QTextEdit
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtGui import QFont


class NotepadWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.filePath = ""
        vBoxMain = QVBoxLayout()

        self.txtedt = QTextEdit()
        self.txtedt.setFont(QFont("Monospace", 12))
        self.txtedt.setMinimumWidth(960)
        self.txtedt.setMinimumHeight(540)
        vBoxMain.addWidget(self.txtedt)

        self.labelFilePath = QLabel("Unsaved File")
        hBoxStatus = QHBoxLayout()
        hBoxStatus.addWidget(self.labelFilePath)
        hBoxStatus.addStretch()
        vBoxMain.addLayout(hBoxStatus)

        self.setLayout(vBoxMain)


class Notepad(QMainWindow):
    def __init__(self):
        super().__init__()

        menuBar = self.menuBar()
        
        # Menu: File
        fileMenu = menuBar.addMenu("File")
        
        # Action: New File
        newFileAction = fileMenu.addAction("New file")
        newFileAction.setShortcut("Ctrl+N")
        newFileAction.triggered.connect(self.newFileOnTriggered)

        # Action: Opem File
        openFileAction = fileMenu.addAction("Open file")
        openFileAction.setShortcut("Ctrl+O")
        openFileAction.triggered.connect(self.openFileOnTriggered)
        
        fileMenu.addSeparator()

        # Action: Save File
        saveFileAction = fileMenu.addAction("Save file")
        saveFileAction.setShortcut("Ctrl+S")
        saveFileAction.triggered.connect(self.saveFileOnTriggered)

        # Action: Save As File
        saveAsAction = fileMenu.addAction("Save as")
        saveAsAction.setShortcut("Ctrl+Alt+S")
        saveAsAction.triggered.connect(self.saveAsOnTriggered)
        
        fileMenu.addSeparator()

        # Action: Quit
        quitAction = fileMenu.addAction("Quit")
        quitAction.setShortcut("Ctrl+Q")
        quitAction.triggered.connect(self.quitOnTriggered)

        # Menu: View
        viewMenu = menuBar.addMenu("View")

        # Action: Zoom In
        zoomInAction = viewMenu.addAction("Zoom in")
        zoomInAction.setShortcut("Ctrl++")
        zoomInAction.triggered.connect(self.zoomInOnTriggered)

        # Action: Zoom Out
        zoomOutAction = viewMenu.addAction("Zoom out")
        zoomOutAction.setShortcut("Ctrl+-")
        zoomOutAction.triggered.connect(self.zoomOutOnTriggered)
        
        viewMenu.addSeparator()

        # Action: Reset Zoom
        resetZoomAction = viewMenu.addAction("Reset zoom")
        resetZoomAction.setShortcut("Ctrl+0")
        resetZoomAction.triggered.connect(self.resetZoomOnTriggered)

        # Action: About
        aboutAction = menuBar.addAction("About")
        aboutAction.triggered.connect(self.aboutOnTriggered)

        self.notepadWidget = NotepadWidget()
        self.setCentralWidget(self.notepadWidget)
        self.setWindowTitle("Notepad")
        self.show()

    def newFileOnTriggered(self):
        if self.notepadWidget.filePath == "":
            if self.notepadWidget.txtedt.toPlainText() != "":
                self.showMessageBoxSave()
        else:
            with open(self.notepadWidget.filePath, "r") as file:
                if file.read() != self.notepadWidget.txtedt.toPlainText():
                    self.showMessageBoxSave()
        self.notepadWidget.filePath = ""
        self.notepadWidget.labelFilePath.setText("Unsaved File")
        self.notepadWidget.txtedt.clear()

    def openFileOnTriggered(self):
        if self.notepadWidget.filePath == "":
            if self.notepadWidget.txtedt.toPlainText() != "":
                self.showMessageBoxSave()
        else:
            with open(self.notepadWidget.filePath, "r") as file:
                if file.read() != self.notepadWidget.txtedt.toPlainText():
                    self.showMessageBoxSave()
        fileInfo = QFileDialog.getOpenFileName(self, "Open File", os.getenv("HOME"))
        if fileInfo[0] != "":
            self.notepadWidget.filePath = fileInfo[0]
            with open(self.notepadWidget.filePath, "r") as file:
                self.notepadWidget.txtedt.setText(file.read())
            self.notepadWidget.labelFilePath.setText(f"{self.notepadWidget.filePath}")

    def saveFileOnTriggered(self):
        if self.notepadWidget.filePath != "":
            with open(self.notepadWidget.filePath, "w") as file:
                file.write(self.notepadWidget.txtedt.toPlainText())
        else:
            self.saveAsOnTriggered()

    def saveAsOnTriggered(self):
        fileInfo = QFileDialog.getSaveFileName(self, "Save As", os.getenv("HOME"))
        if fileInfo[0] != "":
            self.notepadWidget.filePath = fileInfo[0]
            with open(self.notepadWidget.filePath, "w") as file:
                file.write(self.notepadWidget.txtedt.toPlainText())
            self.notepadWidget.labelFilePath.setText(f"{self.notepadWidget.filePath}")

    def quitOnTriggered(self):
        if self.notepadWidget.filePath == "":
            if self.notepadWidget.txtedt.toPlainText() != "":
                self.showMessageBoxSave()
        else:
            with open(self.notepadWidget.filePath, "r") as file:
                if file.read() != self.notepadWidget.txtedt.toPlainText():
                    self.showMessageBoxSave()
        qApp.exit()

    def zoomInOnTriggered(self):
        font = self.notepadWidget.txtedt.font()
        font.setPointSize(font.pointSize() + 1)
        self.notepadWidget.txtedt.setFont(font)

    def zoomOutOnTriggered(self):
        font = self.notepadWidget.txtedt.font()
        font.setPointSize(font.pointSize() - 1)
        self.notepadWidget.txtedt.setFont(font)

    def resetZoomOnTriggered(self):
        font = self.notepadWidget.txtedt.font()
        font.setPointSize(12)
        self.notepadWidget.txtedt.setFont(font)

    @staticmethod
    def aboutOnTriggered():
        messageBoxAbout = QMessageBox()
        messageBoxAbout.setWindowTitle("About Notepad")
        messageBoxAbout.setText("A simple, cross-platform notepad.\n\ngithub.com/memmre\nlinkedin.com/in/memmre")
        messageBoxAbout.setStandardButtons(QMessageBox.Ok)
        messageBoxAbout.exec_()

    def showMessageBoxSave(self):
        messageBoxSave = QMessageBox()
        messageBoxSave.setWindowTitle("Unsaved Changes")
        messageBoxSave.setIcon(QMessageBox.Warning)
        messageBoxSave.setText("Do you want to save the file?")
        messageBoxSave.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        messageBoxSave.setDefaultButton(QMessageBox.Yes)
        messageBoxSave.buttonClicked.connect(self.messageBoxSaveOnClicked)
        messageBoxSave.exec_()

    def messageBoxSaveOnClicked(self, button):
        if button.text() == "&Yes":
            self.saveFileOnTriggered()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    notepad = Notepad()
    sys.exit(app.exec_())
