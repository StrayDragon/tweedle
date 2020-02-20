import shlex
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Dict, List

import click
import toml
from munch import munchify

from tweedle import PROJECT_NAME, PROJECT_ROOT
from tweedle.util import archive, clickx, fs, sh

dev_ignore_this_field = field(init=False)
BACKUP_RECOVERY_METAINFO_FILE_NAME = f'__{PROJECT_NAME}_backup_recovery_stub__.toml'


def prepare_to_backup_existing_app_configs_tutor():
    # 运行时处理外部应用的相关信息的数据类
    @dataclass
    class ExternalAppInfo:
        name: str
        selected_path: Path
        hit: bool = False

        def __post_init__(self):
            self.selected_path = self.selected_path.expanduser()

    click.secho("Start to recovery this operator system", fg="yellow")
    click.secho("Finding managable Apps...")

    # NOTE: 反序列化待查数据 读取所有预设的外部应用的stub
    raw_app_infos: List[dict] = []
    app_stub_paths: List[Path] = [p for p in (PROJECT_ROOT / 'stubs').glob('*.toml')]
    for app_path in app_stub_paths:
        if app_path.exists():
            raw_app_infos.append(toml.load(app_path))
        else:
            click.secho(f"Bad load app info: {fs.strip_ext( app_path.name )}")

    # __import__('pprint').pp(raw_app_infos)

    # 序列化结果
    app_infos: List[ExternalAppInfo] = [
        ExternalAppInfo(name=raw_info["name"],
                        selected_path=Path(raw_info['config']['habitual_path']))
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
    click.secho(f"\nTry to select proper configs from unhit list orderly...", fg="yellow")
    app_name_lookup_paths_kv: Dict[str, List[str]] = {
        raw_info['name']: raw_info['config']['lookup_paths']
        for raw_info in raw_app_infos
    }
    for app in unhit_apps:
        click.secho(f"solve {app.name:<54}", nl=False)
        has_hit = False
        for app_condidate_path in app_name_lookup_paths_kv[app.name]:
            if app_condidate_path:
                if app_condidate_path.startswith('~'):
                    app_condidate_path = Path(app_condidate_path).expanduser()
                elif '$' in app_condidate_path:
                    from os.path import expandvars
                    changed = expandvars(app_condidate_path)
                    if changed != app_condidate_path:
                        app_condidate_path = Path(changed)
                    else:
                        continue
                app_condidate_path = Path(app_condidate_path)
                if app_condidate_path.exists():
                    click.secho(f"Hit in {str(app_condidate_path)}")
                    has_hit = True
                    need_grab_configs.append(
                        ExternalAppInfo(name=app.name, selected_path=app_condidate_path, hit=True))
                    break
        if not has_hit:
            click.secho("failed to hit config, ignore it as a not installed app")

            # __import__('pprint').pp(lookup_paths)
        # app_config_path = munchify()

        # __import__('pprint').pp(app_config_path)

    # NOTE: 抓取配置至置顶文件夹(仓库)
    click.secho("\nGrab all hit configs to /tmp/.tweedle/external_app_configs", fg='yellow')
    target_dir: Path = Path('/tmp') / '.tweedle' / 'external_app_configs_repo'
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
    click.secho("\nStart to git init/add/commit your collected configs repo...", fg="yellow")

    with sh.change_dir_temporarily_to(target_dir):
        if True:
            # subprocess.run(shlex.split(f"git init {target_dir}"))
            subprocess.run(shlex.split(f"git init"))
        subprocess.run(shlex.split(f"git add -A"))
        commit_msg = click.prompt(
            'Please input commit message([...] is default)',
            prompt_suffix=f': ',
            default='init configs repo',
        )
        subprocess.run(shlex.split(f"git commit -m '{commit_msg}'"))
        # subprocess.run(shlex.split(f"git add {target_dir / '*'}"))
        # subprocess.run(shlex.split(f"git commit -m 'first 23333' -- {target_dir}"))

        # TODO:git控制下的其他相关细节, 预置命令自动获取功能git
        #       - remote 建立
        if click.confirm(click.style('add git remote?', fg='yellow'),
                         prompt_suffix=' [No]/Yes:',
                         show_default=False):
            remote_url = click.prompt('Please input remote url', show_default=False)
            subprocess.run(shlex.split(f"git remote add origin '{remote_url}'"))

        #       - sync 同步专用指令
        #           - push
        if click.confirm(click.style('push to remote now?', fg='yellow'),
                         prompt_suffix=' [No]/Yes:',
                         show_default=False):
            subprocess.run(shlex.split(f"git push -u origin master"))


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.secho(
            "this tutor will help you to create a configurations file(stub.toml) to hold:",
            fg='yellow',
        )
        managables = "app configs", "backup or recovery archive file"
        for managable in managables:
            click.secho(f'\t - {managable}', fg='green')
        if click.confirm('continue?', abort=True):
            # TODO: create user manage configurations file
            pass


# @cli.command()
# def info():
#     click.secho("info searching...", fg='green')

# @cli.command()
# def sync():
#     click.secho("sync remote configs repo...", fg='green')

# @cli.command()
# def dump():
#     click.secho("dump recovery list", fg='green')


@clickx.noncontext_callback
def check_and_convert_path(value):
    if not value:
        return value
    path = Path(value)
    if not path.exists():
        raise click.BadParameter(f'File not found or incorrect path')
    if path.is_dir():
        raise click.BadParameter(f'Not a file')
    return path


@cli.command()
@click.help_option()
@click.option(
    '-i',
    '--backup-stub-file',
    'backup_stub_path',
    # type=clickx.Path(exists=True, file_okay=True, dir_okay=True),
    # required=True,
    callback=check_and_convert_path,
)
def backup(backup_stub_path: Path):
    """"""
    if not backup_stub_path:
        if click.confirm(
                'Ensure to step into backup git managable configs tutor?',
                default=True,
                abort=True,
                prompt_suffix=' [Yes]/No: ',
                show_default=False,
        ):
            prepare_to_backup_existing_app_configs_tutor()
            click.secho('Done ´ ▽ ` )ﾉ`')
            return
    # 0. Check backup_stub_path correctness: by option callback
    # 1. Find and deserialize user defined backup configs
    #    from Path.cwd() (default) or user defined file
    # check no options situation
    # if not backup_stub_path:
    #     backup_stub_path = Path.cwd() / f'{PROJECT_NAME}_backup_stub.toml'
    # if not backup_stub_path.exists():
    #     click.secho(
    #         f"not found backup description, check out 'tweedle manage backup --help'",
    #         err=True,
    #         fg='red',
    #     )
    #     raise click.Abort()

    # 1. Find and deserialize user defined backup configs file
    stub = munchify(toml.load(backup_stub_path))

    # 2. Display collected infos
    backup_paths = stub.backup.paths
    will_be_archived_paths = [Path(p) for p in backup_paths]

    for path in will_be_archived_paths:
        if not path.exists():
            click.secho(f'error: {str(path)} is not exist!')
            raise click.Abort()

    click.secho(f"these files or folders will be archived...")
    for p in backup_paths:
        click.secho(f'\t{p:<60}')

    # 3. Popup confirm dialog and prepare to archive
    if click.confirm(click.style(f'Are these correctly?'),
                     default=True,
                     abort=True,
                     show_default=False,
                     prompt_suffix=' [Yes]/No: '):

        # a. prepare final metainfo stub
        kv = {
            'backup': {
                'archive_file': {
                    'auto_recovery': False
                },
                'old_paths': [str(path) for path in will_be_archived_paths]
            },
        }

        # (option) add auto_recovery related metainfo to stub
        if stub.backup.auto_recovery:
            # prepare 'autorecovery' metainfo
            kv['backup']['archive_file'] = {'auto_recovery': True}
            kv['recovery'] = {
                'archive_file': {
                    'irrelevant_recovery_paths':
                    [str(path.relative_to(Path.home())) for path in will_be_archived_paths],
                },
            }
            click.echo('create and write recovery stub...', nl=False)
            temp_dir = TemporaryDirectory()
            _p: Path = Path(temp_dir.name) / BACKUP_RECOVERY_METAINFO_FILE_NAME
            with open(_p, 'w', encoding='utf-8') as f:
                toml.dump(kv, f)
            will_be_archived_paths.append(_p)
            click.secho('  Done', fg='green')

        # b. retrieve archived path and prepare
        # NOTE: user maybe set 'store_path' to:
        # a. ~/xxx/xxx b. ~/xxx/xxx.zip c. /xxx/xxx d. /xxx/xxx.zip
        # e. ../xxx f. ../xxx.zip g. xxx.zip h. xxx ........
        # but now, only support paths with like .zip suffix(b. or d.)
        # or empty(default: archived) in Path.cwd()!
        try:
            store_path = Path(stub.backup.store_path).expanduser()
        except AttributeError:
            click.secho('not found store_path attribution select current workspace (archived.zip)')
            store_path = Path.cwd() / 'archived.zip'
        if not store_path.suffix:
            raise click.ClickException(
                f"Wrong stubfile attribution: 'store_path = \"{str(store_path)}\"'")
        store_path.parent.mkdir(parents=True, exist_ok=True)
        arcname, arctype = fs.strip_ext(store_path.name), archive.get_arctype(store_path.name)

        # 4. start to archive
        click.secho(f"\tNote: maybe take a long time depend on these size")
        all_tasks = archive.compress_processing(arcname,
                                                arctype,
                                                *will_be_archived_paths,
                                                dest_dir=store_path.parent)
        with click.progressbar(all_tasks, label='archiving') as bar:
            for _ in bar:
                pass

        # d. done
        click.secho(f'archived {str(store_path)}')
        click.secho(f'Done. ´ ▽ ` )ﾉ`')
        temp_dir.cleanup()


@cli.command()
@click.help_option()
@click.option(
    '-i',
    '--archive-file',
    'archived_file_path',
    required=False,
    callback=check_and_convert_path,
)
# @click.option('-o', '--configs', 'app_configs')
def recovery(archived_file_path):
    if not archived_file_path:
        if click.confirm(
                'Ensure to step into recovery git managable configs tutor?',
                default=True,
                abort=True,
                prompt_suffix=' [Yes]/No: ',
                show_default=False,
        ):

            # prepare_to_recovery_git_managed_app_configs_tutor()
            # 0. check user preference? from defined stubinfo or default and get behavior stubinfo
            # 1. check git managed repo location: local or remote repo? finally, unify them to 'p'
            click.secho("Please input your configs repo location:")
            click.secho("support: location path('~/xxx'), https & git protocal url")
            url: str = click.prompt('url', type=str)
            app_dir_path = Path(click.get_app_dir(PROJECT_NAME, roaming=False)).expanduser()
            app_dir_path.mkdir(parents=True, exist_ok=True)
            if url.startswith('https') or url.startswith('git'):
                with sh.change_dir_temporarily_to(app_dir_path):
                    subprocess.run(shlex.split(f"git clone '{url}' external/app_configs_repo"))
                    Path('external').mkdir(parents=True, exist_ok=True)
                    repo_path = app_dir_path / 'external' / 'app_configs_repo'
                    # TODO: if git clone error, note to handle this exception
            else:
                if url.startswith('~'):
                    repo_path = Path(url).expanduser()
                else:
                    repo_path = Path(url)
            try:
                if repo_path.is_dir():
                    click.secho(f'find repo : {str( repo_path )}')
            except Exception:
                raise click.UsageError('please input correct url... Abort!')
            # 2. from this 'p', dispatch corresponding configs to correct position
            # TODO: 派发配置到宿主机
            click.secho(f'will symbol link to current user configs path...')
            click.pause()
            # 建立软链接,方便统一管理
            # >>> p = Path('mylink')
            # >>> p.symlink_to('setup.py')
            # >>> p.resolve()
            # PosixPath('/home/antoine/pathlib/setup.py')
            # >>> p.stat().st_size
            # 956
            # >>> p.lstat().st_size
            # 8
            with sh.change_dir_temporarily_to(repo_path):
                # find habitual_path in stubs dict by folder name
                app_stubs = (toml.load(p) for p in (PROJECT_ROOT / 'stubs').glob('*.toml'))
                db = {app_stub['name']: Path(app_stub['habitual_path']) for app_stub in app_stubs}
                for appname in db.keys():
                    config_path: Path = Path.cwd() / appname / db[appname].name
                    target_path: Path = db[appname].expanduser()
                    click.secho(f"deal {appname}: link {config_path} to {target_path}", nl=False)
                    target_path.parent.mkdir(parent=True, exist_ok=True)
                    config_path.symlink_to(target_path)
                    click.secho(f"\tok")

            click.secho('Done ´ ▽ ` )ﾉ`')
            return

    # 0. Check archived path correctness: by option callback

    # 1. Check to see whether it contains
    #    the description file (BACKUP_RECOVERY_METAINFO_FILE_NAME)

    # 2. Unpack(extract) all to temp-directory
    home_path = Path.home()
    with TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        archive.extract_all(archived_file_path, temp_dir)

        # retrieve description file (BACKUP_RECOVERY_METAINFO_FILE_NAME.toml) path
        df = temp_dir / BACKUP_RECOVERY_METAINFO_FILE_NAME
        stub = munchify(toml.load(df))
        if not stub.backup.archive_file.auto_recovery:
            click.secho('detect auto_recovery=False, cleanup...')
            click.Abort()

        # print(list(temp_dir.glob('*')))

        # 3. Assign these files or folders if necessary(has the `auto_recovery=true`)
        good_paths = [Path(p) for p in stub.recovery.archive_file.irrelevant_recovery_paths]
        with click.progressbar(good_paths, label='recovering') as bar:
            for good in bar:
                # print(f'move {temp_dir / good.name} -> {home_path / good.parent}')
                shutil.move(str(temp_dir / good.name), str(home_path / good.parent))
        click.secho(f'Done. ´ ▽ ` )ﾉ`')
