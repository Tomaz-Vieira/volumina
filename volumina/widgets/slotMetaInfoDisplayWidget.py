###############################################################################
#   volumina: volume slicing and editing library
#
#       Copyright (C) 2011-2014, the ilastik developers
#                                <team@ilastik.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the Lesser GNU General Public License
# as published by the Free Software Foundation; either version 2.1
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# See the files LICENSE.lgpl2 and LICENSE.lgpl3 for full text of the
# GNU Lesser General Public License version 2.1 and 3 respectively.
# This information is also available on the ilastik web site at:
# 		   http://ilastik.org/license/
###############################################################################
import os

import sip
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget


class SlotMetaInfoDisplayWidget(QWidget):
    """
    Simple display widget for a slot's meta-info (shape, axes, dtype).
    """

    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi(os.path.splitext(__file__)[0] + ".ui", self)
        self._slot = None

    def initSlot(self, slot):
        if self._slot is not slot:
            if self._slot:
                self._slot.unregisterMetaChanged(self._refresh)
            self._slot = slot
            slot.notifyMetaChanged(self._refresh)
            #slot.notifyReady(self._refresh)
        self._refresh()

    def _refresh(self, *args):
        shape = axes = dtype = ""
        if self._slot.ready():
            shape = str(tuple(self._slot.meta.getOriginalShape()))
            axes = "".join(self._slot.meta.getOriginalAxisKeys())
            dtype = self._slot.meta.dtype.__name__
        self._do_refresh(shape, axes, dtype)

    def _do_refresh(self, shape, axes, dtype):
        if not sip.isdeleted(self.shapeDisplay):
            self.shapeDisplay.setText(shape)
            self.axisOrderDisplay.setText(axes)
            self.dtypeDisplay.setText(dtype)

class OutputSlotMetaInfoDisplayWidget(SlotMetaInfoDisplayWidget):
    def _refresh(self, *args):
        shape = axes = dtype = ""
        if self._slot.ready():
            shape = str(tuple(self._slot.meta.shape))
            axes = "".join(self._slot.meta.getAxisKeys())
            dtype = self._slot.meta.dtype.__name__
        self._do_refresh(shape, axes, dtype)
