# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dragon', 'dragon.cmd']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'munch>=2.5.0,<3.0.0', 'toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['dragon = dragon.entry:main']}

setup_kwargs = {
    'name': 'dragon',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'straydragon',
    'author_email': 'straydragonl@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
