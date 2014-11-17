# -*- coding: utf-8 -*-
"""
Created on Mon Nov 17 14:16:41 2014

@author: vidarton
"""



from python_qt_binding import QtGui, QtCore
from QtCore import *
from QtGui import *

import types

class Worker(QObject):
    progress = QtCore.Signal(int)
    finished = QtCore.Signal()
    error = QtCore.Signal(str)
    
    def __init__(self, run):
        super(Worker, self).__init__()
        self.run_function = run
    
    def process(self):
        if isinstance(self.run_function, types.GeneratorType):
            p = 0
            self.progress.emit(p)
            while p < 100:
                p = self.run_function()
                self.progress.emit(p)
        else:
            self.run_function()
        self.progress.emit(100)
        self.finished.emit()
        

class ProgressThread(QObject):
    """
    Executes a user provided function in a new thread, and pops up a
    QProgressBar until it finishes. To have an updating progress bar,
    have the provided function be a generator, and yield completion rate
    in percent (int from 0 to 100).
    """

    pool = []    
    def add_to_pool(instance):
        ProgressThread.pool.append(instance)
    
    def remove_from_pool(instance):
        ProgressThread.pool.remove(instance)
    
    def __init__(self, parent, run, finished=None, label=None, title="Processing"):
        super(ProgressThread, self).__init__()
        
        # Create thread/objects
        self.thread = QThread()
        worker = Worker(run)
        worker.moveToThread(self.thread)
        ProgressThread.add_to_pool(self)
        
        # Create progress bar.
        progressbar = QProgressDialog(parent)
        if isinstance(run, types.GeneratorType):
            progressbar.setMinimum(0)
            progressbar.setMaximum(100)
        else:
            progressbar.setMinimum(0)
            progressbar.setMaximum(0)
        progressbar.hide()
        progressbar.setWindowTitle(title)
        progressbar.setLabelText(label)
        progressbar.setCancelButtonText(None)
             
        
        # Connect error reporting
        self.connect(worker, SIGNAL('error(QString)'), self.errorString)
        
        # Start up
        self.connect(self.thread, SIGNAL('started()'), progressbar.exec_)
        self.connect(self.thread, SIGNAL('started()'), worker.process)
        
        # Clean up
        self.connect(worker, SIGNAL('finished()'), progressbar.close)
        self.connect(worker, SIGNAL('finished()'), self.thread.quit)
        self.connect(worker, SIGNAL('finished()'), worker.deleteLater)
        self.connect(self.thread, SIGNAL('finished()'), self.thread.deleteLater)
        
        def remove_ref():
            ProgressThread.remove_from_pool(self)
        
        self.connect(self.thread, SIGNAL('finished()'), remove_ref)
        
        if finished is not None:
            self.connect(worker, SIGNAL('finished()'), finished)
        
        # Progress reporting
        self.connect(worker, SIGNAL('progress(int)'), progressbar.setValue)
        
        # Need to keep ref so they stay in mem
        self.progressbar = progressbar
        self.worker = worker
        
    def errorString(self, error):
        print error
        
    def run(self):
        self.thread.start()