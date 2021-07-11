import pytest

from PySide2.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import Test


@pytest.fixture
def app(qtbot):
    testApp = Test.Window()
    qtbot.addWidget(testApp)

    return testApp


def test_arraysPass_after_click(app, qtbot):
    app.equation.setText("2*x+4")
    app.minimum.setText("0")
    app.maximum.setText("10")

    x = np.linspace(0, 10, 100)
    y = 2*x+4

    qtbot.mouseClick(app.plotBtn, Qt.LeftButton)
    assert sum(x == app.x) == len(x) and sum(y == app.y) == len(y)


def test_arraysWrong_after_click(app, qtbot):
    app.equation.setText("2*x+4")
    app.minimum.setText("0")
    app.maximum.setText("10")

    x = np.linspace(0, 10, 100)
    y = 2*x**3+4

    qtbot.mouseClick(app.plotBtn, Qt.LeftButton)
    assert sum(x == app.x) == len(x) and sum(y == app.y) != len(y)
