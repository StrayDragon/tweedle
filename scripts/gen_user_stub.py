from pathlib import Path

from box import Box

b = Box(default_box=True)

b.author = 'straydragon'
b.version = ''

b.management.app.configs.auto_detect = True
b.management.app.configs.ignore_non_exist = True
b.management.app.configs.not_grub_root = True


def make_hook(a, pr, po):
    return Box(apply_for=a, pre_scripts=pr, post_scripts=po, default_box=True)


app_names = [p.name.split('.')[0] for p in Path('../stubs').glob('*.toml')]
b.management.app.configs.hooks = [make_hook(name, [], []) for name in app_names]

b.management.backup.paths = []
b.management.backup.auto_recovery = True

user_defined_manage_stub = b

print(user_defined_manage_stub.to_toml('all.toml'))
