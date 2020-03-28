# NOTE: will merge to `clickx` package or module
import logging

import click


def option_with_verbose_cnt(logger=None, *names, **kwargs):
    if not isinstance(logger, logging.Logger):
        logger = logging.getLogger(logger)

    if not names:
        names = [
            "--verbose",
            "-v",
        ]
    if isinstance(logger, str) and logger.startswith("-"):
        raise ValueError("Since click-log 0.2.0, the first argument must now " "be a logger.")
    kwargs.setdefault("count", True)
    kwargs.setdefault("is_eager", True)
    kwargs.setdefault("expose_value", False)

    def decorator(f):
        def _set_level(ctx, param, value):
            # if hasattr(ctx, 'obj'):
            #     print(ctx.obj, type(ctx.obj), type(param), param.human_readable_name, '=', value)
            if value == 0:
                logging.disable(logging.WARNING)
            elif value == 1:
                logger.setLevel(logging.INFO)
            else:
                logger.setLevel(logging.DEBUG)

        return click.option(*names, callback=_set_level, **kwargs)(f)

    return decorator
