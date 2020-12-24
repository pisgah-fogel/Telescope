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
        self.logangle = []
        for i in range(100):
            self.logangle.append(0)
        plt.ylim([0, 95])
        plt.xlim([0, 100])
        self.line, = plt.plot(self.logangle)
        plt.show()
        self.horizontal = 0 # horizontal angle
        self.vertical = 0 # vertical angle
        self.up = True

    def start(self):
        self.timer.start(500)

    def update(self):
        self.horizontal += 5
        
        if self.up:
            self.vertical += 10
            if self.vertical >= 90:
                self.up = False
        else:
            self.vertical -= 10
            if self.vertical <= 0:
                self.up = True

        App.ActiveDocument.Spreadsheet.set('B12:B12', str(self.vertical)) # set telscope angle
        App.ActiveDocument.Spreadsheet.set('B16:B16', str(self.horizontal)) # set telscope angle
        App.ActiveDocument.recompute()
        App.Console.PrintMessage('vertical: '+str(self.vertical)+'\n')
        App.Console.PrintMessage('horizontal: '+str(self.horizontal)+'\n')
        self.logangle.pop(0)
        self.logangle.append(float(self.vertical))
        self.line.set_ydata(self.logangle)
        plt.draw()

    def stop(self):
        self.timer.stop()


a = Animation()
a.start()
a.stop()
