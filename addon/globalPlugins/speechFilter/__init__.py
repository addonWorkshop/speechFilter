import addonHandler
import api
import config
import globalPluginHandler
from scriptHandler import script
from speech import commands, speech
import speechViewer
import ui

from . import interface

addonHandler.initTranslation()

beep_command = commands.BeepCommand(200, 100)

config.conf.spec['speechFilter'] = {
    'threshold': 'integer(min=500, default=5000)',
}


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    scriptCategory = _('Speech Filter')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config.conf['speechFilter']
        self.validate_config(self.config)
        interface.add_settings(self.on_save_callback)
        self.old_speak = speech.speak
        speech.speak = self.speak_decorator(speech.speak)
        self.last_sequence_with_long_text = None

    def validate_config(self, section):
        '''Tries to get all keys from a section, and recursively from nested sections.
        On validation errors, it removes the incorrect value.
        '''
        for key in list(section):
            try:
                value = section[key]
            except (configobj.validate.ValidateError, KeyError):
                for profile in section.profiles:
                    profile.pop(key, None)
                section._cache.pop(key, None)
            if isinstance(value, config.AggregatedSection):
                self.validate_config(value)

    def on_save_callback(self):
        pass

    def process_long_text(self, text):
        return [
            beep_command,
            _('A lot of text.')
        ]

    def speak_decorator(self, func):
        def wrapper(sequence, *args, **kwargs):
            new_sequence = []
            long_text_detected = False
            for item in sequence:
                if isinstance(item, str) and len(item) >= self.config['threshold']:
                    long_text_detected = True
                    new_sequence.extend(self.process_long_text(item))
                else:
                    new_sequence.append(item)
            if long_text_detected:
                self.last_sequence_with_long_text = sequence
            return func(new_sequence, *args, **kwargs)
        return wrapper

    def terminate(self):
        speech.speak = self.old_speak

    def get_text_from_sequence(self, sequence):
        return speechViewer.SPEECH_ITEM_SEPARATOR.join([x for x in sequence if isinstance(x, str)])

    @script(
        description=_('Copy last filtered text')
    )
    def script_copy_last_filtered_text(self, gesture):
        if self.last_sequence_with_long_text is None:
            ui.message('Nothing has been filtered')
            return
        text = self.get_text_from_sequence(self.last_sequence_with_long_text)
        api.copyToClip(text)
        ui.message(
            _('{chars_amount} characters copied.').format(
                chars_amount=len(text)
            )
        )
