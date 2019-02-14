from setuptools import setup

setup(
    name='dragon',
    version='0.0.1-dev',
    py_modules=['dragon'],
    include_package_data=True,
    install_requires=[
        'click',
        'colorama',
    ],
    license='MIT',
    entry_points='''
        [console_scripts]
        dragon=dragon:cli
    ''',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Programming Language :: Python :: 3.7',
    ],
)
