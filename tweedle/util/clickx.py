import inspect
import os
import stat
from functools import update_wrapper, wraps
from importlib import import_module

import click
from click._compat import filename_to_ui
from click.formatting import join_options
from click_plugins import with_plugins as __with_plugins
from pkg_resources import iter_entry_points

# click-plugins
# usage:
# ```
#   ...
#   # must on the top of your @click.group
#   @clickx.with_plugins(iter_entry_points('<CLINAME>.plugins'))
#   @...
#   ...
# ```
# more details: https://github.com/click-contrib/click-plugins
#              https://github.com/click-contrib/click-plugins/tree/master/example


def with_plugins(entry_point: str):
    decorator = __with_plugins(iter_entry_points(entry_point))
    return decorator


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


option_of_common_help = click.help_option(help="show usages details")
option_of_not_implement_help = click.help_option(help="Sorry, this command is not implemented now!")


class NoneType(click.ParamType):
    name = "NoneType"

    def convert(self, value, param, ctx):
        return None


none_type = NoneType()


class OptionWithCustomShowDefault(click.Option):
    def get_help_record(self, ctx):
        if self.hidden:
            return
        any_prefix_is_slash = []

        def _write_opts(opts):
            rv, any_slashes = join_options(opts)
            if any_slashes:
                any_prefix_is_slash[:] = [True]
            if not self.is_flag and not self.count:
                rv += ' ' + self.make_metavar()
            return rv

        rv = [_write_opts(self.opts)]
        if self.secondary_opts:
            rv.append(_write_opts(self.secondary_opts))

        help = self.help or ''
        extra = []
        if self.show_envvar:
            envvar = self.envvar
            if envvar is None:
                if self.allow_from_autoenv and ctx.auto_envvar_prefix is not None:
                    envvar = '%s_%s' % (ctx.auto_envvar_prefix, self.name.upper())
            if envvar is not None:
                extra.append(
                    'env var: %s' %
                    (', '.join('%s' % d
                               for d in envvar) if isinstance(envvar, (list, tuple)) else envvar, ))
        if self.default is not None and self.show_default:
            # if isinstance(self.show_default, string_types):
            if isinstance(self.show_default, str):
                default_string = '({})'.format(self.show_default)
            elif isinstance(self.default, (list, tuple)):
                default_string = ', '.join('%s' % d for d in self.default)
            elif inspect.isfunction(self.default):
                default_string = "(dynamic)"
            else:
                default_string = self.default
            # extra.append('default: {}'.format(default_string))
            extra.append('DetectedType: {}'.format(default_string))

        if self.required:
            extra.append('required')
        if extra:
            help = '%s[%s]' % (help and help + '  ' or '', '; '.join(extra))

        return ((any_prefix_is_slash and '; ' or ' / ').join(rv), help)
