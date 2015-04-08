# -*- coding: utf-8 -*-
"""
Created on Tue Nov 25 02:10:29 2014

@author: Vidar Tonaas Fauske
"""

import os
import sys

from python_qt_binding import QtGui, QtCore
import hyperspyui.info
from hyperspyui.singleapplication import get_app


# TODO: Autohide toolbars w.r.t. signal type. (maybe?)
# TODO: Add selection groups for signals by hierarchy in DataViewWidget
# TODO: Make sure everything records / plays back code
# TODO: MPL artist editor via traitsui with custom handler
# TODO: Batch processing dialog (browse + drop&drop target)
# TODO: Editor threading + parallell processing utils (w/batch input)
# TODO: Layout save/restore (ignorable settings (_settings?))
# TODO: Fix unloading of plugins' tools
# TODO: Add xray element find tool
# TODO: Add xray 3rd state: Element present, but not used for maps
# TODO: Add xray background window tool for modifying those by auto
# TODO: Add quantification button. Needs k-factor setup.
# TODO: Add EELSDB widget plugin
# TODO: Create contributed plugins repository with UI integrated hot-load
# TODO: Auto-resize font in Periodic table
# TODO: Utilities to combine signals into stack and reverse
# TODO: Make editor tabs drag&dropable + default to all in one
# TODO: Make data type changer handle RGBX data types.


# import logging
# logging.basicConfig(level=logging.DEBUG)


def main():
    exe_dir, exe_name = os.path.split(sys.executable)
    if exe_name.startswith('pythonw'):
        sys.stdout = sys.stderr = open(
            os.path.dirname(__file__) + './hyperspyui.log', 'w')
    # TODO: Make single/multi a setting
    app = get_app('hyperspyui')     # Make sure we only have a single instance

    QtCore.QCoreApplication.setApplicationName("HyperSpyUI")
    QtCore.QCoreApplication.setOrganizationName("Hyperspy")
    QtCore.QCoreApplication.setApplicationVersion(hyperspyui.info.version)

    # Create and display the splash screen
    splash_pix = QtGui.QPixmap(
        os.path.dirname(__file__) + './images/splash.png')
    splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()

    # Need to have import here, as it can take some time, so should happen
    # after displaying splash
    from hyperspyui.mainwindow import MainWindow

    form = MainWindow()
    app.messageAvailable.connect(form.handleSecondInstance)
    form.showMaximized()

    splash.finish(form)

    app.exec_()

if __name__ == "__main__":
    sys.path.append(os.path.dirname(__file__) + './')
    main()