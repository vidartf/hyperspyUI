# -*- coding: utf-8 -*-
# Copyright 2014-2016 The HyperSpyUI developers
#
# This file is part of HyperSpyUI.
#
# HyperSpyUI is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# HyperSpyUI is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with HyperSpyUI.  If not, see <http://www.gnu.org/licenses/>.
"""
Created on Sun Aug 21 19:59:04 2016

@author: Vidar Tonaas Fauske
"""


from python_qt_binding import QtGui, QtCore


# QAction.trigger/activate are not virtual, so cannot simply override.
# Instead, we shadow/wrap the triggered signal used by our python code
class AdvancedAction(QtGui.QAction):
    # The overloaded signal can take an optional argument `advanced`
    _triggered = QtCore.Signal([], [bool], [bool, bool])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super().triggered[bool].connect(self._trigger)

    @property
    def triggered(self):
        return self._triggered

    def _trigger(self, checked):
        mods = QtGui.QApplication.keyboardModifiers()
        advanced = mods & QtCore.Qt.AltModifier == QtCore.Qt.AltModifier
        self._triggered[bool, bool].emit(checked, advanced)
        self._triggered[bool].emit(checked)
        self._triggered.emit()

AdvancedAction.__init__.__doc__ = QtGui.QAction.__init__.__doc__
