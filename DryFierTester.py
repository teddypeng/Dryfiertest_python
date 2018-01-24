# -*- coding: utf-8 -*-
# teddy.peng
# Form implementation generated from reading ui file 'DryFierTester.ui'
#
# Created: Fri Sep  8 12:28:55 2017
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!
import sys
import RPi.GPIO as GPIO
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *  
from PyQt4.QtGui import *  
import time      

GPIO.setmode(GPIO.BCM) # Specifies referring to GPIO pins by Broadcom SOC channel
GPIO.setwarnings(False) #Disables the Warning


try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0
    
# instantiate
config = ConfigParser()
config.read('test.ini')

int_val = config.getint('section_a', 'int_val')
global cycle, cycle_set  
cycle =  int_val
cycle_set = 0


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DryFieTester(object):
    def __int__(self):
        super().__init__()
        
    def setupUi(self, DryFieTester):
        
        DryFieTester.setObjectName(_fromUtf8("DryFieTester"))
        DryFieTester.resize(800, 600)
        DryFieTester.setWindowOpacity(1.0)
        self.centralwidget = QtGui.QWidget(DryFieTester)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.CycleSet = QtGui.QSpinBox(self.centralwidget)
        self.CycleSet.setGeometry(QtCore.QRect(70, 160, 311, 31))
        self.CycleSet.setMaximum(500000)
        self.CycleSet.setMinimum(0)
        self.CycleSet.setProperty("value", 0)
        self.CycleSet.setObjectName(_fromUtf8("CycleSet"))
        self.StartButton = QtGui.QPushButton(self.centralwidget)
        self.StartButton.setGeometry(QtCore.QRect(440, 370, 93, 32))
        self.StartButton.setObjectName(_fromUtf8("StartButton"))
        self.CycleCount = QtGui.QLCDNumber(self.centralwidget)
        self.CycleCount.setGeometry(QtCore.QRect(70, 90, 311, 61))
        self.CycleCount.setObjectName(_fromUtf8("CycleCount"))
        self.CycleCount.display(cycle)
        self.StopButton = QtGui.QPushButton(self.centralwidget)
        self.StopButton.setGeometry(QtCore.QRect(550, 370, 93, 32))
        self.StopButton.setObjectName(_fromUtf8("StopButton"))
        self.ClearButton = QtGui.QPushButton(self.centralwidget)
        self.ClearButton.setGeometry(QtCore.QRect(390, 120, 93, 32))
        self.ClearButton.setObjectName(_fromUtf8("ClearButton"))
        DryFieTester.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(DryFieTester)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 29))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuS = QtGui.QMenu(self.menubar)
        self.menuS.setObjectName(_fromUtf8("menuS"))
        DryFieTester.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(DryFieTester)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        DryFieTester.setStatusBar(self.statusbar)
        self.menuS.addSeparator()
        self.menubar.addAction(self.menuS.menuAction())
        #self.worker = Main(start_signal)
        #QtCore.QObject.connect(self.StartButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.start)
        self.retranslateUi(DryFieTester)
        QtCore.QObject.connect(self.ClearButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.clear) # Function to be fired on Button Click Action
        QtCore.QObject.connect(self.StartButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.GPIO23On)
        QtCore.QObject.connect(self.StopButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.GPIO23Off)
        QtCore.QObject.connect(self.CycleSet, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.cycleSet)
        QtCore.QMetaObject.connectSlotsByName(DryFieTester)
        
    def clear(self):
        self.CycleCount.display(0)
        global  cycle 
        cycle = 0   
         
    def GPIO23On(self):  # Function declaration which fires on respective button click
        GPIO.setup(23, GPIO.OUT)  #Set GPIO Pin as Output 
        GPIO.output(23, 1) # Turns the GPIO logical High
        print("GPIO23 has been turned ON in OUTPUT Mode") #Append the current GPIO pin status
        global bt2
        bt2 = True
        self.workThread = WorkThread() #define the workthread
        self.workThread.trigger.connect(self.countTime) # connect trigger with countTime function
        self.workThread.start()  #start the workthread run method
        

    def countTime(self):  
        global  cycle 
        cycle+=1
        self.CycleCount.display(cycle)
        config.read('test.ini')
        config.set('section_a', 'int_val', str(cycle))   # update existing value must strng
        with open('test.ini', 'w') as configfile:  # save to a file
            config.write(configfile)
        print(cycle)

    
    def GPIO23Off(self): # Function declaration which fires on respective button click
        GPIO.setup(23, GPIO.OUT) #Set GPIO Pin as Output 
        GPIO.output(23, 0) # Turns the GPIO logical Low
        GPIO.setup(24, GPIO.OUT)
        GPIO.output(24, 0)
        global bt2
        bt2 = False
        print("GPIO23 has been turned OFF in OUTPUT Mode")
        
        
    def cycleSet(self):
        global cycle_set
        cycle_set = self.CycleSet.value()
        
        print(cycle_set)
        
    def retranslateUi(self, DryFieTester):
        DryFieTester.setWindowTitle(QtGui.QApplication.translate("DryFieTester", "DryFieTester", None, QtGui.QApplication.UnicodeUTF8))
        self.StartButton.setText(QtGui.QApplication.translate("DryFieTester", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.StopButton.setText(QtGui.QApplication.translate("DryFieTester", "Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.ClearButton.setText(QtGui.QApplication.translate("DryFieTester", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.menuS.setTitle(QtGui.QApplication.translate("DryFieTester", "Dry Fier Tester", None, QtGui.QApplication.UnicodeUTF8))

class WorkThread(QThread):  
    trigger = pyqtSignal() #init trigger signal
    global bt2
    bt2 = True
    def __int__(self):  
        super(WorkThread,self).__init__() 
    def run(self):
            while(bt2 != False): 
                    global cycle_set, cycle
                    if cycle_set > cycle:
                        GPIO.setup(24, GPIO.OUT)  #Set GPIO Pin as Output 
                        GPIO.output(24,1) # Turns the GPIO logical High
                        print("GPIO24 has been turned ON in OUTPUT Mode")
                        time.sleep(1.5)
                        GPIO.output(24, 0) 
                        print("GPIO24 has been turned OFF in OUTPUT Mode")
                        self.trigger.emit() #send trigger msg
                        time.sleep(1)
                    else:
                        break
 
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    DryFieTester = QtGui.QMainWindow()
    ui = Ui_DryFieTester()
    ui.setupUi(DryFieTester)
    DryFieTester.show()
    timer=QTimer()  
    workThread=WorkThread()
    sys.exit(app.exec_())

