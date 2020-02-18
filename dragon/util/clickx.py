import os
import stat
from functools import update_wrapper, wraps
from importlib import import_module

import click
from click._compat import filename_to_ui


class ClickDefaultErrorOutput(object):
    MISS_OPT = 'Missing option'
    NO_OPT = 'no such option:'
    RQR_OPT = 'option requires an argument'
    CHOOSE_OPT = 'invalid choice'


class Colors:
    Black = 'black'
    Gray = 'black'
    Green = 'green'
    Yellow = 'yellow'
    Blue = 'blue'
    Magenta = 'magenta'
    Cyan = 'cyan'
    White = 'white'
    LightGray = 'white'
    RESET = 'reset'


def pass_props(f):
    """refer: https://click.palletsprojects.com/en/7.x/commands/#nested-handling-and-contexts"""
    @click.pass_context
    def new_fn(ctx, *args, **kwargs):
        return ctx.invoke(f, ctx.props, *args, **kwargs)

    return update_wrapper(new_fn, f)


class _Missing(object):
    def __repr__(self):
        return "no value"

    def __reduce__(self):
        return "_missing"


_missing = _Missing()


class cached_property(property):
    """A decorator that converts a function into a lazy property.  The
    function wrapped is called the first time to retrieve the result
    and then that calculated result is used the next time you access
    the value::
        class Foo(object):
            @cached_property
            def foo(self):
                # calculate something important here
                return 42
    The class has to have a `__dict__` in order for this property to
    work.

    FROM: https://github.com/pallets/werkzeug/blob/master/src/werkzeug/_internal.py#L56
    FIXME: add license
    """

    # implementation detail: A subclass of python's builtin property
    # decorator, we override __get__ to check for a cached value. If one
    # chooses to invoke __get__ by hand the property will still work as
    # expected because the lookup logic is replicated in __get__ for
    # manual invocation.

    def __init__(self, func, name=None, doc=None):
        self.__name__ = name or func.__name__
        self.__module__ = func.__module__
        self.__doc__ = doc or func.__doc__
        self.func = func

    def __set__(self, obj, value):
        obj.__dict__[self.__name__] = value

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        value = obj.__dict__.get(self.__name__, _missing)
        if value is _missing:
            value = self.func(obj)
            obj.__dict__[self.__name__] = value
        return value


class LazyGroup(click.Group):
    """
    A click Group that imports the actual implementation only when
    needed.  This allows for more resilient CLIs where the top-level
    command does not fail when a subcommand is broken enough to fail
    at import time.


    FROM: https://github.com/indico/indico/blob/master/indico/cli/util.py#L95
    FIXME: add license
    """
    def __init__(self, import_name: str, **kwargs):
        self._import_name = import_name
        super(LazyGroup, self).__init__(**kwargs)

    @cached_property
    def _impl(self):
        module, name = self._import_name.split(':', 1)
        return getattr(import_module(module), name)

    def get_command(self, ctx, cmd_name):
        return self._impl.get_command(ctx, cmd_name)

    def list_commands(self, ctx):
        return self._impl.list_commands(ctx)

    def invoke(self, ctx):
        return self._impl.invoke(ctx)

    def get_usage(self, ctx):
        return self._impl.get_usage(ctx)

    def get_params(self, ctx):
        return self._impl.get_params(ctx)


class Path(click.Path):
    def convert(self, value, param, ctx):
        rv = value

        is_dash = self.file_okay and self.allow_dash and rv in (b'-', '-')

        if not is_dash:
            if self.resolve_path:
                rv = os.path.realpath(rv)

            try:
                st = os.stat(rv)
            except OSError:
                if not self.exists:
                    return self.coerce_path_result(rv)
                self.fail(
                    click.style('%s "%s" does not exist.' % (self.path_type, filename_to_ui(value)),
                                fg='red'),
                    param,
                    ctx,
                )

            if not self.file_okay and stat.S_ISREG(st.st_mode):
                self.fail('%s "%s" is a file.' % (self.path_type, filename_to_ui(value)), param,
                          ctx)
            if not self.dir_okay and stat.S_ISDIR(st.st_mode):
                self.fail('%s "%s" is a directory.' % (self.path_type, filename_to_ui(value)),
                          param, ctx)
            if self.writable and not os.access(value, os.W_OK):
                self.fail('%s "%s" is not writable.' % (self.path_type, filename_to_ui(value)),
                          param, ctx)
            if self.readable and not os.access(value, os.R_OK):
                self.fail('%s "%s" is not readable.' % (self.path_type, filename_to_ui(value)),
                          param, ctx)

        return self.coerce_path_result(rv)


def noncontext_callback(f):
    @wraps(f)
    def fake_callback(ctx, param, value):
        return f(value)

    return fake_callback
