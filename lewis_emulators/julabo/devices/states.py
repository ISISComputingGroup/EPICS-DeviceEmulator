# -*- coding: utf-8 -*-
# *********************************************************************
# plankton - a library for creating hardware device simulators
# Copyright (C) 2016-2017 European Spallation Source ERIC
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# *********************************************************************

from lewis.core.statemachine import State
from lewis.core import approaches


class DefaultNotCirculatingState(State):
    pass


class DefaultCirculatingState(State):
    def in_state(self, dt):
        # Approach target temperature at a set rate
        self._context.temperature = approaches.linear(
            self._context.temperature,
            self._context.set_point_temperature,
            self._context.heating_power / 60.0,
            dt,
        )
