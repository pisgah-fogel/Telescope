# To run the script:
# Run: ~/Downloads/FreeCAD_0.19-23463-Linux-Conda_glibc2.12-x86_64.AppImage
# Then copy the code below in the python terminal

# Doesn't work
#import sys
#sys.path.append('/usr/lib/freecad/lib')
#sys.path.append('/usr/lib/freecad-python3/lib/')

import matplotlib.pyplot as plt
import FreeCAD
import FreeCAD as App, FreeCADGui as Gui, Part, time, sys, math, Draft, DraftGeomUtils
from PySide import QtGui,QtCore

Gui.runCommand('Std_Workbench',22)
Gui.runCommand('Std_ViewStatusBar',1)
FreeCAD.openDocument('/home/phileas/projects/Telescope/dobson.FCStd')
App.setActiveDocument("dobson")
App.ActiveDocument=App.getDocument("dobson")
Gui.ActiveDocument=Gui.getDocument("dobson")

class Animation(object):
    def __init__(self):
        App.Console.PrintMessage('init')
        App.ActiveDocument.recompute()
        self.timer = QtCore.QTimer()
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.update)
        self.an = 0.1
        self.logangle = []
        for i in range(100):
            self.logangle.append(0)
        plt.ylim([0, 95])
        plt.xlim([0, 100])
        self.line, = plt.plot(self.logangle)
        plt.show()

    def start(self):
        self.timer.start(500)

    def update(self):
        self.an = self.an + 0.05 if self.an < (math.pi/2) else 0.0
        angle = math.degrees(self.an)
        App.ActiveDocument.Spreadsheet.set('B12:B12', str(angle)) # set telscope angle
        App.ActiveDocument.recompute()
        App.Console.PrintMessage('angle: '+str(angle)+'\n')
        self.logangle.pop(0)
        self.logangle.append(float(angle))
        self.line.set_ydata(self.logangle)
        plt.draw()

    def stop(self):
        self.timer.stop()


a = Animation()
a.start()
a.stop()
