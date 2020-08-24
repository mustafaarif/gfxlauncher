#!/bin/env python
#
# LUNARC HPC Desktop On-Demand graphical launch tool
# Copyright (C) 2017-2020 LUNARC, Lund University
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
Launch settings singleton

Implements a simple singleton for storing launch options.
"""

from .singleton import *

@Singleton
class LaunchSettings:
    def __init__(self):
        self.args = None
