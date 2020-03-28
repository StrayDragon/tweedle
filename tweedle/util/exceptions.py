# TODO: need to think again
# NOTE: Imitate `click` exceptions design to make it:
#           - [ ] has type annotation
#           - [ ] has more options
#           - [ ] easy to test
#           - [ ] prepare for i18n
#           - [ ] no longer compatible with python2

from pathlib import Path


def i18n_get_value(key: str):
    raise NotImplementedError


class ErrorTemplates:
    BASIC = "Error: {}"
    USAGE_WRONG = "Wrong usage: {}"
    PARAMS_WRONG = "Invalid value: {}"
    PARAMS_MISSING = "Missing value: {}"
    FILE_WRONG = "Could not open file: {}"

    @classmethod
    def from_i18n(cls, config_path):
        config_path = Path(config_path)
        this = cls()
        this.basic = i18n_get_value('basic')
        this.usage_error = i18n_get_value('usage_error')

        pass


class TweedleCLIException(Exception):
    def __init__(self, message: str, message_template: str = ErrorTemplates.BASIC):
        self.message = message
        self.message_template = message_template

    def show(self, file=None):
        if file is None:
            raise NotImplementedError
