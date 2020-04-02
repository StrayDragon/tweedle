from pathlib import Path

import click
import inquirer
from box.box import Box
from inquirer.themes import Theme, term

from tweedle.util import clickx


class TweedleTheme(Theme):
    def __init__(self):
        super().__init__()
        self.Question.mark_color = term.blue
        self.Question.brackets_color = term.normal
        self.Question.default_color = term.normal
        self.Editor.opening_prompt_color = term.bright_black
        self.Checkbox.selection_color = term.blue
        self.Checkbox.selection_icon = '>'
        self.Checkbox.selected_icon = '✔️'
        self.Checkbox.selected_color = term.blue + term.bold
        self.Checkbox.unselected_color = term.normal
        self.Checkbox.unselected_icon = 'x'
        self.List.selection_color = term.normal
        self.List.selection_cursor = '>'
        self.List.unselected_color = term.normal


def detect_cwd_project_type():
    if Path.cwd().joinpath('pyproject.toml').exists():
        return 'Python'
    return 'own'


@clickx.noncontext_callback
def use_option_like_argument(value):
    return value


@click.group(name='project')
def cli():
    """
    control your project workspace
    """
    pass


# @click.group(
#     invoke_without_command=True,
#     short_help=f"manage your {detect_cwd_project_type()} project",
# )
# @click.option(
#     '--type',
#     'project_type',
#     help='detect project type',
#     default=detect_cwd_project_type(),
#     show_default=detect_cwd_project_type(),
#     callback=use_option_like_argument,
# )
# @click.pass_context
# @clickx.option_of_common_help
# def cli(ctx, select_project_type):
#     ctx.obj.project.lang = select_project_type
#     project_type = select_project_type if select_project_type != 'own' else 'others'
#     msg = f"Detect current workspace type is {project_type}"
#     cliview.display(msg)
#     pass

# TODO:[Refactor] Will delegate to the cookiecutter(https://github.com/audreyr/cookiecutter) project
# @cli.command()
# @click.argument('project_name')
# @click.option('-L', '--lang', type=click.Choice(['cpp']), required=True)
# @click.option('-B', '--build-tool', type=click.Choice(['cmake']))
# @click.option('-T', '--third-party', type=click.Choice(['googletest']))
# def new(project_name, lang, build_tool, third_party):
#     """Generate a target project"""
#     import os
#     cur_path = os.getcwd()
#     os.mkdir(os.path.join(cur_path, project_name))

#     # Display these after success
#     cliview.display('Generated the project in ',
#                     font_color=cliview.Colors.Green,
#                     bold=True,
#                     nl=False)
#     cliview.display(sh.current_running_path())
#     cliview.display(f'  Project Name : {project_name}')
#     cliview.display(f'  Language     : {lang}')
#     if build_tool:
#         cliview.display(f'  Build Tool   : {build_tool}')
#     if third_party:
#         cliview.display(f'  External-Libs: {third_party}')

# @cli.command(context_settings={"ignore_unknown_options": True})
# @click.option('--select-lang', 'select_lang')
# @click.argument('optionlike', type=str, nargs=1)  # FIXME:use option like arguments
# @clickx.option_of_common_help
# @click.pass_context
# @click.help_option()
# def spawn_old(ctx, select_lang, optionlike):
#     if optionlike == '--list':
#         cliview.display('hit --list')
#         return
#     if not select_lang:
#         select_lang = ctx.obj.project.lang
#     if (select_lang := select_lang.strip().lower()) == 'python':
#         available_configs = [
#             'pyright',
#             'mypy',
#             'vimspector(python)',
#             'pre-commit',
#             'tox',
#             'poetry',
#         ]
#         cliview.display(f"list all available {select_lang} configs")
#         for no, config in enumerate(available_configs):
#             click.secho(f"{no}.  ", fg='yellow', nl=False)
#             click.secho(f"{config}")
#         cliview.display('Select config(s) your want to spawn to this project')


def init_monkey_patch():
    def inquirer_patch_checkbox_support_jk_move():
        from readchar import key
        from inquirer import errors
        from inquirer.render.console._checkbox import Checkbox

        def process_input(self, pressed):
            if pressed == 'k':
                self.current = max(0, self.current - 1)
                return
            elif pressed == 'j':
                self.current = min(len(self.question.choices) - 1, self.current + 1)
                return
            elif pressed == key.UP:
                self.current = max(0, self.current - 1)
                return
            elif pressed == key.DOWN:
                self.current = min(len(self.question.choices) - 1, self.current + 1)
                return
            elif pressed == key.SPACE:
                if self.current in self.selection:
                    self.selection.remove(self.current)
                else:
                    self.selection.append(self.current)
            elif pressed == key.LEFT:
                if self.current in self.selection:
                    self.selection.remove(self.current)
            elif pressed == key.RIGHT:
                if self.current not in self.selection:
                    self.selection.append(self.current)
            elif pressed == key.ENTER:
                result = []
                for x in self.selection:
                    value = self.question.choices[x]
                    result.append(getattr(value, 'value', value))
                raise errors.EndOfInput(result)
            elif pressed == key.CTRL_C:
                raise KeyboardInterrupt()

        Checkbox.process_input = process_input

    def inquirer_patch_list_support_jk_move():
        from readchar import key
        from inquirer import errors
        from inquirer.render.console._list import List

        def process_input(self, pressed):
            question = self.question
            if pressed == 'k':
                if question.carousel and self.current == 0:
                    self.current = len(question.choices) - 1
                else:
                    self.current = max(0, self.current - 1)
                return
            if pressed == 'j':
                if question.carousel and self.current == len(question.choices) - 1:
                    self.current = 0
                else:
                    self.current = min(len(self.question.choices) - 1, self.current + 1)
                return
            if pressed == key.UP:
                if question.carousel and self.current == 0:
                    self.current = len(question.choices) - 1
                else:
                    self.current = max(0, self.current - 1)
                return
            if pressed == key.DOWN:
                if question.carousel and self.current == len(question.choices) - 1:
                    self.current = 0
                else:
                    self.current = min(len(self.question.choices) - 1, self.current + 1)
                return
            if pressed == key.ENTER:
                value = self.question.choices[self.current]
                raise errors.EndOfInput(getattr(value, 'value', value))

            if pressed == key.CTRL_C:
                raise KeyboardInterrupt()

        List.process_input = process_input

    inquirer_patch_list_support_jk_move()
    inquirer_patch_checkbox_support_jk_move()


@cli.command()
@clickx.option_of_common_help
def spawn():
    """
    [WIP] spawn project default configs\n
    WARNING: Current implementation is not completed, please do not use this cmd in real workspace
    """
    import shutil
    # FIXME: Temp code !!!
    temp_project_config_templates_root_path = Path("~/Repo/ProjectConfigTemplates").expanduser()
    if not temp_project_config_templates_root_path.exists():
        click.secho("Not Found Temp 'ProjectConfigTemplates'", fg='red')
        raise click.Abort()
    temp_py_root_path: Path = temp_project_config_templates_root_path / 'Python3'
    temp_py_root_path.mkdir(parents=True, exist_ok=True)
    # temp_js_root_path = temp_project_config_templates_root_path / 'JavaScript'
    # temp_vim_root_path = temp_project_config_templates_root_path / 'Vim'

    init_monkey_patch()
    box = Box(default_box=True)
    box.python3 = {
        ('pyright', 'pyrightconfig.json', '.'),
        ('mypy', 'mypy.ini', '.'),
        ('vimspector(python)', '.vimspector.json', '.'),
        ('pre-commit(python)', '.pre-commit-config.yaml', '.'),
        ('tox', 'tox.ini', '.'),
        ('poetry', 'poetry.toml', '.'),
        ('bump2version config', '.bumpversion.cfg', '.'),
        ('flake8', '.flake8', '.'),
        ('coc-setting(python)', 'coc-settings.json', '.vim/coc-setting.json'),
    }
    # box.javascript = ['eslint', 'webpack.config']
    # box.git = ['.gitconfig', '.gitignore']
    # box.vscode = ['task.json']
    lang = inquirer.list_input(
        "All supportted project configs type:",
        choices=[key.title() for key in box.keys()],
    )
    lang = lang.lower()
    supportted_configs = [
        inquirer.Checkbox(
            'project_config_type',
            message="Choose the config(s) your want to generate in this workspace:",
            choices=[info[0] for info in box.get(lang)],
        ),
    ]
    supportted_configs_rsp = inquirer.prompt(supportted_configs, theme=TweedleTheme())
    # print(supportted_configs_rsp['project_config_type'])

    target = box.get(lang)
    config_names = supportted_configs_rsp['project_config_type']
    for name in config_names:
        filename, rela_cwd_path = None, None
        for k in target:
            if name == k[0]:
                filename, rela_cwd_path = k[1], k[2]
                break
        src_path = str(temp_py_root_path / filename)
        dest_path: Path = Path.cwd() / rela_cwd_path / filename
        dest_path.parent.mkdir(exist_ok=True, parents=True)
        skip = True
        is_exist = False
        if dest_path.exists():
            is_exist = True
            if click.confirm(
                    click.style(f'\n{filename}', fg='blue') + ' already exist, overwrite? '):
                skip = False
            else:
                click.secho('skiping...', fg='green')
        if not skip or not is_exist:
            msg = "Copying " + click.style(f"{filename:<24}", fg='blue') + "to " + click.style(
                f"{rela_cwd_path:<14}\t", fg='blue')
            click.echo(msg, nl=False)
            shutil.copy(src_path, str(dest_path))
            click.secho("Done", fg='green')
    click.secho("\nHave a fun day and enjoy coding :)")

    # choice = inquirer.list_input("Public or private?", choices=['public', 'private'])
    # print(choice)
    # box.to_json('project-configs.json')
    pass
