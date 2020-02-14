import shlex
import shutil
import subprocess
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

import click
import toml
from munch import munchify

dev_ignore_this_field = field(init=False)


def recovery_tutor(ctx):
    # 运行时处理外部应用的相关信息的数据类
    @dataclass
    class ExternalAppInfo:
        name: str
        selected_path: Path
        hit: bool = False

    # util
    def strip_ext(filename: str) -> str:
        return filename[:filename.rfind('.')]

    click.secho("Start to recovery this operator system", fg="yellow")
    click.secho("Finding managable Apps...")

    from .. import PROJECT_ROOT

    # app_names: List[str] = [
    #     str(p.name) for p in (PROJECT_ROOT / 'stubs').glob('*.toml')
    # ]
    # for name in app_names:
    #     click.secho(f"\t{strip_ext( name )}")

    # NOTE: 反序列化待查数据 读取所有预设的外部应用的stub
    raw_app_infos: List[dict] = []
    app_paths: List[Path] = [
        p for p in (PROJECT_ROOT / 'stubs').glob('*.toml')
    ]
    for app_path in app_paths:
        if app_path.exists():
            raw_app_infos.append(toml.load(app_path))
        else:
            click.secho(f"Bad load app info: {strip_ext( app_path.name )}")

    # __import__('pprint').pp(raw_app_infos)

    def _get_path(raw_info):
        p = list(
            map(
                lambda kv: kv['path'],
                filter(lambda kv: kv['default_hit'],
                       raw_info["config"]["lookup_paths"])))[0]
        path = Path(p).expanduser()
        return path

    # 序列化结果
    app_infos: List[ExternalAppInfo] = [
        ExternalAppInfo(name=raw_info["name"],
                        selected_path=_get_path(raw_info))
        for raw_info in raw_app_infos
    ]
    # __import__('pprint').pp(app_infos)

    # 用于一会集中管理的配置列表
    need_grab_configs: List[ExternalAppInfo] = []

    # NOTE: 检查所有已知依赖
    #       目前是写死的...
    # REFACTOR:提供用户可选配置
    has_not_hit_cases = False
    for app in app_infos:
        click.secho(f"checking {app.name} current default config hit status ")
        click.secho(f"{str(app.selected_path):<60}", fg="blue", nl=False)
        if app.selected_path.exists():
            click.secho("Hit", fg="green")
            app.hit = True
            need_grab_configs.append(app)
        else:
            click.secho("Not Hit", fg='red')
            has_not_hit_cases = True

    if has_not_hit_cases:
        # Will start to detect current lookup configs orderly
        unhit_apps = [app for app in app_infos if not app.hit]
        click.secho(f"unhit list: { [app.name for app in unhit_apps] }")

    # NOTE: 通过存根反查配置
    # FIXME: 现在会抓取到系统预设配置
    click.secho(f"\nTry to select proper configs from unhit list orderly...",
                fg="yellow")
    app_name_lookup_paths_kv: dict = {
        raw_info['name']: raw_info['config']['lookup_paths']
        for raw_info in raw_app_infos
    }
    for app in unhit_apps:
        click.secho(f"solve {app.name:<54}", nl=False)
        has_hit = False
        for app_path_config in app_name_lookup_paths_kv[app.name]:
            p = munchify(app_path_config)
            if not p.default_hit:
                if p.path.startswith('~'):
                    p.path = Path(p.path).expanduser()
                elif '$' in p.path:
                    from os.path import expandvars
                    changed = expandvars(p.path)
                    if changed != p.path:
                        p.path = Path(changed)
                    else:
                        continue
                p.path = Path(p.path)
                if p.path.exists():
                    click.secho(f"Hit in {str(p.path)}")
                    has_hit = True
                    need_grab_configs.append(
                        ExternalAppInfo(name=app.name,
                                        selected_path=p.path,
                                        hit=True))
                    break
        if not has_hit:
            click.secho(
                "failed to hit config, ignore it as a not installed app")

            # __import__('pprint').pp(lookup_paths)
        # app_config_path = munchify()

        # __import__('pprint').pp(app_config_path)

    # NOTE: 抓取配置至置顶文件夹(仓库)
    click.secho("\nGrab all hit configs to /tmp/.dragon/external_app_configs",
                fg='yellow')
    target_dir: Path = Path('/tmp') / '.dragon' / 'external_app_configs_repo'
    ####
    try:
        shutil.rmtree(target_dir)
    except Exception:
        pass
    ####
    target_dir.mkdir(parents=True, exist_ok=True)
    for app in need_grab_configs:
        click.secho("grab ", nl=False)
        click.secho(f"{app.name:<55}", fg="blue", nl=False)
        dest_dir = target_dir / app.name
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_path = target_dir / app.name / app.selected_path.name
        is_ok = True
        with open(app.selected_path, 'r', encoding='utf-8') as f:
            with open(dest_path, 'w', encoding='utf-8') as d:
                try:
                    d.writelines(f.readlines())
                except IOError:
                    is_ok = False
        if is_ok:
            click.secho("Done", fg='green')
        else:
            click.secho("Error", fg='red')

    # 使用git进行配置控制,主要为连接远程仓库同步
    @contextmanager
    def change_dir_temporarily_to(dir_path):
        from os import chdir
        old_dir_path = Path.cwd()
        chdir(dir_path)
        yield
        chdir(old_dir_path)

    click.secho(
        "\nStart to git init/add/commit your collected configs repo...",
        fg="yellow")

    with change_dir_temporarily_to(target_dir):
        if True:
            # subprocess.run(shlex.split(f"git init {target_dir}"))
            subprocess.run(shlex.split(f"git init"))
        subprocess.run(shlex.split(f"git add -A"))
        subprocess.run(
            shlex.split(f"git commit -m 'first 23333'"))  # TODO:Commit msg
        # subprocess.run(shlex.split(f"git add {target_dir / '*'}"))
        # subprocess.run(shlex.split(f"git commit -m 'first 23333' -- {target_dir}"))

        # TODO:git控制下的其他相关细节, 预置命令自动获取功能git
        #       - remote 建立
        if click.confirm(click.style('add git remote?', fg='yellow'),
                         prompt_suffix=' [No]/Yes:',
                         show_default=False):
            click.secho(f"adding gitremote ...")

        #       - sync 同步专用指令
        #           - push
        if click.confirm(click.style('push to remote?', fg='yellow'),
                         prompt_suffix=' [No]/Yes:',
                         show_default=False):
            subprocess.run(shlex.split(f"git push"))

    # TODO: 派发配置到宿主机
    click.secho(f'Auto symbol link to current user configs path...')
    # 建立软链接,方便统一管理
    # >>> p = Path('mylink')
    # >>> p.symlink_to('setup.py')
    # >>> p.resolve()
    # PosixPath('/home/antoine/pathlib/setup.py')
    # >>> p.stat().st_size
    # 956
    # >>> p.lstat().st_size
    # 8
    # FIXME: 重构以上代码,拆分职责 = .=


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        if click.confirm(click.style('Really sure?'),
                         show_default=False,
                         prompt_suffix='[No]Yes:'):
            recovery_tutor(ctx)
    else:
        click.secho("Subcommands invoke successfully", fg="yellow")


@cli.command()
def info():
    click.secho("info searching...", fg='green')


@cli.command()
def sync():
    click.secho("sync remote configs repo...", fg='green')


@cli.command()
def dump():
    click.secho("dump recovery list", fg='green')
