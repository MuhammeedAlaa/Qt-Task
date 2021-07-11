from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PySide2.QtWidgets import QWidget, QApplication, QPushButton, QMessageBox, QLabel, QTextEdit, QStyle, QHBoxLayout, QVBoxLayout, QGroupBox
from PySide2.QtGui import QIcon, QImage, QPixmap, QGuiApplication, QFont
from PySide2.QtCore import Qt
import sys
import re
import matplotlib.pyplot as plt
import numpy as np


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.replacements = {
            '^': '**'
        }
        self.allowedWords = [
            'x'
        ]
        self.setWindowTitle("Task 1")
        self.setGeometry(500, 100, 450, 850)
        self.label_image = self.createLabel()
        self.initGui()

    def initGui(self):
        self.setIcon()

        self.createLayout()
        vbox = QVBoxLayout()

        self.displayImage(vbox)

        self.createTextBoxes(vbox)

        self.createButtons(vbox)

        fig = plt.figure(figsize=(10, 5))
        self.canvas = FigureCanvas(fig)
        vbox.addWidget(self.canvas)
        self.groupBox.setLayout(vbox)
        hbox = QHBoxLayout()
        hbox.addWidget(self.groupBox)
        self.setLayout(hbox)
        self.center()

    def setIcon(self):
        appIcon = QIcon("icon.png")
        self.setWindowIcon(appIcon)

    def createTextBoxes(self, vbox):
        hbox = QHBoxLayout()
        # Create the equation field
        self.equation = QTextEdit(self)
        self.equation.setMinimumHeight(55)
        self.equation.setPlaceholderText("EQUATION")
        vbox.addWidget(self.equation)

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
        plotbtn = QPushButton("Plot", self)
        plotbtn.setMinimumHeight(55)
        vbox.addWidget(plotbtn)
        plotbtn.clicked.connect(self.plotSlot)

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

    def center(self):
        self.setGeometry(
            QStyle.alignedRect(
                Qt.LeftToRight,
                Qt.AlignCenter,
                self.size(),
                QGuiApplication.primaryScreen().availableGeometry(),
            ),
        )

    def createLayout(self):
        self.groupBox = QGroupBox("Plotter")
        self.groupBox.setFont(QFont("Sanserif", 13))

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

        self.ax = self.canvas.figure.subplots()
        x = np.linspace(int(self.minimum.toPlainText()),
                        int(self.maximum.toPlainText()), 100)
        y = self.string2func(self.equation.toPlainText())(x)

        self.ax.plot(x, y)

        self.ax.set(xlabel='x', ylabel='y',
                    title=self.equation.toPlainText())
        self.ax.grid()
        self.canvas.draw()
        return

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
