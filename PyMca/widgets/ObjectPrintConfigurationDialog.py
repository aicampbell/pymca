#/*##########################################################################
# Copyright (C) 2004-2014 European Synchrotron Radiation Facility
#
# This file is part of the PyMca X-ray Fluorescence Toolkit developed at
# the ESRF by the Software group.
#
# This toolkit is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# PyMca is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# PyMca; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# PyMca follows the dual licensing model of Riverbank's PyQt and cannot be
# used as a free plugin for a non-free program.
#
# Please contact the ESRF industrial unit (industry@esrf.fr) if this license
# is a problem for you.
#############################################################################*/
__author__ = "V.A. Sole"
__license__ = "GPL"

from PyMca import PyMcaQt as qt

class ObjectPrintConfigurationWidget(qt.QWidget):
    def __init__(self, parent=None):
        super(ObjectPrintConfigurationWidget, self).__init__(parent)
        self.mainLayout = qt.QGridLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(2)
        hbox = qt.QWidget()
        hboxLayout = qt.QHBoxLayout(hbox)
        hboxLayout.setContentsMargins(0, 0, 0, 0)
        hboxLayout.setSpacing(2)
        label = qt.QLabel(self)
        label.setText("Units")
        label.setAlignment(qt.Qt.AlignCenter)
        self._pageButton = qt.QRadioButton()
        self._pageButton.setText("Page")
        self._inchButton = qt.QRadioButton()
        self._inchButton.setText("Inches")
        self._cmButton = qt.QRadioButton()
        self._cmButton.setText("Centimeters")
        self._buttonGroup = qt.QButtonGroup(self)
        self._buttonGroup.addButton(self._pageButton)
        self._buttonGroup.addButton(self._inchButton)
        self._buttonGroup.addButton(self._cmButton)
        self._buttonGroup.setExclusive(True)

        # units
        self.mainLayout.addWidget(label, 0, 0, 1, 4)
        #self.mainLayout.addWidget(self._pageButton, 0, 1)
        #self.mainLayout.addWidget(self._inchButton, 0, 2)
        #self.mainLayout.addWidget(self._cmButton, 0, 3)
        hboxLayout.addWidget(self._pageButton)
        hboxLayout.addWidget(self._inchButton)
        hboxLayout.addWidget(self._cmButton)
        self.mainLayout.addWidget(hbox, 1, 0, 1, 4)
        self._pageButton.setChecked(True)

        # xOffset
        label = qt.QLabel(self)
        label.setText("X Offset:")
        self.mainLayout.addWidget(label, 2, 0)
        self._xOffset = qt.QLineEdit(self)
        validator = qt.QDoubleValidator(None)
        self._xOffset.setValidator(validator)
        self._xOffset.setText("0.0")
        self.mainLayout.addWidget(self._xOffset, 2, 1)

        # yOffset
        label = qt.QLabel(self)
        label.setText("Y Offset:")
        self.mainLayout.addWidget(label, 2, 2)
        self._yOffset = qt.QLineEdit(self)
        validator = qt.QDoubleValidator(None)
        self._yOffset.setValidator(validator)
        self._yOffset.setText("0.0")
        self.mainLayout.addWidget(self._yOffset, 2, 3)

        # width
        label = qt.QLabel(self)
        label.setText("Width:")
        self.mainLayout.addWidget(label, 3, 0)
        self._width = qt.QLineEdit(self)
        validator = qt.QDoubleValidator(None)
        self._width.setValidator(validator)
        self._width.setText("0.5")
        self.mainLayout.addWidget(self._width, 3, 1)

        # height
        label = qt.QLabel(self)
        label.setText("Height:")
        self.mainLayout.addWidget(label, 3, 2)
        self._height = qt.QLineEdit(self)
        validator = qt.QDoubleValidator(None)
        self._height.setValidator(validator)
        self._height.setText("0.5")
        self.mainLayout.addWidget(self._height, 3, 3)

        # aspect ratio
        self._aspect = qt.QCheckBox(self)
        self._aspect.setText("Keep screen aspect ratio")
        self._aspect.setChecked(True)
        self.mainLayout.addWidget(self._aspect, 4, 1, 1, 2)

    def getParameters(self):
        ddict = {}
        if self._inchButton.isChecked():
            ddict['units'] = "inches"
        elif self._cmButton.isChecked():
            ddict['units'] = "centimeters"
        else:
            ddict['units'] = "page"

        ddict['xOffset'] = float(qt.safe_str(self._xOffset.text()))
        ddict['yOffset'] = float(qt.safe_str(self._yOffset.text()))
        ddict['width'] = float(qt.safe_str(self._width.text()))
        ddict['height'] = float(qt.safe_str(self._height.text()))
        
        if self._aspect.isChecked():
            ddict['keepAspectRatio'] = True
        else:
            ddict['keepAspectRatio'] = False
        return ddict

    def setParameters(self, ddict=None):
        if ddict is None:
            ddict = {}
        oldDict = self.getParameters()
        for key in ["units", "xOffset", "yOffset",
                    "width", "height", "keepAspectRatio"]:
            ddict[key] = ddict.get(key, oldDict[key])

        if ddict['units'].lower().startswith("inc"):
            self._inchButton.setChecked(True)
        elif ddict['units'].lower().startswith("c"):
            self._cmButton.setChecked(True)
        else:
            self._pageButton.setChecked(True)

        self._xOffset.setText("%s" % float(ddict['xOffset']))    
        self._yOffset.setText("%s" % float(ddict['yOffset']))    
        self._width.setText("%s" % float(ddict['width']))    
        self._height.setText("%s" % float(ddict['height']))
        if ddict['keepAspectRatio']:
            self._aspect.setChecked(True)
        else:
            self._aspect.setChecked(False)

class ObjectPrintConfigurationDialog(qt.QDialog):
    def __init__(self, parent=None, configuration=None):
        qt.QDialog.__init__(self, parent)
        self.setWindowTitle("Set print size preferences")
        if configuration is None:
            configuration = {"xOffset": 0.0,
                             "yOffset": 0.0,
                             "width": 0.5,
                             "height": 0.5,
                             "units": "page",
                             "keepAspectRatio": True}
        layout = qt.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.configurationWidget = ObjectPrintConfigurationWidget(self)
        hbox = qt.QWidget(self)
        hboxLayout = qt.QHBoxLayout(hbox)
        self.okButton = qt.QPushButton(hbox)
        self.okButton.setText("Accept")
        self.okButton.setAutoDefault(False)
        self.rejectButton = qt.QPushButton(hbox)
        self.rejectButton.setText("Dismiss")
        self.rejectButton.setAutoDefault(False)
        self.okButton.clicked.connect(self.accept)
        self.rejectButton.clicked.connect(self.reject)
        hboxLayout.setContentsMargins(0, 0, 0, 0)
        hboxLayout.setSpacing(2)
        hboxLayout.addWidget(qt.HorizontalSpacer(hbox))
        hboxLayout.addWidget(self.okButton)
        hboxLayout.addWidget(self.rejectButton)
        hboxLayout.addWidget(qt.HorizontalSpacer(hbox))
        layout.addWidget(self.configurationWidget)
        layout.addWidget(hbox)
        self.setPrintConfiguration(configuration)

    def setPrintConfiguration(self, configuration, printer=None):
        # TODO: Receive printer in order to be able to convert units
        # from page to inch and/or centimeters
        self.configurationWidget.setParameters(configuration)

    def getPrintConfiguration(self):
        return self.configurationWidget.getParameters()

if __name__ == "__main__":
    app = qt.QApplication([])
    w = ObjectPrintConfigurationDialog()
    if w.exec_():
        print(w.getPrintConfiguration())
