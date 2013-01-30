#!/usr/bin/env python
############################################################################
#
#  Copyright (C) 2006-2007 Trolltech ASA. All rights reserved.
#
#  This file is part of the example classes of the Qt Toolkit.
#
#  This file may be used under the terms of the GNU General Public
#  License version 2.0 as published by the Free Software Foundation
#  and appearing in the file LICENSE.GPL included in the packaging of
#  this file.  Please review the following information to ensure GNU
#  General Public Licensing requirements will be met:
#  http://trolltech.com/products/qt/licenses/licensing/opensource/
#
#  If you are unsure which license is appropriate for your use, please
#  review the following information:
#  http://trolltech.com/products/qt/licenses/licensing/licensingoverview
#  or contact the sales department at sales@trolltech.com.
#
#  In addition, as a special exception, Trolltech gives you certain
#  additional rights. These rights are described in the Trolltech GPL
#  Exception version 1.0, which can be found at
#  http://www.trolltech.com/products/qt/gplexception/ and in the file
#  GPL_EXCEPTION.txt in this package.
#
#  In addition, as a special exception, Trolltech, as the sole copyright
#  holder for Qt Designer, grants users of the Qt/Eclipse Integration
#  plug-in the right for the Qt/Eclipse Integration to link to
#  functionality provided by Qt Designer and its related libraries.
#
#  Trolltech reserves all rights not expressly granted herein.
#
#  Trolltech ASA (c) 2007
#
#  This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
#  WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#
############################################################################
# This is only needed for Python v2 but is harmless for Python v3.
#import sip
#sip.setapi('QVariant', 2)
from PySide import QtCore, QtGui
import systray_rc

from subprocess import call
from threading import Thread
from threading import Event
from time import sleep

class PulseAudio:
    pa = "pulseaudio"
    
    def __init__(self):
        print "Pulse"

    def check(self):
        retval = call([self.pa, "--check"])
        #print "Pulse checked %d" % (retval)
        return retval

    def start(self):
        retval = call([self.pa, "--start"])
        print "Pulse started %d" % (retval)

    def stop(self):
        retval = call([self.pa, "--kill"])
        print "Pulse stopped %d" % (retval)

class PAmonitor(QtCore.QThread):
    dataReady = QtCore.Signal(int)
    
    def __init__ (self,pa,win,interval=1):
        QtCore.QThread.__init__(self)
        self.pa=pa
        self.win=win
        self.interval=interval

    def run(self):
        while True:
            state=self.pa.check()
            self.dataReady.emit(state)
            sleep(self.interval)

        
class Window(QtGui.QDialog):
    def __init__(self):
        super(Window, self).__init__()
        self.pa = PulseAudio()
        self.createIconGroupBox()
        self.createActions()
        self.createTrayIcon()
        self.iconComboBox.currentIndexChanged[int].connect(self.setIcon)
        self.trayIcon.activated.connect(self.iconActivated)
        self.setIcon(0)
        self.trayIcon.show()
        self.monitor = PAmonitor(self.pa, self)
        self.monitor.dataReady.connect(self.status, QtCore.Qt.QueuedConnection)
        self.monitor.start()

    def start(self):
        print "start"
        self.pa.start()

    def stop(self):
        print "stop"
        self.pa.stop()

    def status(self, state):
        self.setIcon(state)

    def setIcon(self, index):
        #print index
        icon = self.iconComboBox.itemIcon(index)
        self.trayIcon.setIcon(icon)
        self.setWindowIcon(icon)
        self.trayIcon.setToolTip(self.iconComboBox.itemText(index))

    def iconActivated(self, reason):
        if reason in (QtGui.QSystemTrayIcon.Trigger, QtGui.QSystemTrayIcon.DoubleClick):
            if self.pa.check() == 0:
                self.pa.stop()
            else:
                self.pa.start()

    def createIconGroupBox(self):
        self.iconGroupBox = QtGui.QGroupBox("Tray Icon")
        self.iconLabel = QtGui.QLabel("Icon:")
        self.iconComboBox = QtGui.QComboBox()
        self.iconComboBox.addItem(QtGui.QIcon('images/running.svg'), "pulseaudio running")
        self.iconComboBox.addItem(QtGui.QIcon('images/stopped.svg'), "pulseaudio stopped")
        self.showIconCheckBox = QtGui.QCheckBox("Show icon")
        self.showIconCheckBox.setChecked(True)
        iconLayout = QtGui.QHBoxLayout()
        iconLayout.addWidget(self.iconLabel)
        iconLayout.addWidget(self.iconComboBox)
        iconLayout.addStretch()
        iconLayout.addWidget(self.showIconCheckBox)
        self.iconGroupBox.setLayout(iconLayout)

    def quit(self):
        self.monitor.exit()
        QtGui.qApp.quit();

    def createActions(self):
        self.startAction = QtGui.QAction("Start", self,
                triggered=self.start)
        self.stopAction = QtGui.QAction("Stop", self,
                triggered=self.stop)
        self.quitAction = QtGui.QAction("&Quit", self,
                triggered=self.quit)

    def createTrayIcon(self):
         self.trayIconMenu = QtGui.QMenu(self)
         self.trayIconMenu.addAction(self.startAction)
         self.trayIconMenu.addAction(self.stopAction)
         self.trayIconMenu.addSeparator()
         self.trayIconMenu.addAction(self.quitAction)
         self.trayIcon = QtGui.QSystemTrayIcon(self)
         self.trayIcon.setContextMenu(self.trayIconMenu)

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    if not QtGui.QSystemTrayIcon.isSystemTrayAvailable():
        QtGui.QMessageBox.critical(None, "Systray",
                "I couldn't detect any system tray on this system.")
        sys.exit(1)
    QtGui.QApplication.setQuitOnLastWindowClosed(False)
    window = Window()
    print "start"
    #window.show()
    sys.exit(app.exec_())
