from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QLabel, QTextEdit, QStyle, QMainWindow
from PySide2.QtGui import QIcon, QImage, QPixmap, QGuiApplication
from PySide2.QtCore import Qt
import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task 1")
        self.setGeometry(500, 100, 350, 550)
        self.label_image = self.createLabel(75, 20, 200, 200)
        self.initGui()

    def initGui(self):
        self.setIcon()
        self.displayImage()
        self.createButtons()
        self.createTextBoxes()
        self.center()

    def setIcon(self):
        appIcon = QIcon("icon.png")
        self.setWindowIcon(appIcon)

    def createTextBoxes(self):
        # Create the equation field
        equation = QTextEdit(self)
        equation.setGeometry(25, 270, 300, 40)
        equation.setPlaceholderText("EQUATION")

        # Create the Max field
        maximum = QTextEdit(self)
        maximum.setGeometry(25, 330, 300, 40)
        maximum.setPlaceholderText("UPPER LIMIT")

        # Create the Min field
        minimum = QTextEdit(self)
        minimum.setGeometry(25, 390, 300, 40)
        minimum.setPlaceholderText("LOWER LIMIT")

    def createButtons(self):
        plotbtn = QPushButton("Plot", self)
        plotbtn.setGeometry(25, 450, 300, 40)
        # plotbtn.clicked.connect(self.quitApp)

    # Function to display an image
    def displayImage(self):
        image = QImage("icon.png")
        display_image = QPixmap.fromImage(image)

        self.label_image.setPixmap(display_image)
        self.label_image.setScaledContents(True)
    # Function to Create label that contains images

    def createLabel(self, left, top, width, height):
        created_label = QLabel(self)
        created_label.setGeometry(left, top, width, height)
        return created_label

    def center(self):
        self.setGeometry(
            QStyle.alignedRect(
                Qt.LeftToRight,
                Qt.AlignCenter,
                self.size(),
                QGuiApplication.primaryScreen().availableGeometry(),
            ),
        )

    def quitApp(self):
        userInfo = QMessageBox.question(
            self, "Exit", "Do you want to close the application ?", QMessageBox.Yes | QMessageBox.No)
        if userInfo == QMessageBox.No:
            pass
        elif userInfo == QMessageBox.Yes:
            myApp.quit()


myApp = QApplication(sys.argv)
window = Window()
window.show()
style_sheet = """
    QMainWindow {
        background-color: #383738;
    }

    QPushButton {
        background-color: #9dced4;
        color: #2E2E2E;
        border: 2px solid #9dced4;
    }
    QMessageBox {
        background-color: #383738;
    }

    QTextEdit {
        background-color: #cbd3d7;
        color: #8E8E8E;
        padding: 6px 2px;
        border: 2px solid #9dced4;
    }

    QLabel {
        border: 3 solid #9dced4;
        background-color: #4E4E4E;
    }

"""
myApp.setStyleSheet(style_sheet)
sys.exit(myApp.exec_())
