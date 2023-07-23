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
        self.threshold_spin = bind_with_config(sizer.addLabeledControl(_('Threshold value for triggering (in characters)'), wx.SpinCtrl, min=500, max=sys.maxsize), 'threshold')


def add_settings(on_save_callback):
    SpeechFilterSettingsPanel.on_save_callback = on_save_callback
    gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(SpeechFilterSettingsPanel)


def remove_settings():
    gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(SpeechFilterSettingsPanel)


def open_settings():
    wx.CallAfter(gui.mainFrame._popupSettingsDialog, gui.NVDASettingsDialog, SpeechFilterSettingsPanel)
