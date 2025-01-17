#!/bin/env python
#
# LUNARC HPC Desktop On-Demand graphical launch tool
# Copyright (C) 2017-2021 LUNARC, Lund University
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Resource specification window

This module implements the resource specification window.
"""

import os
import getpass
from datetime import datetime

from PyQt5 import Qt, QtCore, QtGui, QtWidgets, uic

from . import jobs
from . import lrms
from . import remote
from . import settings
from . import config
from . import launcher

class ResourceSpecWindow(QtWidgets.QWidget):
    """Resource specification window"""

    def __init__(self, parent=None):
        """Resource window constructor"""

        super(ResourceSpecWindow, self).__init__(parent, QtCore.Qt.Window)

        self.default_job = jobs.Job()
        self.default_job.memory = 3200
        self.default_job.cpusPerNode = 1
        self.default_job.tasksPerNode = 1
        self.default_job.nodeCount = 1

        self.old_tasks_per_node = -1

        self.tool_path = settings.LaunchSettings.create().tool_path
        ui_path = os.path.join(self.tool_path, "ui")

        uic.loadUi(os.path.join(ui_path, "resource_specification.ui"), self)

        self.parent = parent

        self.set_data()

    def set_data(self, check_boxes=True):
        """Assign values to controls"""

        self.jobNameEdit.setText(self.parent.job_name)
        self.exclusiveCheck.setChecked(self.parent.exclusive)

        if int(self.parent.memory)>=0:
            self.memoryPerCpuEdit.setText(str(self.parent.memory))
            self.memoryPerCpuEdit.setVisible(True)
            self.memoryPerCpuEdit.setEnabled(True)
            self.specifyMemoryCheck.setChecked(True)
        else:
            self.memoryPerCpuEdit.setText('-1')
            self.memoryPerCpuEdit.setVisible(False)
            self.memoryPerCpuEdit.setEnabled(False)
            self.specifyMemoryCheck.setChecked(False)

        if int(self.parent.tasks_per_node)>=0:
            self.tasksPerNodeSpin.setValue(int(self.parent.tasks_per_node))
            self.tasksPerNodeSpin.setVisible(True)
            self.tasksPerNodeSpin.setEnabled(True)
            self.specifyTasksPerNodeCheck.setChecked(True)
        else:
            self.tasksPerNodeSpin.setValue(-1)
            self.tasksPerNodeSpin.setVisible(False)
            self.tasksPerNodeSpin.setEnabled(False)
            self.specifyTasksPerNodeCheck.setChecked(False)

        #if int(self.parent.count)>=0:
        #    self.numberOfNodesSpin.setValue(int(self.parent.count))
        #    self.numberOfNodesSpin.setEnabled(True)
        #    self.specifyNumberOfNodesCheck.setChecked(True)
        #else:
        #    self.numberOfNodesSpin.setValue(-1)
        #    self.numberOfNodesSpin.setEnabled(False)
        #    self.specifyNumberOfNodesCheck.setChecked(False)

        #if int(self.parent.cpus_per_task)>=0:
        #    self.cpuPerTaskSpin.setValue(int(self.parent.cpus_per_task))
        #    self.cpuPerTaskSpin.setEnabled(True)
        #    self.specifyCPUsPerTaskCheck.setChecked(True)
        #else:
        #    self.cpuPerTaskSpin.setValue(-1)
        #    self.cpuPerTaskSpin.setEnabled(False)
        #    self.specifyCPUsPerTaskCheck.setChecked(False)

        #self.noRequeueCheck.setChecked(self.parent.no_requeue) 

    def get_data(self):
        """Get values from controls"""

        try:
            self.parent.job_name = self.jobNameEdit.text()
            self.parent.memory = int(self.memoryPerCpuEdit.text())
            self.parent.exclusive = self.exclusiveCheck.isChecked()
            self.parent.tasks_per_node = self.tasksPerNodeSpin.value()
            #self.parent.count = self.numberOfNodesSpin.value()
            #self.parent.cpus_per_task = self.cpuPerTaskSpin.value()
            #self.parent.no_requeue = self.noRequeueCheck.isChecked()
        except ValueError:
            pass

    @QtCore.pyqtSlot()
    def on_exclusiveCheck_clicked(self):
        if self.exclusiveCheck.isChecked():
            self.old_tasks_per_node = self.parent.tasks_per_node
            self.parent.tasks_per_node = -1
            self.parent.exclusive = True
        else:
            self.parent.tasks_per_node = self.old_tasks_per_node
            self.parent.exclusive = False

        self.set_data()


    @QtCore.pyqtSlot()
    def on_specifyMemoryCheck_clicked(self):
        if self.specifyMemoryCheck.isChecked():
            self.memoryPerCpuEdit.setEnabled(True)
            self.memoryPerCpuEdit.setVisible(True)
            self.memoryPerCpuEdit.setText(str(self.default_job.memory))
        else:
            self.memoryPerCpuEdit.setEnabled(False)
            self.memoryPerCpuEdit.setVisible(False)
            self.memoryPerCpuEdit.setText("-1")

    @QtCore.pyqtSlot()
    def on_specifyTasksPerNodeCheck_clicked(self):
        if self.specifyTasksPerNodeCheck.isChecked():
            self.tasksPerNodeSpin.setEnabled(True)
            self.tasksPerNodeSpin.setVisible(True)
            self.tasksPerNodeSpin.setValue(self.default_job.tasksPerNode)
        else:
            self.tasksPerNodeSpin.setEnabled(False)
            self.tasksPerNodeSpin.setVisible(False)
            self.tasksPerNodeSpin.setValue(-1)

    """     @QtCore.pyqtSlot()
        def on_specifyNumberOfNodesCheck_clicked(self):
            if self.specifyNumberOfNodesCheck.isChecked():
                self.numberOfNodesSpin.setEnabled(True)
                self.numberOfNodesSpin.setValue(self.default_job.nodeCount)
            else:
                self.numberOfNodesSpin.setEnabled(False)
                self.numberOfNodesSpin.setValue(-1)
    """
    """     @QtCore.pyqtSlot()
        def on_specifyCPUsPerTaskCheck_clicked(self):
            if self.specifyCPUsPerTaskCheck.isChecked():
                self.cpuPerTaskSpin.setEnabled(True)
                self.cpuPerTaskSpin.setValue(self.default_job.cpusPerNode)
            else:
                self.cpuPerTaskSpin.setEnabled(False)
                self.cpuPerTaskSpin.setValue(-1)
    """

    @QtCore.pyqtSlot()
    def on_okButton_clicked(self):
        """Event method for OK button"""
        self.get_data()
        self.close()

    @QtCore.pyqtSlot()
    def on_cancelButton_clicked(self):
        """Event method for Cancel button"""
        self.close()

