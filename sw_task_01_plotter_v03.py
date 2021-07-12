# import pyside2 utilities and some libraries fro canvous and matplotlib fro equation drawing
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PySide2.QtWidgets import QWidget, QApplication, QPushButton, QMessageBox, QLabel, QTextEdit, QStyle, QHBoxLayout, QVBoxLayout, QGroupBox
from PySide2.QtGui import QIcon, QImage, QPixmap, QGuiApplication, QFont
from PySide2.QtCore import Qt
import sys
import re
import matplotlib.pyplot as plt
import numpy as np


# main class for the application
class Window(QWidget):
    def __init__(self):
        super().__init__()
        # the allowed and the operators that will be taking from user and replaced
        self.replacements = {
            '^': '**'
        }
        self.allowedWords = [
            'x'
        ]
        # set the taks title and the weigth and the hieght for the window
        self.setWindowTitle("Equation Plotter")
        self.setGeometry(500, 100, 450, 850)
        # intialize the gui window
        self.initGui()

    def initGui(self):
        # create and label for the image
        self.label_image = self.createLabel()
        # set an icon for the application
        self.setIcon()
        # create layout to aligne objects
        self.createLayout()
        # create a flex box to make objects responsive
        vbox = QVBoxLayout()
        # put the image in the vbox
        self.displayImage(vbox)
        # put the textboxes in the vbox
        self.createTextBoxes(vbox)
        # put the canvous that will hold the graph in the vbox
        self.createCanvas(vbox)
        # put the plot button in the vbox
        self.createButtons(vbox)
        # set the layout of the group box to the vbox
        self.groupBox.setLayout(vbox)
        # create a hbox that will hold this vbox
        hbox = QHBoxLayout()
        hbox.addWidget(self.groupBox)
        # set the layout of the application to the hbox
        self.setLayout(hbox)
        # center the window on the screen
        self.center()

    def setIcon(self):
        # get the icon from path and set it as the icon
        appIcon = QIcon("icon.png")
        self.setWindowIcon(appIcon)

    def createTextBoxes(self, vbox):
        # Create the equation field
        self.equation = QTextEdit(self)
        self.equation.setMinimumHeight(55)
        self.equation.setPlaceholderText("EQUATION")
        vbox.addWidget(self.equation)

        # create a hbox to make the max / min boxes in same line
        hbox = QHBoxLayout()

        # Create the Min field
        self.minimum = QTextEdit(self)
        self.minimum.setMinimumHeight(55)
        self.minimum.setPlaceholderText("LOWER LIMIT")
        hbox.addWidget(self.minimum)
        vbox.addLayout(hbox)

        # Create the Max field
        self.maximum = QTextEdit(self)
        self.maximum.setMinimumHeight(55)
        self.maximum.setPlaceholderText("UPPER LIMIT")
        hbox.addWidget(self.maximum)

    def createButtons(self, vbox):
        # creat a button and set the plotSolt as its slot when the signal came by user
        self.plotBtn = QPushButton("Plot", self)
        self.plotBtn.setMinimumHeight(55)
        vbox.addWidget(self.plotBtn)
        self.plotBtn.clicked.connect(self.plotSlot)

    def createCanvas(self, vbox):
        # create a canvas and set it to a figure
        fig = plt.figure(figsize=(10, 5))
        self.canvas = FigureCanvas(fig)
        vbox.addWidget(self.canvas)

    # Function to display an image
    def displayImage(self, vbox):
        image = QImage("icon.png")
        display_image = QPixmap.fromImage(image)

        self.label_image.setPixmap(display_image)
        self.label_image.setScaledContents(True)
        vbox.addWidget(self.label_image)

    # Function to Create label that contains images
    def createLabel(self):
        created_label = QLabel(self)
        created_label.setStyleSheet(
            "border: 3 solid #9dced4; background-color: #4E4E4E")
        return created_label
    # Function to center the window

    def center(self):
        self.setGeometry(
            QStyle.alignedRect(
                Qt.LeftToRight,
                Qt.AlignCenter,
                self.size(),
                QGuiApplication.primaryScreen().availableGeometry(),
            ),
        )
    # create the group box that will hold the layout

    def createLayout(self):
        self.groupBox = QGroupBox("Plotter")
        self.groupBox.setFont(QFont("Sanserif", 13))
    # a slot for the user signal to test and draw the equation

    def plotSlot(self):
        if re.match("(([0-9]{1,}[*|^|\/|+|-][xX])|[xX]|[0-9]{1,}|[*|^|\/|+|-]|\s)+$", self.equation.toPlainText(), flags=0):
            pass
        else:
            QMessageBox.critical(
                self, "Error", "The equation you entered has a wrong format !!", QMessageBox.Ok)
            return
        if re.match("^-?[0-9]+$", self.maximum.toPlainText(), flags=0):
            pass
        else:
            QMessageBox.critical(
                self, "Error", "The Maximum must be a number !!", QMessageBox.Ok)
            return
        if re.match("^-?[0-9]+$", self.minimum.toPlainText(), flags=0):
            pass
        else:
            QMessageBox.critical(
                self, "Error", "The Minimum must be a number !!", QMessageBox.Ok)
            return
        if int(self.minimum.toPlainText()) > int(self.maximum.toPlainText()):
            QMessageBox.critical(
                self, "Error", "The Minimum can't be greter than the maximum !!", QMessageBox.Ok)
            return
        # matplotlib script
        plt.clf()
        self.ax = self.canvas.figure.subplots()
        self.x = np.linspace(int(self.minimum.toPlainText()),
                             int(self.maximum.toPlainText()), 100)
        self.y = self.string2func(self.equation.toPlainText())(self.x)

        self.ax.plot(self.x, self.y)

        self.ax.set(
            title="f(x)="+self.equation.toPlainText())
        self.ax.grid()
        self.canvas.draw()
        return

    # Function to convert the input equation to a code so we can plot it and this for security so no one can inject a code
    def string2func(self, string):
        # find all words and check if all are allowed:
        for word in re.findall('[a-zA-Z_]+', string):
            if word not in self.allowedWords:
                raise ValueError(
                    '"{}" is forbidden to use in math expression'.format(word)
                )

        for old, new in self.replacements.items():
            string = string.replace(old, new)

        def func(x):
            return eval(string)

        return func


if __name__ == '__main__':

    myApp = QApplication(sys.argv)
    window = Window()
    window.show()
    style_sheet = """
        QWidget {
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
            color: #000000;
            padding: 6px 2px;
            border: 2px solid #9dced4;
        }

    """
    myApp.setStyleSheet(style_sheet)
    sys.exit(myApp.exec_())
