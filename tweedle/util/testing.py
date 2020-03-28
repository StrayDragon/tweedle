from dataclasses import dataclass


@dataclass(frozen=True)
class ClickOptionErrorPrefixes:
    # ref:
    miss = 'Missing option'
    non_exist = 'no such option'
    required = 'option requires an argument'
    choose = 'invalid choice'


@dataclass(frozen=True)
class ClickExceptionErrorPrefixes:
    # ref: https://github.com/pallets/click/blob/master/src/click/exceptions.py
    basic = 'Error'
    basic_hint = 'Try'
    bad_param = 'Invalid value'
    miss = 'missing parameter'
    no_such_opt_hint = 'Did your mean'
    no_such_opt = 'no such option'


class ClickExceptionErrorNo:
    # ref: https://github.com/pallets/click/blob/master/src/click/exceptions.py
    usage_error = 2
