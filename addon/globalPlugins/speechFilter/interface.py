# Copyright © 2024 Danil Pylaev <danstiv@yandex.ru>.
#
# This file is part of speechFilter NVDA-addon
# (see https://github.com/Danstiv/speechFilter).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Lesser General Public License for more details.
#
#You should have received a copy of the GNU Lesser General Public License
#along with this program. If not, see <http://www.gnu.org/licenses/>.

import sys

import addonHandler
import config
import gui
import wx

from .interface_helpers import ConfigBoundSettingsPanel, bind_with_config

addonHandler.initTranslation()


class SpeechFilterSettingsPanel(ConfigBoundSettingsPanel):
    title = addonHandler.getCodeAddon().manifest['summary']

    def makeSettings(self, settings_sizer):
        self.config = config.conf['speechFilter']
        sizer = gui.guiHelper.BoxSizerHelper(self, sizer=settings_sizer)
        self.threshold_spin = bind_with_config(sizer.addLabeledControl(_('Threshold value for triggering (in characters)'), wx.SpinCtrl, min=500, max=10**7), 'threshold')


def add_settings(on_save_callback):
    SpeechFilterSettingsPanel.on_save_callback = on_save_callback
    gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(SpeechFilterSettingsPanel)


def remove_settings():
    gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(SpeechFilterSettingsPanel)


def open_settings():
    wx.CallAfter(gui.mainFrame._popupSettingsDialog, gui.NVDASettingsDialog, SpeechFilterSettingsPanel)
